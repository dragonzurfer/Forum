from django.shortcuts import render,get_object_or_404,redirect,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
import datetime
from django.template import loader, RequestContext
from polls.forms import UserForm,ForumForm,QuestionForm
from .models import Question,Choice,Forum
from django.urls import reverse
from django.views import generic,View
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,permission_required
from django.utils.decorators import method_decorator  
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from pure_pagination.mixins import PaginationMixin

index_view='polls/index.html'

class IndexView(generic.ListView):
    context_object_name='latest_question_list'
    template_name=index_view
    model=Question


    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['now'] = datetime.datetime.now()
        context['method']= self.request.user.has_perm('polls.delete_question')
        return context


class DetailView(generic.DetailView):
    model=Question
    template_name='polls/detail.html'
   

class ResultView(generic.DetailView):
    model=Question
    template_name='polls/results.html'


class QuestionCreate(LoginRequiredMixin,CreateView):
    model=Question
    fields=['question_text']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(QuestionCreate, self).form_valid(form)

class QuestionDelete(LoginRequiredMixin,generic.DeleteView):
    model=Question
    success_url=reverse_lazy('polls:index')
    def dispatch(self, request, *args, **kwargs):
        @permission_required('polls.delete_question',login_url='polls:user_login')
        def wrapper(request, *args, **kwargs):
            return super(QuestionDelete, self).dispatch(request, *args, **kwargs)
        return wrapper(request, *args, **kwargs)


class QuestionUpdate(LoginRequiredMixin,generic.UpdateView):
    model=Question
    fields=['question_text']
    template_name_suffix = '_update_form'
    def dispatch(self, request, *args, **kwargs):
        @permission_required('polls.change_question',login_url='polls:user_login')
        def wrapper(request, *args, **kwargs):
            return super(QuestionUpdate, self).dispatch(request, *args, **kwargs)
        return wrapper(request, *args, **kwargs)


@login_required(login_url='polls:user_login')
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    error_message="PLEASE SELECT A CHOICE"
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
      
       return  render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        
        return render(request, 'polls/results.html', {
            'question': question
        })


@login_required(login_url='polls:user_login')
def create_choice(request,question_id):
    question=get_object_or_404(Question,pk=question_id)

    if request.method=="POST":
        created_choice =request.POST['choice']
        question.choice_set.create(choice_text=created_choice)
        question.save()
        return HttpResponseRedirect(reverse('polls:detail',args=(question.id,),current_app=request.resolver_match.namespace))
    if request.method=="GET":
        return render(request,'polls/create_question_choice.html', {'question':question})
       
   
@login_required(login_url='polls:user_login')
@permission_required('polls.change_question',login_url='polls:user_login')
def delete_choice(request,question_id):
    question=get_object_or_404(Question,pk=question_id)
    if request.method=="POST":
        if request.user.has_perm('polls.delete_choice'):
            delete_choice =question.choice_set.get(pk=request.POST['choice'])
            delete_choice.delete()
        return HttpResponseRedirect(reverse('polls:detail',args=(question.id,),current_app=request.resolver_match.namespace))
    if request.method=="GET":
        return render(request,'polls/delete_question_choice.html',{'question':question})



class UserFormView(View):
    form_class=UserForm
    template_name='polls/user_registration_form.html'
    def get(self,request):
        form=self.form_class(None)
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form=self.form_class(request.POST)
        if(form.is_valid()):
            user=form.save(commit=False)
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            email=form.cleaned_data['email']
            user.set_password(password)
            user.save()

            user=authenticate(username=username,password=password)

            if(user is not None):
                if user.is_active:
                    login(request,user)
                    return redirect('polls:index')

        return render(request,self.template_name,{'form':form})



class LoginFormView(View):
   
    template_name='polls/user_registration_form.html'
    def get(self,request):
        return render(request,'polls/user_registration_form.html')

  
    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('polls:forum_index'))
        else:
           return render(request,'polls/user_registration_form.html',{
                'error_message': "Incorrect credentials.",
            })


def logout_view(request):
    logout(request)
    return redirect('polls:user_login')




class ForumCreate(LoginRequiredMixin,CreateView):
    login_url='polls/login/'
    template_name='polls/forum_form.html'
    form_class=ForumForm
    def get(self,request):
        form=self.form_class(None)
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form=self.form_class(request.POST)
        if(form.is_valid()):
            new_forum_name=form.cleaned_data['forum_name']
            new_forum_description=form.cleaned_data['forum_description']
            new_forum=Forum(forum_name=new_forum_name,forum_description=new_forum_description)
            new_forum.save()
            return redirect('polls:forum_index')
        return render(request,self.template_name,{'form':form})


def ForumQuestionCreate(request,forum_id):
    login_url='polls/login/'
    template_name='polls/forum_question_create.html'
    form_class=QuestionForm
    forum = get_object_or_404(Forum, pk=forum_id)
    if request.method=="GET":
        form=form_class(None)
        return render(request,template_name,{'form':form,'forum':forum})

    if request.method=="POST":
        form=form_class(request.POST)
        if(form.is_valid()):
            question_text=form.cleaned_data['question_text']
            question=Question(question_text=question_text)
            question.user=request.user
            question.save()
            f=Forum.objects.get(id=forum_id)
            f.save()

            question.forum.add(f)
            question.save()
            f.save()
            return HttpResponseRedirect(reverse('polls:forum_detail',args=(forum.id,),current_app=request.resolver_match.namespace))
        return render(request,template_name,{'form':form})


    

class ForumIndexView(PaginationMixin,generic.ListView):
    template_name='polls/forum_index.html'
    context_object_name='latest_forum_list'
    model=Forum
    paginate_by = 3
    

    def get_context_data(self, **kwargs):
        context = super(ForumIndexView, self).get_context_data(**kwargs)
        context['now'] = datetime.datetime.now()
        forum_list = Forum.objects.all()
        return context



def ForumDetailView(request,forum_id):
    forum = get_object_or_404(Forum, pk=forum_id)
    return render(request, 'polls/forum_detail.html', {
            'forum': forum
        })













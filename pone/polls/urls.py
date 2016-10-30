from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
app_name='polls'

urlpatterns = [
    #url(r'^$', views.current_datetime, name=''),
    url(r'^$', views.ForumIndexView.as_view(), name='index'),
    #
    url(r'^question/index$', views.IndexView.as_view(), name='index'),
    #
     url(r'login/$',views.LoginFormView.as_view(),name='user_login'), 
    #
    url(r'^logout/$',views.logout_view,name='user_logout'),
    #
    url(r'register/$', views.UserFormView.as_view(), name='user_register'),
    # ex: /polls/5/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultView.as_view(), name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    #ex:/polls/5/create_choice
    url(r'^(?P<question_id>[0-9]+)/create_choice/$', views.create_choice, name='create_choice'),
    #
    url(r'^(?P<question_id>[0-9]+)/delete_choice/$', views.delete_choice, name='delete_choice'),
    #/polls/add
    url(r'^question/add/$',views.QuestionCreate.as_view(),name='question_create'),
    #/polls/3/delete
    url(r'^(?P<pk>[0-9]+)/delete/$', views.QuestionDelete.as_view(), name='question_delete'),
    #/polls/3/update
    url(r'^(?P<pk>[0-9]+)/update/$', views.QuestionUpdate.as_view(), name='question_update'),
    #
    url(r'^Forum/add/$',views.ForumCreate.as_view(),name='forum_create'),
    #/polls/forums/5/
    url(r'^forums/(?P<forum_id>[0-9]+)/$', views.ForumDetailView, name='forum_detail'),
    #
    url(r'^forums/$',views.ForumIndexView.as_view(),name='forum_index'),
    #
    url(r'^forums/(?P<forum_id>[0-9]+)/question/add/$',views.ForumQuestionCreate,name='forum_question_create'),
    ]

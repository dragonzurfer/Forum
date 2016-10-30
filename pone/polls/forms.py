from django import forms
from django.contrib.auth.models import User
from .models import Forum,Question

class UserForm(forms.ModelForm):
	password=forms.CharField(widget=forms.PasswordInput)
	
	def clean_username(self):
		username=self.cleaned_data['username']
	    	if User.objects.filter(username=self.cleaned_data['username']).exists():
    			raise forms.ValidationError(u'Username "%s" shut up and take another one.' % username)
    		elif len(username)<5:
    			raise forms.ValidationError(u'Username "%s" less than 5 letters' % username)
    		return username

	class Meta:
		model=User
		fields=['username','email','password']

	def clean_email(self):
		email=self.cleaned_data['email']
	    	if User.objects.filter(email=email).exists():
    			raise forms.ValidationError(u'email "%s" shut up and take another one.' % email)
    		return email

   	



class ForumForm(forms.ModelForm):
	class Meta:
		model=Forum
		fields=['forum_name','forum_description']


	


class QuestionForm(forms.ModelForm):
    question_text= forms.CharField(label='question_text', max_length=100)
    class Meta:
		model=Question
		fields=['question_text']


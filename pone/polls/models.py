from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
import datetime

class Forum(models.Model):
	forum_name=models.CharField(max_length=200)
	forum_description=models.TextField()


	def get_absolute_url(self):
		return reverse('polls:forum_index',kwargs={'pk':self.pk})

	def __str__(self):
		return self.forum_name

	class Meta:
		ordering=('-id',)

	


class Question(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	question_text=models.CharField(max_length=200)
	pub_date=models.DateTimeField('date published',default=datetime.datetime.now())
	forum=models.ManyToManyField(Forum)
	def was_published_recently(self):
		return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

	def get_absolute_url(self):
		return reverse('polls:detail',kwargs={'pk':self.pk})

	def get_user(self):
		return self.user.username

	def __str__(self):
		return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.TextField()
    votes = models.IntegerField(default=0)
	
    def __str__(self):
       return self.choice_text
# Create your models here.


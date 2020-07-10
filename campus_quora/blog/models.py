import json

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# from django.contrib.postgres.fields import ArrayField





TAGS = (
    (0,"Department"),
    (1,"Clubs"),
    (2,"placements"),
    (3,"fests"),
    (4,"hostel"),
    (5,"general")
)

ANSWERED = (
    (0,"Not Answered"),
    (1,"Answered")
)

class Question(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.IntegerField(choices=TAGS, default=0)
    #slug = models.SlugField(max_length=200, unique=True)
    votes = models.IntegerField(default=0)
    # votes = ArrayField(
    #     models.IntegerField(),
    #     size=1000,
    # )
    updated_on = models.DateTimeField(auto_now= True)
    question = models.TextField(max_length = 250,)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=ANSWERED, default=0)
    title = models.CharField(max_length = 11, )

    def get_absolute_url(self):
        user = User.objects.get(pk=User)
        return reverse('blog:myques', user.username)

    # for sorting
    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return str(self.pk)

class Answer(models.Model):
    Question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    votes = models.IntegerField(default=0)
    class Meta:
        # ordering = ['-votes']
        ordering = ['-created_on']

    def __str__(self):
        return str(self.User)

class Quesvotes(models.Model):
    Question = models.ForeignKey(Question, on_delete=models.CASCADE)
    User = models.ForeignKey(User, on_delete=models.CASCADE)

class Ansvotes(models.Model):
    Answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    User = models.ForeignKey(User, on_delete=models.CASCADE)

class Bookmark(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Question = models.ForeignKey(Question, on_delete=models.CASCADE)

class Notifications(models.Model):
    who = models.CharField(max_length = 250, )
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    #whom = models.CharField(max_length = 250, )
    created_on = models.DateTimeField(auto_now_add=True)
    Question = models.ForeignKey(Question, on_delete=models.CASCADE)
    Answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_on']
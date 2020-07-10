from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('tags', 'question', 'title')

class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ['answer']
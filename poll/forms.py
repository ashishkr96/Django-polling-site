from django import forms
from .models import *
from django.forms import formset_factory
from django.contrib.auth.forms import UserCreationForm


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question']



class ImageQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question']

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choices
        fields = ['choices']





Choicefactoryform = formset_factory(ChoiceForm, extra=9)

class ImageChoice(forms.ModelForm):
    class Meta:
        model = ImagePoll
        fields = ['choice']


ImageChoicefactoryform = formset_factory(ImageChoice, extra=5)

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required')
    email = forms.EmailField(max_length=254, help_text='Enter a active email address')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )




class MomentForm(forms.ModelForm):
    class Meta:
        model = MyMoments
        fields = ('Memories',)



class PersonalityQuestionForm(forms.ModelForm):
    Question = forms.CharField(max_length=200, required=True, help_text='Required')
    class Meta:
        model = PersonalityQuestion
        fields = ('Question','image',)



class PersonalityAnswerForm(forms.ModelForm):
    class Meta:
        model = PersonalityAnswer
        fields = ('description',)

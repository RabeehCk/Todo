from django import forms
from work.models import *


class Register(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password']
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your username'}),
            'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your first name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your last name'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter your email'}),
            'password':forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter your password'}),
        }


class TaskForm(forms.ModelForm):

    class Meta:
        model = taskmodel
        fields = ['task_name','task_description']
        widgets = {
            'task_name':forms.TextInput(attrs={'class':'form-control ms-2 me-2','placeholder':'Enter the task'}),
            'task_description':forms.Textarea(attrs={'class':'form-control ms-2 me-2','placeholder':'Enter the task description',}),
        }


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter your password'}))
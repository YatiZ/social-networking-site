
from logging import PlaceHolder
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from requests import options


YEARS = [x for x in range(1930,2022)]
CHOICES = ((1,'male'),(2,'female'))

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'placeholder':'example@gmail.com'}))
    birthday_date = forms.DateField(label="Your Birthday Date",widget=forms.SelectDateWidget(years=YEARS,attrs={'style':'font-size: 20px;'}))
    gender = forms.ChoiceField(choices=CHOICES,widget=forms.RadioSelect(attrs={'class':"radio"}))
    class Meta:
        model = User
        fields = ["username","birthday_date","gender","email","password1","password2"]
        labels = {
            "username":"Your Name",
            
        }


# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post 
#         fields = ["post","image"]  
        
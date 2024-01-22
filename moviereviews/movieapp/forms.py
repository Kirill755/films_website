from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import *


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget = forms.TextInput(attrs={'class':'form-input'}))
    password = forms.CharField(label='Пароль', widget = forms.PasswordInput(attrs={'class':'form-input'}))

class AddFilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = ['film_title', 'Year', 'genre', 'director', 'actors', 'description', 'picture']
        widgets = {
            'film_title': forms.TextInput(attrs={'class': 'form-input'}),
            'Year': forms.TextInput(attrs={'class': 'form-input'}),
           'genre': forms.TextInput(attrs={'class': 'form-input'}),
            'director': forms.TextInput(attrs={'class': 'form-input'}),
            'actors': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

class AddReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['Review_title', 'Main_text', 'Mark']
        widgets = {
            'Review_title': forms.TextInput(attrs={'class': 'form-input'}),
            'Main_text': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

class AddNewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['News_title', 'Main_text']
        widgets = {
            'News_title': forms.TextInput(attrs={'class': 'form-input'})
        }
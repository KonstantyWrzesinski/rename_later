from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserPreference

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=65,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter username'
        })
    )

    password = forms.CharField(
        max_length=65,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter password'
        })
    )

class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username','email','password1','password2'] 


class UserPreferenceForm(forms.ModelForm):
    class Meta:
        model = UserPreference
        fields = ['preferred_city']
        widgets = {
            'preferred_city': forms.TextInput(attrs={
                'placeholder': 'Enter your preferred city',
            })
        }
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
#from .models import UserPreference

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

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter username'
        }),
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter password'
        }),
        help_text='Password must contain at least 8 characters and cannot be entirely numeric.'
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm password'
        }),
        help_text='Enter the same password again for verification.'
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


# class UserPreferenceForm(forms.ModelForm):
#     class Meta:
#         model = UserPreference
#         fields = ['preferred_city']
#         widgets = {
#             'preferred_city': forms.TextInput(attrs={
#                 'placeholder': 'Enter your preferred city',
#             })
#         }
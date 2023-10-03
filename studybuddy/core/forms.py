from django import forms
from django.contrib.auth.forms import UserCreationForm
from . models import UserProfile


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Username:',
                               max_length=64, required=True)
    email = forms.EmailField(label='Email:',
                             max_length=254, required=True)
    password1 = forms.CharField(label='Password:',
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password:',
                                widget=forms.PasswordInput)


class LoginForm(forms.Form):
    username = forms.CharField(label='Username:',
                               max_length=64, required=True)
    password = forms.CharField(label='Password:', widget=forms.PasswordInput)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_pic', 'bio']
        widgets = {
            'profile_pic': forms.FileInput(attrs={'class': 'custom-file-input'}),
        }

        widgets = {
            'bio': forms.Textarea(attrs={'class': 'bio-textarea'}),
        }

    bio = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'bio-textarea'}),
        error_messages={'required': ''}  # Set the error message to an empty string
    )

    profile_pic = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'custom-file-input'}),
        error_messages={'required': ''}  # Set the error message to an empty string
    )
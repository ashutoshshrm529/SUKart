from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import KartUser


class CustomerRegisterForm(UserCreationForm):
    class Meta:
        model = KartUser
        fields = ('username', 'email', 'password1', 'password2', 'city', 'dob')


class DistributorRegisterForm(UserCreationForm):
    class Meta:
        model = KartUser
        fields = ('username', 'email', 'password1', 'password2', 'city', 'dob')


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = KartUser
        fields = ('username', 'email', 'city', 'dob')

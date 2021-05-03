from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import DM


class new_user(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).count():
            raise forms.ValidationError('Email already in use!')
        else:
            return email


class change_user(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

from django import forms
from crispy_forms.helper import FormHelper
from cristy_forms.layout import Submit
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib.auth import get_user_model

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('user', 'gender', 'age', 'occupation')

class UserCustomCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('user')
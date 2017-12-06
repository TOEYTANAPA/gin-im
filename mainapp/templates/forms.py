from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import extras
from .models import Profile


class ProfileForm(UserCreationForm):
    
    sex = forms.CharField(max_length=10, required=False, help_text='')
    birthdate = forms.DateField(widget=extras.SelectDateWidget(years = range(2022, 1930, -1)))
    phone= forms.CharField(max_length=20, required=False, help_text='')

    class Meta:
    
        model = Profile
        fields = ('sex', 'birthdate', 'phone', )
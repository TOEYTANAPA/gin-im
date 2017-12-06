from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import extras
from .models import Profile,Review


class ProfileForm(forms.Form):
    age =  forms.CharField(max_length=10, required=False, help_text='',widget=forms.TextInput(attrs={'class': 'uk-input'}))
    sex = forms.CharField(max_length=10, required=False, help_text='',widget=forms.TextInput(attrs={'class': 'uk-input'}))
    birthdate = forms.DateField(widget=extras.SelectDateWidget(years = range(2022, 1930, -1)))
    phone= forms.CharField(max_length=20, required=False, help_text='',widget=forms.TextInput(attrs={'class': 'uk-input',}))



class ReviewForm(forms.Form):
    comment =  forms.CharField(max_length=100, help_text='',widget=forms.Textarea(attrs={'cols': 5,'rows': 5,'class': 'uk-textarea','placeholder':'เขียนรีวิว', }))
    # sex = forms.CharField(max_length=10, required=False, help_text='',widget=forms.TextInput(attrs={'class': 'uk-input'}))
    # birthdate = forms.DateField(widget=extras.SelectDateWidget(years = range(2022, 1930, -1)))
    # phone= forms.CharField(max_length=20, required=False, help_text='',widget=forms.TextInput(attrs={'class': 'uk-input'}))


# class ReviewForm(forms.Form):
#     class Meta:
#         model = Review
#         fields = [ 'picDR','comment']
#         widgets = {
            
#             'comment': Textarea(attrs={'cols': 5, 'rows': 5,'placeholder': "Comment and Share your happy dog's photo."}),
#             'picDR': FileInput(attrs={'id': 'imgInp'}),
#         }
    # class Meta:
    
    #     model = Profile
    #     fields = ('age','sex', 'birthdate', 'phone', )
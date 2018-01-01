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

class StoreForm(forms.Form):
    store_name =  forms.CharField(max_length=200, help_text='',widget=forms.TextInput(attrs={'class': 'uk-input'}))
    place =  forms.CharField(max_length=1000, help_text='',widget=forms.TextInput(attrs={'class': 'uk-input'}))
    store_image = forms.FileField()
    phone =  forms.CharField(max_length=20, help_text='',widget=forms.TextInput(attrs={'class': 'uk-input'}))
    # tags =  forms.CharField(max_length=1000, help_text='',widget=forms.TextInput(attrs={'class': 'uk-input'}))
    category =  forms.CharField(max_length=50, help_text='',widget=forms.TextInput(attrs={'class': 'uk-input'}))
    time_open = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    TRUE_FALSE_CHOICES = (
    (True, 'Yes'),
    (False, 'No')
    )
    delivery = forms.ChoiceField(choices = TRUE_FALSE_CHOICES, label="", 
                              initial='', widget=forms.Select(), required=True)

class MenuForm(forms.Form):
    menu_name =  forms.CharField(max_length=200, help_text='',widget=forms.TextInput(attrs={'class': 'uk-input'}))
    menu_price =  forms.CharField(max_length=20, help_text='',widget=forms.TextInput(attrs={'class': 'uk-input'}))
    menu_image = forms.FileField()
    # time_close = models.TimeField(null=True, blank=True)
    # phone = models.CharField(max_length=20,blank=True,null=True)
    # tags = models.CharField(max_length=1000,blank=True,null=True)
    # qrcode = models.ImageField(upload_to='qrcodes',blank=True,null=True)
    # category = models.CharField(max_length=30,blank=True,null=True)
    # quote = models.CharField(max_length=1000,blank=True,null=True)
    # latitude=models.FloatField(default=14.073565,null=True, blank=True)
    # longtitude=models.FloatField(default=100.607963,null=True, blank=True)
    # social = moฝdels.CharField(max_length=100,blank=True,null=True)
    # likes = models.MฝanyToManyField(User, related_name="likes")

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
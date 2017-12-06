from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import extras
from mainapp.models import Profile


class SignUpForm(UserCreationForm):
    # first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    # last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
  
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    image = forms.FileField()
    def clean_email(self):
    	data = self.cleaned_data['email']
    	if User.objects.filter(email=data).exists():
        	raise forms.ValidationError("This email already used")
    	return data

    # def save(self, commit=True):
    #     user = super(UserCreationForm, self).save(commit=False)
    #     user.email = self.cleaned_data["email"]
    #     if commit:
    #         user.save()
                
    class Meta:
    
        model = User
        fields = ('username',  'email', 'password1', 'password2','image' )


class ProfileForm(forms.Form):
    name = forms.CharField(max_length=30, required=False, help_text='',widget=forms.TextInput(attrs={'class': 'uk-input'}))
    # age =  forms.CharField(max_length=10, required=False, help_text='',widget=forms.TextInput(attrs={'class': 'uk-input'}))
    # sex = forms.CharField(max_length=10, required=False, help_text='',widget=forms.TextInput(attrs={'class': 'uk-input'}))
    # birthdate = forms.DateField(widget=extras.SelectDateWidget(years = range(2022, 1930, -1)))
    phone = forms.CharField(max_length=20, required=False, help_text='',widget=forms.TextInput(attrs={'class': 'uk-input',}))
    address = forms.CharField(max_length=50, required=False, help_text='',widget=forms.TextInput(attrs={'class': 'uk-input',}))
    image = forms.FileField()
    class Meta:
       model = Profile
       fields = ('name',  'phone', 'address','image' )

class StoreForm(forms.Form):
    name = forms.CharField(max_length=30, required=True, help_text='',widget=forms.TextInput(attrs={'class': 'uk-input'}))
    place = forms.CharField(max_length=50, required=True, help_text='',widget=forms.TextInput(attrs={'class': 'uk-input'}))
    image=forms.FileField()
    # time_open_close = models.TimeField()
    # time_close =
    
    # phone = models.CharField(max_length=20,blank=True,null=True)
    # tags = models.CharField(max_length=100,blank=True,null=True)
    # qrcode = models.ImageField(upload_to='qrcodes',blank=True,null=True)
    # category = models.CharField(max_length=30,blank=True,null=True)
    # quote = models.CharField(max_length=1000,blank=True,null=True)
    # latitude=models.FloatField(default=14.073565,null=True, blank=True)
    # longtitude=models.FloatField(default=100.607963,null=True, blank=True)


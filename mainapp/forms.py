from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import extras
from django.conf import settings

from .models import Profile,Review
# from django.forms.extras.widgets import SelectDateWidget

class ProfileForm(forms.Form):
    age =  forms.CharField(max_length=10, required=False, help_text='',widget=forms.TextInput(attrs={'class': 'uk-input'}))
    sex = forms.CharField(max_length=10, required=False, help_text='',widget=forms.TextInput(attrs={'class': 'uk-input'}))
    birthdate = forms.DateField(widget=extras.SelectDateWidget(years = range(2022, 1930, -1)))
    phone= forms.CharField(max_length=20, required=False, help_text='',widget=forms.TextInput(attrs={'class': 'uk-input',}))



class ReviewForm(forms.Form):
    comment =  forms.CharField(max_length=2000, help_text='',widget=forms.Textarea(attrs={'cols': 5,'rows': 5,'class': 'uk-textarea','placeholder':'เขียนรีวิว', }))
   
class StoreForm(forms.Form):
    TRUE_FALSE_CHOICES = (
    (True, 'มีบริการส่ง'),
    (False, 'ไม่มีบริการส่ง')
    )
    DAY_OPEN = (('วันจันทร์', 'วันจันทร์'),('วันอังคาร', 'วันอังคาร'),('วันพุธ', 'วันพุธ'),('วันพฤหัสบดี', 'วันพฤหัสบดี'),('วันศุกร์.', 'วันศุกร์'),('วันเสาร์.', 'วันเสาร์'),('SUN.', 'วันอาทิตย์'),
        ('วันจันทร์ - วันศุกร์', 'วันจันทร์ - วันศุกร์'),('วันเสาร์ - วันอาทิตย์', 'วันเสาร์ - วันอาทิตย์'),('ทุกวัน', 'ทุกวัน'))
    store_name =  forms.CharField(max_length=200, help_text='',widget=forms.TextInput(attrs={'class': 'uk-input'}))
    place =  forms.CharField(max_length=1000, help_text='',widget=forms.TextInput(attrs={'class': 'uk-input'}))
    store_image = forms.FileField()
    phone =  forms.CharField(max_length=20, help_text='',widget=forms.TextInput(attrs={'class': 'uk-input'}))
    # tags =  forms.CharField(max_length=1000, help_text='',widget=forms.TextInput(attrs={'class': 'uk-input'}))
    category =  forms.CharField(max_length=50, help_text='',widget=forms.TextInput(attrs={'class': 'uk-input'}))
    time_open = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    time_close = forms.TimeField(widget=forms.TimeInput(format='%H:%M'),required = False)
    # time_open = forms.DateField(widget=extras.SelectDateWidget)
    day_open = forms.ChoiceField(choices = DAY_OPEN, label="",initial='', widget=forms.Select(), required=True)
    delivery = forms.ChoiceField(choices = TRUE_FALSE_CHOICES, label="", 
                              initial='', widget=forms.Select(), required=True)

class MenuForm(forms.Form):
    menu_name =  forms.CharField(max_length=200, help_text='',widget=forms.TextInput(attrs={'class': 'uk-input'}))
    menu_price =  forms.CharField(max_length=20, help_text='',widget=forms.TextInput(attrs={'class': 'uk-input'}))
    menu_image = forms.FileField()

class SlipPaymentForm(forms.Form):
    # slip_image = forms.FileField( ) 

    slip_image = forms.FileField() 
    # time_close = models.TimeField(null=True, blank=True)
class InformationsForm(forms.Form):
    # age = forms.IntegerField(required=True)
    # gender = (('Male','male'),('Female','female'))
    birthdate = forms.DateField(widget=extras.SelectDateWidget)
    sex = forms.ChoiceField(choices=(('Male','male'),('Female','female')),required=True, 
        widget=forms.RadioSelect(attrs={'class' : '',}))
    size = forms.ChoiceField(choices = (('thin','ผอม'),('fit','หุ่นดี/ทั่วไป'),('chubby','อวบ'),('fat','อ้วน')), 
        required=True, help_text='',widget=forms.CheckboxSelectMultiple)
    salary = forms.ChoiceField(choices=(('น้อยกว่า 10,000','น้อยกว่า 10,000' ),('10,000-19,000','10,000-19,000')
        ,('20,000-29,999','20,000-29,999'),('30,000-39,000','30,000-39,000'),('40,000-49,000','40,000-49,000')
        ,('50,000 ขึ้นไป','50,000 ขึ้นไป')), required=True)
    meal = forms.ChoiceField(choices=(('มื้อเช้า','มื้อเช้า'),('มื้อเที่ยง','มื้อเที่ยง'),('มื้อเย็น','มื้อเย็น'),('มื้อดึก','มื้อดึก')), required=True)
    reason = forms.ChoiceField(choices=(('รสชาติ','รสชาติ'), ('ราคา','ราคา'),('บริการ','บริการ') ,('ความสะอาด','ความสะอาด'), ('บรรยากาศ','บรรยากาศ'), ('สถานที่ตั้ง','สถานที่ตั้ง')), required=True)
    # favorites = models.CharField(max_length=200,blank=False,null=False)
    social_media = forms.ChoiceField(choices=(('Facebook','facebook'), ('Twitter','twitter'),('Line','line') ,('Instagram','instagram')), required=True)
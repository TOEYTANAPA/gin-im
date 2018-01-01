from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea,TextInput,FileInput,ChoiceField,Select
from datetime import datetime
from django.contrib.postgres.fields import ArrayField
# Create your models here.


class Store(models.Model):
	name = models.CharField(max_length=200)
	place = models.CharField(max_length=1000)
	image=models.ImageField(upload_to='images')
	day_open = models.CharField(max_length=200,null=True, blank=True)
	time_open = models.TimeField(null=True, blank=True)
	time_close = models.TimeField(null=True, blank=True)
	phone = models.CharField(max_length=20,blank=True,null=True)
	tags = models.CharField(max_length=100,blank=True,null=True)
	qrcode = models.ImageField(upload_to='qrcodes',blank=True,null=True)
	category = models.CharField(max_length=30,blank=True,null=True)
	quote = models.CharField(max_length=1000,blank=True,null=True)
	latitude=models.FloatField(default=14.073565,null=True, blank=True)
	longtitude=models.FloatField(default=100.607963,null=True, blank=True)
	social = models.CharField(max_length=100,blank=True,null=True)
	likes = models.ManyToManyField(User, related_name="likes",blank=True,null=True)
	created_by = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)


	def __str__(self):
		return self.name

	@property
	def total_likes(self):
		return self.likes.count()

class Menu(models.Model):
	store = models.ForeignKey(Store, on_delete=models.SET_NULL,blank=True,null=True)
	name = models.CharField(max_length=100)
	price = models.CharField(max_length=50)
	image=models.ImageField(upload_to='images')
	isSell = models.BooleanField(default=True)
	created_by = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)

	def __str__(self):
		return self.name

class Order(models.Model):
	store = models.ForeignKey(Store,on_delete=models.SET_NULL,blank=True,null=True)
	menu = ArrayField(models.CharField(max_length=500), blank=True,null=True)
	amount = ArrayField(models.CharField(max_length=500), blank=True,null=True)
	user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)
	date = models.DateTimeField(default=datetime.now, blank=True)
	address = models.CharField(max_length=1000,blank=True,null=True)
	
class Profile(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)
	name = models.CharField(max_length=100)
	age = models.CharField(max_length=10)
	sex = models.CharField(max_length=10)
	birthdate = models.DateField(blank=True,null=True)
	email = models.EmailField(max_length=100)
	phone_number = models.CharField(max_length=20)
	address = models.CharField(max_length=1000,blank=True,null=True)
	picture=models.FileField(upload_to="profilePicture/",default="")
	person_type =  models.CharField(max_length=100,blank=True,null=True)

class StoreByUser(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)
	store = models.ForeignKey(Store,on_delete=models.SET_NULL,blank=True,null=True)
	

class Review(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)
	store = models.ForeignKey(Store, on_delete=models.SET_NULL,blank=True,null=True)
	comment = models.CharField(max_length=5000)
	rating = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True,null=True,)

class User_session(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)
	action = models.CharField(max_length=50,blank=True,null=True)
	value = models.CharField(max_length=100,blank=True,null=True)
	created_at = models.DateTimeField(auto_now_add=True,null=True,)

class Anonymous_session(models.Model):
	name = models.CharField(max_length=100,blank=True,null=True)
	action = models.CharField(max_length=50,blank=True,null=True)
	value = models.CharField(max_length=100,blank=True,null=True)
	created_at = models.DateTimeField(auto_now_add=True,null=True,)

class HungerHistory(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)
	sex = models.CharField(max_length=10,blank=True,null=True)
	age = models.CharField(max_length=10,blank=True,null=True)
	salary = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True,null=True,)

class UserValueStore(models.Model):
	store = models.ForeignKey(Store, on_delete=models.SET_NULL,blank=True,null=True)
	user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)
	frequency = models.IntegerField(default=0)

class UserValueDelivery(models.Model):
	store = models.ForeignKey(Store, on_delete=models.SET_NULL,blank=True,null=True)
	user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)
	cumulative_purchase = models.IntegerField(default=0)

class UserValueStoreAndDelivery(models.Model):
	store = models.ForeignKey(Store, on_delete=models.SET_NULL,blank=True,null=True)
	user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)
	frequency = models.IntegerField(default=0)
	cumulative_purchase = models.IntegerField(default=0)


class QMatrix(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)
	frequency = models.IntegerField(default=0)
	amount = ArrayField(models.IntegerField(default=0), blank=True,null=True)
	reward = ArrayField(models.IntegerField(default=0), blank=True,null=True)
	


# class Review(models.Model):
#     RATING_CHOICES = (
#         (1, '1'),
#         (2, '2'),
#         (3, '3'),
#         (4, '4'),
#         (5, '5'),
#     )
#     person = models.ForeignKey(Person,on_delete=models.CASCADE,null=True)
#     pub_date = models.DateTimeField(auto_now_add=True)
#     user_name = models.CharField(max_length=200,null=True,default="")
#     comment = models.CharField(max_length=200)
#     rating = models.IntegerField()
#     picDR = models.ImageField(upload_to="documents/",default="")

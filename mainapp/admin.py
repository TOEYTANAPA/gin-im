from django.contrib import admin
from .models import *

class StoreAdmin(admin.ModelAdmin):
	list_display=[f.name for f in Store._meta.fields]
admin.site.register(Store, StoreAdmin)

class MenuAdmin(admin.ModelAdmin):
	list_display=[f.name for f in Menu._meta.fields]
admin.site.register(Menu, MenuAdmin)


class ProfileAdmin(admin.ModelAdmin):
	list_display=[f.name for f in Profile._meta.fields]
admin.site.register(Profile, ProfileAdmin)

class ReviewAdmin(admin.ModelAdmin):
	list_display=[f.name for f in Review._meta.fields]
admin.site.register(Review, ReviewAdmin)

class User_sessionAdmin(admin.ModelAdmin):
	list_display=[f.name for f in User_session._meta.fields]
admin.site.register(User_session, User_sessionAdmin)

class OrderAdmin(admin.ModelAdmin):
	list_display=[f.name for f in Order._meta.fields]
admin.site.register(Order, OrderAdmin)

class StoreByUserAdmin(admin.ModelAdmin):
	list_display=[f.name for f in StoreByUser._meta.fields]
admin.site.register(StoreByUser, StoreByUserAdmin)

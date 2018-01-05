from django.conf.urls import url,include
from . import views
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
import os
from django.conf.urls.static import static


import os

urlpatterns = [

    url(r'^$', views.home, name='home'),
    url(r'^report/?$',views.report, name='report'),
    url(r'^questionnaire/?$',views.questionnaire, name='questionnaire'),
    # url(r'^profile/?$',views.profile, name='profile'),
    url(r'^delivery/?$',views.delivery, name='delivery'),
    url(r'^success/(?P<order_id>\d+)/?$',views.success, name='success'),
    url(r'^addStore/?$', views.addStore, name='add_store'),
    url(r'^(?P<pk>\d+)/addMenu/?$', views.addMenu, name='add_menu'),
    url(r'^store/(?P<pk>\d+)/?$', views.shop, name='shop'),
    url(r'^search/(?P<cate>.*)?$',views.searchBycate, name='search_cate'),
    url(r'^usecoupon/(?P<coupon>\d+)?$',views.use_coupon, name='use_coupon'),
    url(r'^search/?$',views.searchAll, name='search_input'),
    url(r'^about-ginim/?$',views.about_us, name='about_us'),
    url(r'^contact/?$',views.contact, name='contact'),
    url(r'^order/?$',views.order, name='order'),
    url(r'^like/$', views.like_button, name='like_button'),
    url(r'^checkIsSell/$', views.checkIsSell, name='checkIsSell'),
    url(r'^select-payment/(?P<pk>\d+)/$', views.payment, name='select_payment'),
    url(r'^edit-store/$', views.outofstock, name='outofstock'),
    url(r'^inf$', views.fill_in, name='inf'),
    url(r'^inf-complete$', views.fill_in_complete, name='inf-complete'),
    url(r'^inf-edit$', views.fill_in_edit, name='is_inf'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG404: :
#     urlpatterns += staticfiles_urlpatterns()
from django.conf.urls import url,include
from . import views

from django.contrib.auth import views as auth_views


from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # url(r'^$', views.home, name='home'),
    url(r'^',  include('mainapp.urls',namespace='mainapp')),
    url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout,{'next_page': 'home'}, name='logout'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),  # <--
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^settings/$', views.profile, name="profile"),
    url(r'^settings/store/$', views.profile_store, name="profile_store"),
    url(r'^password/$', views.change_password, name='change_password'),
    # url(r'^success/$',  name='change_password_success'),

    # url(r'^password/$', views.change_password, name='change_password'),
    # url(r'import_rule/', views.import_rule, name='import_rule'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# from django.conf.urls import url, include
# from django.contrib import admin
# from django.contrib.auth import views as auth_views

# from mysite.core import views as core_views

# urlpatterns = [
#     url(r'^$', core_views.home, name='home'),
#     url(r'^login/$', auth_views.login, name='login'),
#     url(r'^logout/$', auth_views.logout, name='logout'),
#     url(r'^oauth/', include('social_django.urls', namespace='social')),  # <--
#     url(r'^admin/', admin.site.urls),
# ]
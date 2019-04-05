from django.urls import include, re_path
from . import views


app_name = 'app'

# Url patterns for the website.
urlpatterns = [
    re_path('^$', views.landing, name='landing'),
    re_path('^profile/$', views.profile, name='profile'),
    re_path('^home/$', views.home, name='home'),
    re_path('^profile/update_profile_pic/$', views.update_profile_pic, name='update_profile_pic'),
    re_path('^update_profile_details/$', views.update_profile, name='update_profile'),
]

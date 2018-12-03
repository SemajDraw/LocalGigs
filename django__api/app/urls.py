from django.urls import include, re_path
from . import views
from django.views.decorators.csrf import csrf_exempt
from api.views import tm_get_events, tm_get_venue, UpdatePosition, UpdateInterestedHTML

app_name = 'app'

# Url patterns for the website.
urlpatterns = [
    re_path('^$', views.landing, name='landing'),
    re_path('^profile/$', views.profile, name='profile'),
    re_path('^profile/update_profile_pic/$', views.update_profile_pic, name='update_profile_pic'),
    re_path('^update_profile_details/$', views.update_profile, name='update_profile'),
    re_path('^get_events/$', tm_get_events, name='get_events'),
    re_path('^get_venue_details/$', tm_get_venue, name='get_venue'),
    re_path('^update_position/$', UpdatePosition.as_view(), name='update_position'),
    re_path('^update_interested_html/$', csrf_exempt(UpdateInterestedHTML.as_view()), name='update_interested_html'),
]

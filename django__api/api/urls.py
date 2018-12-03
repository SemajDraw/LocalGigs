from django.urls import include, re_path
from . import views

app_name = 'api'

# URL's for the applications api
urlpatterns = [
    re_path(r'^login/$', views.token_login, name='token_login'),
    re_path(r'^get_events/$', views.tm_get_events, name='get_events'),
    re_path('^get_venue_details/$', views.tm_get_venue, name='get_venue'),
    re_path(r'^rest_auth/', include('rest_auth.urls')),
    re_path(r'^rest_auth/registration/', include('rest_auth.registration.urls')),
    re_path(r'^rest_auth/facebook/$', views.FacebookLogin.as_view(), name='fb_login')
]

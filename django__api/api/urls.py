from django.urls import include, re_path
from . import views

app_name = 'api'

# URL's for the applications api
urlpatterns = [
    re_path(r'^login/$', views.token_login, name='token_login'),
    re_path(r'^search_events/$', views.search_ticketmaster_events, name='search_events'),
    re_path('^save_event/$', views.update_saved_events, name='save_event'),
    re_path('^delete_event/$', views.delete_saved_event, name='delete_event'),
    re_path('^update_recommended_events/$', views.update_recommended_events, name='update_recommended_events'),
    re_path('^render_recommended_events/$', views.render_recommended_events, name='render_recommended_events'),

    re_path('^get_saved_events/$', views.get_saved_events, name='get_saved_events'),
    re_path('^get_recommended_events/$', views.get_recommended_events, name='get_recommended_events'),
    re_path('^get_ticketmaster_events/$', views.get_ticketmaster_events, name='get_ticketmaster_events'),

    re_path(r'^rest_auth/', include('rest_auth.urls')),
    re_path(r'^rest_auth/registration/', include('rest_auth.registration.urls')),
    re_path(r'^rest_auth/facebook/$', views.FacebookLogin.as_view(), name='fb_login'),
]

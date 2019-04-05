from django.urls import re_path
from . import views

app_name = 'api'

urlpatterns = [
    re_path(r'^get_recommendations/', views.get_recommendations, name='get_recommendations')
]


from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    re_path('', include('app.urls')),
    path('admin/', admin.site.urls),
    re_path('account/', include('allauth.urls')),
    re_path('social/', include('social_django.urls')),
    re_path('^api/', include('api.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

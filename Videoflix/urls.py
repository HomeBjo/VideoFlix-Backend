
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from debug_toolbar.toolbar import debug_toolbar_urls
from Users.views import activate


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')), 
    path('users/', include('Users.urls')),
    path('videos/', include('Video_App.urls')),
    path('django-rq/', include('django_rq.urls')),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) + debug_toolbar_urls()
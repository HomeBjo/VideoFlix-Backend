
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')), 
    path('users/', include('Users.urls')),
    path('videos/', include('Video_App.urls')),
    
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
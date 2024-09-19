
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from debug_toolbar.toolbar import debug_toolbar_urls
from Users.views import PasswordResetAPIView, activate, PasswordResetConfirmAPIView
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')), 
    path('users/', include('Users.urls')),
    path('videos/', include('Video_App.urls')),
    path('django-rq/', include('django_rq.urls')),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('password_reset/', PasswordResetAPIView.as_view(), name='password_reset'),
    path('password_reset/confirm/<uidb64>/<token>/', PasswordResetConfirmAPIView.as_view(), name='password_reset_confirm'),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) + debug_toolbar_urls()
# + staticfiles_urlpatterns()

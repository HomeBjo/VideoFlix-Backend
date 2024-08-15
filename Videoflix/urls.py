
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from debug_toolbar.toolbar import debug_toolbar_urls
from Users.views import PasswordResetAPIView, PasswordResetCompleteView, activate
from django.contrib.auth import views as auth_views
from Users.views import   CustomPasswordResetConfirmView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')), 
    path('users/', include('Users.urls')),
    path('videos/', include('Video_App.urls')),
    path('django-rq/', include('django_rq.urls')),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    # path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/', PasswordResetAPIView.as_view(), name='password_reset'),
    # path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # path('login/', LoginView.as_view(), name='login'), # oder halt in der user view 

]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) + debug_toolbar_urls()
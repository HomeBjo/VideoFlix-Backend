
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Users.views import LoginViewSet, LogoutViewSet, RegisterViewSet, CheckEmailView, TokenVerificationViewSet, UserDataViewSet, UpdateUserDataViewSet



router = DefaultRouter()
router.register(r'login',  LoginViewSet, basename='login')
router.register(r'logout', LogoutViewSet, basename='logout')
router.register(r'register', RegisterViewSet, basename='register')
router.register(r'check-email', CheckEmailView, basename='check-email')
router.register(r'verify-token', TokenVerificationViewSet, basename='verify-token')
router.register(r'user-data', UserDataViewSet, basename='user-data')
router.register(r'update-user-data', UpdateUserDataViewSet, basename='update-user-data')


app_name = 'Users'

urlpatterns = [
    path('', include(router.urls)),

]

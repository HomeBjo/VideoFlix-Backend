
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from Users.views import LoginViewSet, LogoutViewSet, RegisterViewSet
from Users import views



router = DefaultRouter()
router.register(r'login',  LoginViewSet, basename='login')
router.register(r'logout', LogoutViewSet, basename='logout')
router.register(r'register', RegisterViewSet, basename='register')

app_name = 'Users'

urlpatterns = [
    path('', include(router.urls)),
    # path('register/', register_user, name='register'),  # Funktionsbasierte Ansicht separat registrieren
    # path('login/', LoginView.as_view(), name='login'),  # Wenn LoginView ein APIView ist
    # path('logout/', LogoutView.as_view(), name='logout'),  # Wenn LogoutView ein APIView ist
]

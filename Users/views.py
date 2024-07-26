
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import logout
from Users.serializers import UserSerializer
from rest_framework import  viewsets
from django.views.decorators.cache import cache_page
from Videoflix.settings import CACHE_TTL
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT



CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)



class RegisterViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        """
        Handle user registration.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class LoginViewSet(ObtainAuthToken, viewsets.ViewSet):
    """
    Handle user login and return authentication token.
    """
    @cache_page(CACHE_TTL)
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class LogoutViewSet(viewsets.ViewSet):
    """
    Handle user logout.
    """
    def create(self, request, *args, **kwargs):
        logout(request)
        return Response({'message': 'Logout successful'})
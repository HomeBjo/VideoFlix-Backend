from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from django.contrib.auth import logout



@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    API endpoint for user registration.
    """
    serialized = UserSerializer(data=request.data)
    if serialized.is_valid():
        user = serialized.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        }, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class LoginView(ObtainAuthToken):
    """
    API endpoint for user login. Inherits from ObtainAuthToken to provide token authentication.
    """
    def post(self, request, *args, **kwargs):
        """
        Handle user login and return authentication token.
        """
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
        
        
        
class LogoutView(APIView):
    """
    API endpoint for user logout.
    """
    def post(self, request, format=None):
        """
        Handle user logout and provide a success message.
        """
        logout(request)
        return Response({'message': 'Logout successful'})
    
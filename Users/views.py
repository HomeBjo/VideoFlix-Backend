
from django.shortcuts import redirect
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import logout
from Users.serializers import EmailAuthTokenSerializer, PasswordResetConfirmSerializer, PasswordResetSerializer, UserSerializer
from rest_framework import  viewsets
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import  redirect
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action



CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
# @cache_page(CACHE_TTL)   ----- den decorator bei der nötigen function ergänzen

def activate(request, uidb64, token):
    """
        weiterleitung nach der E-Mail-Aktivierung
    """
    CustomUser = get_user_model()  
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = CustomUser.objects.get(pk=uid)
        print(f'try get uid: {uid}')
        print(f'try get user: {user}')
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        print(f'New token created: {token.key}') 
        print(request,'user activated')
        return redirect('http://localhost:4200/video_site')
    else:
        print(request,'user not activated') 
        return redirect('http://localhost:4200/login')

        
class RegisterViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def create(self, request):
        """
        Handle user registration.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('templates_activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'protocol': 'http'
                # 'protocol': 'https' if request.is_secure() else 'http'
            })
            to_email = serializer.validated_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.content_subtype = "html"
            email.send()

            return Response({
                'message': 'Please confirm your email address to complete the registration.'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class LoginViewSet(ObtainAuthToken, viewsets.ViewSet):
    permission_classes = (AllowAny,)
    """
    Handle user login and return authentication token.
    """
    def create(self, request, *args, **kwargs):
        serializer = EmailAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        if not user.is_active:
            return Response({'error': 'This account is not active. Please activate your account first.'}, status=status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
        

class TokenVerificationViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        token_key = request.data.get('token')
        user_id = request.data.get('user_id')

        print(f"Received data: {request.data}")  # Debugging

        if not token_key or not user_id:
            return Response({'error': 'Token oder user_id fehlen.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = Token.objects.get(key=token_key)
            print('Token found:', token)
            CustomUser = get_user_model()
            user_id = int(user_id)
            user = CustomUser.objects.get(pk=user_id)

            print(f'Received token: {token_key}, user_id: {user_id}, user: {user}')
            if token.user == user and user.is_active:
                return Response({
                    'token': token.key,
                    'user_id': user.pk,
                    'email': user.email
                })

            return Response({'error': 'Token und Benutzer stimmen nicht überein oder Benutzer ist nicht aktiv.'},
                            status=status.HTTP_400_BAD_REQUEST)

        except Token.DoesNotExist:
            return Response({'error': 'Ungültiges Token.'}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Benutzer existiert nicht.'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'error': 'Ungültige user_id.'}, status=status.HTTP_400_BAD_REQUEST)



class LogoutViewSet(viewsets.ViewSet):
    """
    Handle user logout.
    """
    def create(self, request, *args, **kwargs):
        logout(request)
        return Response({'message': 'Logout successful'})
    

class CheckEmailView(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def create(self, request):
        email = request.data.get('email')
        CustomUser = get_user_model()
        if CustomUser.objects.filter(email=email).exists():
            return Response({'exists': True}, status=status.HTTP_200_OK)
        return Response({'exists': False}, status=status.HTTP_200_OK)

    
class PasswordResetAPIView(APIView):
    
    def post(self, request, *args, **kwargs):
        print('111111111', self)
        serializer = PasswordResetSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password reset e-mail has been sent."}, status=status.HTTP_200_OK)

User = get_user_model()
class PasswordResetConfirmAPIView(APIView):
    def post(self, request, *args, **kwargs):
        uidb64 = kwargs.get('uidb64')
        token = kwargs.get('token')
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            serializer = PasswordResetConfirmSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)
            return Response({"detail": "Password has been reset."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid token or user."}, status=status.HTTP_400_BAD_REQUEST)
        


class UserDataViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        """
        Diese Methode wird verwendet, um das queryset zu filtern,
        sodass nur der Benutzer mit der angegebenen ID zurückgegeben wird.
        """
        user_id = self.request.query_params.get('userId')
        User = get_user_model()

        if user_id:
            return User.objects.filter(pk=user_id)
        return User.objects.none()  # Gibt ein leeres queryset zurück, wenn keine ID angegeben ist

    @action(detail=False, methods=['get'], url_path='user-data')
    def get_user_data(self, request):
        """
        Diese Methode wird verwendet, um die Benutzer-Daten zu holen.
        """
        user_id = request.query_params.get('userId')
        print(f"user_id: {user_id}")

        # Mit get_queryset() kannst du sicherstellen, dass das queryset korrekt gefiltert wird
        queryset = self.get_queryset()

        if not queryset.exists():
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(queryset.first())  # Nur den ersten Benutzer im queryset serialisieren
        return Response(serializer.data, status=status.HTTP_200_OK)
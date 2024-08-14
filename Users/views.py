
from django.shortcuts import redirect
from django.urls import reverse_lazy
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import logout
from Users.serializers import EmailAuthTokenSerializer, UserSerializer
from rest_framework import  viewsets
from django.views.decorators.cache import cache_page
from Videoflix.settings import CACHE_TTL
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils.decorators import method_decorator
from .forms import CustomPasswordResetForm
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView




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


class LogoutViewSet(viewsets.ViewSet):
    """
    Handle user logout.
    """
    def create(self, request, *args, **kwargs):
        logout(request)
        return Response({'message': 'Logout successful'})
    
class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm #zusätliche Validierungen möglich. hierdurch wird die standart email send angepasst!
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    success_url = reverse_lazy('password_reset_done') 

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'
    
    
class CheckEmailView(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def create(self, request):
        email = request.data.get('email')
        CustomUser = get_user_model()
        if CustomUser.objects.filter(email=email).exists():
            return Response({'exists': True}, status=status.HTTP_200_OK)
        return Response({'exists': False}, status=status.HTTP_200_OK)
    
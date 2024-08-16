
from pyexpat.errors import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import logout
from Users.serializers import EmailAuthTokenSerializer, PasswordResetSerializer, UserSerializer
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

from django.contrib.auth.views import  PasswordResetConfirmView
from rest_framework.views import APIView
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.tokens import default_token_generator
<<<<<<< Updated upstream
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import render, redirect
from django.contrib import messages

=======
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
>>>>>>> Stashed changes



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
    

class PasswordResetAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            CustomUser = get_user_model()

            try:
                user = CustomUser.objects.get(email=email)
                current_site = get_current_site(request)
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = account_activation_token.make_token(user)

                # Debug-Ausgaben
                print(f"Email: {email}")
                print(f"User ID: {user.pk}")
                print(f"UIDB64: {uidb64}")
                print(f"Token: {token}")
                print(f"Domain: {current_site.domain}")

                mail_subject = 'Reset your password.'
                message = render_to_string('password_reset_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': uidb64,
                    'token': token,
                    'protocol': 'http'
                })
                email_message = EmailMessage(mail_subject, message, to=[user.email])
                email_message.content_subtype = "html"
                email_message.send()

                # Rückgabe der wichtigen Daten als Teil der JSON-Antwort
                return Response({
                    "message": "Password reset link sent.",
                    "email": email,
                    "user_id": user.pk,
                    "uidb64": uidb64,
                    "token": token,
                    "domain": current_site.domain
                }, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({"error": "User with this email does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 


# class CustomPasswordResetConfirmView(PasswordResetConfirmView):
#     template_name = 'password_reset_confirm.html'
    
#     def post(self, request, *args, **kwargs):
#         print("POST-Anfrage empfangen")
#         return super().post(request, *args, **kwargs)
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['uidb64'] = self.kwargs['uidb64']
#         context['token'] = self.kwargs['token']
#         return context

<<<<<<< Updated upstream
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['uidb64'] = self.kwargs.get('uidb64')
        context['token'] = self.kwargs.get('token')
        print(f"UIDB64 im Template: {context['uidb64']}")
        print(f"Token im Template: {context['token']}")
        return context

    def post(self, request, *args, **kwargs):
        print('post aufgerufen')
        uidb64 = self.kwargs.get('uidb64')
        token = self.kwargs.get('token')
        UserModel = get_user_model()

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = UserModel.objects.get(pk=uid)
            print(f'Benutzer gefunden: {user}')
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None
            print('Benutzer nicht gefunden oder ungültig')

        if user is not None and default_token_generator.check_token(user, token):
            print('Token ist gültig')
            form = SetPasswordForm(user, request.POST)
            print('Form erstellt:', form)

            if form.is_valid():
                form.save()  # Passwort speichern
                print('Passwort wurde erfolgreich geändert')
                return JsonResponse({'message': 'Password has been successfully reset.'}, status=200)
            else:
                print('Formular ungültig:', form.errors)  # Debugging-Ausgabe bei ungültigem Formular
                return JsonResponse({'errors': form.errors}, status=400)
        else:
            print('Ungültiger Token oder Benutzer')
            return JsonResponse({'error': 'The reset link is invalid or has expired.'}, status=400)

=======
#     def form_valid(self, form):
#         print("Form valid method called")
#         print("New password: ", form.cleaned_data['new_password1'])
#         user = form.save(commit=False)  # Save the form without committing to the database yet
#         user.set_password(form.cleaned_data['new_password1'])  # Set the new password
#         user.save()  # Save the user with the updated password
#         return super().form_valid(form)
# def reset_password(request, uidb64, token):
#     """
#     Reset the password after verifying the user and the token.
#     """
#     CustomUser = get_user_model()
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = CustomUser.objects.get(pk=uid)
#         print(f'Trying to reset password for UID: {uid}, User: {user}')
#     except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist) as e:
#         print(f'Error decoding UID or fetching user: {str(e)}')
#         user = None
    
#     if user is not None:
#         # Überprüfen Sie, ob der Token gültig ist
#         token_valid = default_token_generator.check_token(user, token)
#         print('user and token:',user, token)
#         print(f'Is the token valid?: {token_valid}')
        
#         if token_valid:
#             if request.method == 'POST':
#                 new_password1 = request.POST.get('new_password1')
#                 new_password2 = request.POST.get('new_password2')
                
#                 if new_password1 and new_password2:
#                     if new_password1 == new_password2:
#                         user.set_password(new_password1)
#                         user.save()
#                         print('Password successfully reset.')
#                         return redirect('http://localhost:4200/login')
#                     else:
#                         print('Passwords do not match.')
#                         return HttpResponseBadRequest('Passwords do not match.')
#                 else:
#                     print('Password fields cannot be empty.')
#                     return HttpResponseBadRequest('Password fields cannot be empty.')
#             else:
#                 print('Rendering password reset form.')
#                 return render(request, 'password_reset_form.html', {'uidb64': uidb64, 'token': token})
#         else:
#             print(f'Invalid token for user {user}')
#             return HttpResponseBadRequest('Invalid token or user does not exist.')
#     else:
#         print('User does not exist or UID is incorrect.')
#         return HttpResponseBadRequest('Invalid token or user does not exist.')
def reset_password(request, uidb64, token):
    CustomUser = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
        print(f'Trying to reset password for UID: {uid}, User: {user}')
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist) as e:
        print(f'Error decoding UID or fetching user: {str(e)}')
        user = None
    
    if user is not None:
        token = default_token_generator.make_token(user)
        token_valid = default_token_generator.check_token(user, token)
        print("Generated Token:", token)
        print("Token valid:", token_valid)


        print(f"Password hash: {user.password}")
        print(f"Last login: {user.last_login}")

        if token_valid:
            if request.method == 'POST':
                new_password1 = request.POST.get('new_password1')
                new_password2 = request.POST.get('new_password2')
                
                if new_password1 and new_password2:
                    if new_password1 == new_password2:
                        user.set_password(new_password1)
                        user.save()
                        print('Password successfully reset.')
                        return redirect('http://localhost:4200/login')
                    else:
                        print('Passwords do not match.')
                        return HttpResponseBadRequest('Passwords do not match.')
                else:
                    print('Password fields cannot be empty.')
                    return HttpResponseBadRequest('Password fields cannot be empty.')
            else:
                print('Rendering password reset form.')
                return render(request, 'password_reset_confirm.html', {'uidb64': uidb64, 'token': token})
        else:
            print(f'Invalid token for user {user}')
            return HttpResponseBadRequest('Invalid token or user does not exist.')
    else:
        print('User does not exist or UID is incorrect.')
        return HttpResponseBadRequest('Invalid token or user does not exist.')




    
class PasswordResetCompleteView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"message": "Password reset complete. You can now log in with your new password."}, status=status.HTTP_200_OK)
>>>>>>> Stashed changes

class CheckEmailView(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def create(self, request):
        email = request.data.get('email')
        CustomUser = get_user_model()
        if CustomUser.objects.filter(email=email).exists():
            return Response({'exists': True}, status=status.HTTP_200_OK)
        return Response({'exists': False}, status=status.HTTP_200_OK)

    

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
from Users.models import CustomUser
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
from rest_framework.exceptions import ValidationError


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

def activate(request, uidb64, token):
    """
        Forwarding after email activation
    """
    CustomUser = get_user_model()  
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        
        user_link = user.activation_url
        print('user_link: ',user_link)
        
        if "videoflix.aleksanderdemyanovych.de" in user_link:
            return redirect('https://videoflix.aleksanderdemyanovych.de/video_site')
        elif "videoflix.xn--bjrnteneicken-jmb.de" in user_link:
            return redirect('https://videoflix.xn--bjrnteneicken-jmb.de/video_site')
        else:
            return redirect('https://videoflix.aleksanderdemyanovych.de/video_site')

    else:
        if "videoflix.aleksanderdemyanovych.de" in user_link:
            return redirect('https://videoflix.aleksanderdemyanovych.de/login')
        elif "videoflix.xn--bjrnteneicken-jmb.de" in user_link:
            return redirect('https://videoflix.xn--bjrnteneicken-jmb.de/login')
        else:
            return redirect('https://videoflix.aleksanderdemyanovych.de/login')
        
        
class RegisterViewSet(viewsets.ViewSet):
    """
    This ViewSet handles user registration.
    
    Permissions:
    ------------
    - AllowAny: Allows any user to access the registration functionality.
    """
    permission_classes = (AllowAny,)

    def create(self, request):
        """
        Handles user registration and sends an activation email.
        
        Process:
        --------
        - Validates the user data.
        - Saves the user, but sets them as inactive initially.
        - Sends an email with an activation link to confirm the account.
        
        Returns:
        --------
        - On success: A message instructing the user to confirm their email.
        - On failure: Validation errors.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            
            current_site = get_current_site(request)
            activation_url = f"https://{current_site.domain}"
            user.activation_url = activation_url
            user.save()
            print('current user:', user)
            print(f"Activation URL: {activation_url}")
            mail_subject = 'Activate your account.'
            message = render_to_string('templates_activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'protocol': 'https'
            })
            to_email = serializer.validated_data.get('email')
            print('send to_email:', to_email)
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
    Handles user login and returns an authentication token.
    
    Permissions:
    ------------
    - AllowAny: Allows any user to access the login functionality.
    """
    def create(self, request, *args, **kwargs):
        """
        Processes user login.
        
        Process:
        --------
        - Validates the user credentials.
        - If the user is inactive, returns an error message.
        - If login is successful, returns the user's token and profile information.
        
        Returns:
        --------
        - On success: The user's token, ID, and email.
        - On failure: An error message indicating an inactive account or invalid credentials.
        """
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
    """
    Handles verification of authentication tokens.
    
    Permissions:
    ------------
    - AllowAny: Allows any user to verify their token.
    """
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        """
        Verifies a provided authentication token against the user.

        Process:
        --------
        - Takes a token and user_id from the request.
        - Validates that the token belongs to the user and the user is active.
        
        Returns:
        --------
        - On success: The user's token, ID, and email.
        - On failure: An error message indicating an invalid token or user.
        """
        token_key = request.data.get('token')
        user_id = request.data.get('user_id')

        if not token_key or not user_id:
            return Response({'error': 'Missing Token or user_id.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = Token.objects.get(key=token_key)
            CustomUser = get_user_model()
            user_id = int(user_id)
            user = CustomUser.objects.get(pk=user_id)

            if token.user == user and user.is_active:
                return Response({
                    'token': token.key,
                    'user_id': user.pk,
                    'email': user.email
                })

            return Response({'error': 'Token and user do not match or user is not active.'},
                            status=status.HTTP_400_BAD_REQUEST)

        except Token.DoesNotExist:
            return Response({'error': 'Invalid Token.'}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'error': 'Invalid user_id.'}, status=status.HTTP_400_BAD_REQUEST)



class LogoutViewSet(viewsets.ViewSet):
    """
    Handles user logout.
    
    Permissions:
    ------------
    - No specific permission required; logs out the authenticated user.
    """
    def create(self, request, *args, **kwargs):
        """
        Logs out the user.
        
        Returns:
        --------
        - A success message confirming that the user has been logged out.
        """
        logout(request)
        return Response({'message': 'Logout successful'})
    

class CheckEmailView(viewsets.ViewSet):
    """
    Checks if an email is already registered in the system.
    
    Permissions:
    ------------
    - AllowAny: Allows any user to check if an email exists.
    """
    permission_classes = (AllowAny,)

    def create(self, request):
        """
        Verifies if the provided email is already registered.

        Process:
        --------
        - Takes the email from the request.
        - Checks if a user with this email exists in the system.

        Returns:
        --------
        - True if the email exists, False otherwise.
        """
        email = request.data.get('email')
        print('email:',email)
        if not email:
            print('email not found:',email)
            raise ValidationError({'error': 'Email is required.'})
        
        CustomUser = get_user_model()
        if CustomUser.objects.filter(email=email).exists():
            print('email found:',email)
            return Response({'exists': True}, status=status.HTTP_200_OK)
        return Response({'exists': False}, status=status.HTTP_200_OK)

    
class PasswordResetAPIView(APIView):
    """
    Handles password reset requests.

    Permissions:
    ------------
    - AllowAny: Allows any user to request a password reset.
    """
    permission_classes = [AllowAny] 
    def post(self, request, *args, **kwargs):
        """
        Sends a password reset email to the user.
        
        Process:
        --------
        - Validates the user's request.
        - Sends a password reset email if the validation is successful.

        Returns:
        --------
        - A success message indicating that the email has been sent.
        """
        serializer = PasswordResetSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password reset e-mail has been sent."}, status=status.HTTP_200_OK)

User = get_user_model()
class PasswordResetConfirmAPIView(APIView):
    """
    Handles confirmation of password reset.

    Permissions:
    ------------
    - AllowAny: Allows any user to confirm their password reset.
    """
    permission_classes = [AllowAny] 
    def post(self, request, *args, **kwargs):
        """
        Confirms the password reset using a token and user ID.

        Process:
        --------
        - Takes a token and user ID from the request.
        - Verifies the validity of the token and resets the password if valid.

        Returns:
        --------
        - A success message if the password has been reset.
        - An error message if the token or user is invalid.
        """
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
    """
    Provides access to user data for authenticated users.

    Permissions:
    ------------
    - IsAuthenticated: Only authenticated users can access this view.
    """
    permission_classes = (IsAuthenticated,) 
    serializer_class = UserSerializer

    def get_queryset(self):
        """
        Filters the queryset to return only the authenticated user's data.
        """
        User = get_user_model()
        return User.objects.filter(pk=self.request.user.pk)

    @action(detail=False, methods=['get'], url_path='user-data')
    def get_user_data(self, request):
        """
        Fetches the authenticated user's data.

        Returns:
        --------
        - The user's profile data if found.
        - An error message if the user is not found.
        """
        queryset = self.get_queryset()
    
        if not queryset.exists():
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(queryset.first())
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class UpdateUserDataViewSet(viewsets.ModelViewSet):
    """
    Handles updates to the authenticated user's profile.

    Permissions:
    ------------
    - IsAuthenticated: Only authenticated users can update their profile.
    """
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        """
        Updates the authenticated user's profile.

        Process:
        --------
        - Validates that the user making the request is the profile owner.
        - Partially updates the user's profile data.

        Returns:
        --------
        - The updated user data on success.
        - An error message if the user does not have permission to update the profile.
        """
        partial = kwargs.pop('partial', True) 
        instance = self.get_object()

        if instance.id != request.user.id:
            return Response({'detail': 'You do not have permission to perform this action.'}, status=403)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)
        return Response(serializer.data)

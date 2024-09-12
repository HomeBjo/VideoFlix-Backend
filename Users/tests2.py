
from django.test import RequestFactory, TestCase
from .models import CustomUser
from rest_framework.test import APITestCase
from django.urls import NoReverseMatch, reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.core import mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from Users.views import activate
from Users.tokens import account_activation_token
from urllib.parse import urlparse
from unittest.mock import patch
from django.contrib.auth.tokens import default_token_generator
from rest_framework.test import APIClient

#----------------------- User-Viwes Test -----------------------

class UserRegistrationTest(APITestCase):
    def test_user_registration(self):
        url = reverse('Users:register-list')
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword123',
            'first_name': 'Test',
            'last_name': 'User',
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        user = CustomUser.objects.get(username='testuser')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertFalse(user.is_active)

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Activate your account', mail.outbox[0].subject)
        self.assertIn('testuser@example.com', mail.outbox[0].to)

        

class ActivateUserTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123',
            is_active=False
        )
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = account_activation_token.make_token(self.user)

    def test_activate_success(self):
        """Test successful account activation."""
        request = self.factory.get(reverse('activate', kwargs={'uidb64': self.uid, 'token': self.token}))
        response = activate(request, uidb64=self.uid, token=self.token)
        
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
        self.assertEqual(response.status_code, 302)
        
        parsed_url = urlparse(response.url)
        self.assertEqual(parsed_url.path, '/video_site')
        
        

    def test_activate_invalid_token(self):
        invalid_token = 'invalid-token'
        request = self.factory.get(reverse('activate', kwargs={'uidb64': self.uid, 'token': invalid_token}))
        response = activate(request, uidb64=self.uid, token=invalid_token)

        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        self.assertEqual(response.status_code, 302)
        parsed_url = urlparse(response.url)
        self.assertEqual(parsed_url.path, '/login')

    def test_activate_invalid_uid(self):
        invalid_uid = urlsafe_base64_encode(force_bytes(99999))
        request = self.factory.get(reverse('activate', kwargs={'uidb64': invalid_uid, 'token': self.token}))
        response = activate(request, uidb64=invalid_uid, token=self.token)

        parsed_url = urlparse(response.url)
        self.assertEqual(parsed_url.path, '/login')

    def test_activate_user_does_not_exist(self):
        self.user.delete()
        request = self.factory.get(reverse('activate', kwargs={'uidb64': self.uid, 'token': self.token}))
        response = activate(request, uidb64=self.uid, token=self.token)

        parsed_url = urlparse(response.url)
        self.assertEqual(parsed_url.path, '/login')

    @patch('Users.views.account_activation_token.check_token')
    def test_activate_token_fails(self, mock_check_token):
        mock_check_token.return_value = False
        request = self.factory.get(reverse('activate', kwargs={'uidb64': self.uid, 'token': self.token}))
        response = activate(request, uidb64=self.uid, token=self.token)

        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        parsed_url = urlparse(response.url)
        self.assertEqual(parsed_url.path, '/login')
        
        
class UserLoginTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='testuser@example.com', password='testpassword123')
        self.url = reverse('Users:login-list')
        
    def test_user_login(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword123',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['user_id'], self.user.id)
        self.assertEqual(response.data['email'], self.user.email)


class TokenVerificationViewSetTest(APITestCase):
    
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123'
        )
        self.token = Token.objects.create(user=self.user)
        self.valid_data = {
            'token': self.token.key,
            'user_id': self.user.pk
        }
        try:
            self.url = reverse('Users:verify-token-list')
            print(self.url)
        except NoReverseMatch:
            print("URL-Name nicht gefunden.")
    
    
    def test_token_verification_success(self):
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], self.token.key)
        self.assertEqual(response.data['user_id'], self.user.pk)
        self.assertEqual(response.data['email'], self.user.email)
    
    
    def test_missing_token(self):
        data = {'user_id': self.user.pk}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Missing Token or user_id.')
    
    
    def test_missing_user_id(self):
        data = {'token': self.token.key}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Missing Token or user_id.')

    @patch('rest_framework.authtoken.models.Token.objects.get')
    def test_invalid_token(self, mock_get):
        mock_get.side_effect = Token.DoesNotExist
        data = {'token': 'invalid_token', 'user_id': self.user.pk}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid Token.')


    def test_invalid_user_id(self):
        data = {'token': self.token.key, 'user_id': 'invalid_user_id'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid user_id.')


    def test_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Token and user do not match or user is not active.')
        
        
class UserLogoutTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='testuser@example.com', password='testpassword123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('Users:logout-list')
        
        
    def test_user_logout(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Logout successful')
        
        
        
class CheckEmailViewTest(APITestCase):
    
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123'
        )
        self.url = reverse('Users:check-email-list')

    def test_check_email_exists(self):
        response = self.client.post(self.url, {'email': 'testuser@example.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['exists'], True)


    def test_check_email_does_not_exist(self):
        response = self.client.post(self.url, {'email': 'nonexistent@example.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['exists'], False)


    def test_missing_email(self):
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Email is required.')
           

class PasswordResetConfirmAPIViewTest(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123'
        )
        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = default_token_generator.make_token(self.user)
        self.url = f'/password_reset/confirm/{self.uidb64}/{self.token}/'

    @patch('django.contrib.auth.tokens.default_token_generator.check_token')
    def test_password_reset_confirm_success(self, mock_check_token):
        mock_check_token.return_value = True
        data = {'new_password1': 'newpassword123', 'new_password2': 'newpassword123'}
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Password has been reset.')
        user = CustomUser.objects.get(email='testuser@example.com')
        self.assertTrue(user.check_password('newpassword123'))


    @patch('django.contrib.auth.tokens.default_token_generator.check_token')
    def test_password_reset_confirm_invalid_token(self, mock_check_token):
        mock_check_token.return_value = False
        data = {'new_password1': 'newpassword123', 'new_password2': 'newpassword123'}
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Invalid token or user.')


    def test_password_reset_confirm_invalid_user(self):
        invalid_uidb64 = urlsafe_base64_encode(force_bytes(99999))
        url = f'/password_reset/confirm/{invalid_uidb64}/{self.token}/'
        data = {'new_password1': 'newpassword123', 'new_password2': 'newpassword123'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Invalid token or user.')


    def test_missing_password(self):
        data = {}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('new_password1', response.data)
        self.assertEqual(response.data['new_password1'][0], 'This field is required.')
        self.assertIn('new_password2', response.data)
        self.assertEqual(response.data['new_password2'][0], 'This field is required.')
        

class UpdateUserDataViewSetTest(APITestCase):
    
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('Users:update-user-data-detail', args=[self.user.pk])


    def test_update_user_data_success(self):
        data = {
            'username': 'updateduser',
            'email': 'updateduser@example.com',
        }
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'updateduser')
        self.assertEqual(response.data['email'], 'updateduser@example.com')


    def test_update_user_data_not_authenticated(self):
        self.client.credentials()
        data = {
            'username': 'updateduser',
            'email': 'updateduser@example.com',
        }
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')


    def test_update_user_data_no_permission(self):
        other_user = CustomUser.objects.create_user(
            username='otheruser',
            email='otheruser@example.com',
            password='otherpassword123'
        )
        other_token = Token.objects.create(user=other_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + other_token.key)
        
        data = {
            'username': 'updateduser',
            'email': 'updateduser@example.com',
        }
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'You do not have permission to perform this action.')



    def test_update_user_data_invalid_data(self):
        data = {
            'email': 'invalidemail'
        }
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        
        
        
class UserDataViewSetTests(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        User = CustomUser
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='testuser@example.com'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('Users:user-data-list')
    
    
    def test_authenticated_user_can_get_own_data(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user_data = response.data[0] 
        self.assertEqual(user_data['id'], self.user.pk)
        self.assertEqual(user_data['email'], self.user.email)
        
    def test_unauthenticated_user_cannot_get_user_data(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_user_data_not_found(self):
        url_with_invalid_id = reverse('Users:user-data-detail', kwargs={'pk': 9999})
        response = self.client.get(url_with_invalid_id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_user_data_serialization(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user_data = response.data[0] 
        self.assertIn('username', user_data)
        self.assertIn('email', user_data)
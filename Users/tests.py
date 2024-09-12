from django.db import IntegrityError
from django.test import RequestFactory, TestCase
from Users.serializers import EmailAuthTokenSerializer, PasswordResetConfirmSerializer, PasswordResetSerializer, UserSerializer
from .models import CustomUser
from django.contrib.auth.hashers import check_password
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token


#----------------------- User-Model Test -----------------------
class CustomUserModelTests(TestCase):

    def test_create_user(self):
        user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            custom='Custom Field Value',
            address='123 Test St, Test City',
            phone='+1234567890'
        )
        
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertTrue(user.check_password('password123'))
        self.assertEqual(user.custom, 'Custom Field Value')
        self.assertEqual(user.address, '123 Test St, Test City')
        self.assertEqual(user.phone, '+1234567890')
        
        
    def test_create_user_without_email(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(email='', password='password123')
            
            
    def test_create_superuser(self):
        superuser = CustomUser.objects.create_superuser(
            email='superuser@example.com',
            password='superpassword123',
        )
        
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
        self.assertEqual(superuser.email, 'superuser@example.com')
        self.assertTrue(superuser.check_password('superpassword123'))
        
        
    def test_email_unique(self):
        CustomUser.objects.create_user(
            email='unique@example.com',
            password='password123'
        )
        
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create_user(
                email='unique@example.com',
                password='password456'
            )
       
       
    def test_password_is_hashed(self):
        user = CustomUser.objects.create_user(
            email='passwordhashuser@example.com',
            password='password123'
        )
        
        self.assertNotEqual(user.password, 'password123')
        self.assertTrue(user.check_password('password123'))
        
        
#----------------------- User-Serializer Test -----------------------

class UserSerializerTest(TestCase):

    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'email': 'testuser@example.com',
            'first_name': 'firstnameTest',
            'last_name': 'lastnameTest',
        }


    def test_valid_user_serializer(self):
        serializer = UserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        
       
        self.assertEqual(user.username, self.user_data['username'])
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])
        self.assertTrue(check_password(self.user_data['password'], user.password))
        self.assertEqual(CustomUser.objects.count(), 1)


    def test_user_serializer_invalid_data(self):
        invalid_data = {
            'email': '',
            'password': 'testpassword123',
            'first_name': 'firstnameTest',
            'last_name': 'lastnameTest',
        }
        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    
    def test_user_update_serializer(self):
        user = CustomUser.objects.create_user(**self.user_data)
        update_data = {
            'username': 'newusername',
            'password': 'newpassword123',
            'email': 'newuser@example.com',
            'first_name': 'newfirstnameTest',
            'last_name': 'newlastnameTest',
        }
        
        serializer = UserSerializer(user, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()
        
        self.assertEqual(updated_user.first_name, 'newfirstnameTest')
        self.assertEqual(updated_user.last_name, 'newlastnameTest')
        self.assertEqual(updated_user.email, 'newuser@example.com')
        self.assertEqual(updated_user.username, 'newusername')
        
        
    def test_missing_required_fiels(self):
        required_data = {
            'email': '',
            'password': 'testpassword123',
        }
        
        serializer = UserSerializer(data=required_data)
        self.assertFalse(serializer.is_valid())   
        self.assertIn('email', serializer.errors)
        
    def test_password_write_only(self):
        user = CustomUser.objects.create_user(**self.user_data)
        serializer = UserSerializer(user)
        
        if 'password' in serializer.data:
            self.assertTrue(serializer.data['password'].startswith('pbkdf2_sha256$'))

    
    def test_favorite_videos_read_only(self):
        user = CustomUser.objects.create_user(**self.user_data)
        data = self.user_data.copy()
        data['favorite_videos'] = [1, 2, 3] 
        serializer = UserSerializer(user, data=data)
        self.assertTrue(serializer.is_valid())
        self.assertNotIn('favorite_videos', serializer.validated_data)
        
        
    def test_invalid_email_format(self):
        invalid_data = self.user_data.copy()
        invalid_data['email'] = 'notanemail'
        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)


    def test_email_auth_token_serializer(self):
        user = CustomUser.objects.create_user(**self.user_data)
        data = {
            'email': self.user_data['email'],
            'password': self.user_data['password'],
        }
        
        serializer = EmailAuthTokenSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['user'], user)
        
    
    def test_password_reset_serializer(self):
        user = CustomUser.objects.create_user(**self.user_data)
        request = RequestFactory().post('/api/password-reset/', {'email': user.email})
        serializer = PasswordResetSerializer(data={'email': user.email}, context={'request': request})
        self.assertTrue(serializer.is_valid())
        serializer.save()
        
        
    def test_password_reset_confirm_serializer(self):
        user = CustomUser.objects.create_user(**self.user_data)
        serializer = PasswordResetConfirmSerializer(data= {
            'new_password1': 'newpassword123', 
            'new_password2': 'newpassword123'}, context={'user': user})
        
        self.assertTrue(serializer.is_valid())
        serializer.save(user=user)
        self.assertTrue(user.check_password('newpassword123'))
        
        
# #----------------------- User-Viwes Test -----------------------

# class UserRegistrationTest(APITestCase):
#     def test_user_registration(self):
#         url = reverse('Users:register-list')
#         data = {
#             'username': 'testuser',
#             'email': 'testuser@example.com',
#             'password': 'testpassword123',
#         }
        
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertIn('token', response.data)
#         self.assertEqual(response.data['user_id'], CustomUser.objects.get(username='testuser').id)
#         self.assertEqual(response.data['email'], 'testuser@example.com')

# class UserLoginTest(APITestCase):
#     def setUp(self):
#         self.user = CustomUser.objects.create_user(username='testuser', password='testpassword123')
#         self.url = reverse('Users:login-list')
        
#     def test_user_login(self):
#         data = {
#             'username': 'testuser',
#             'password': 'testpassword123',
#         }
#         response = self.client.post(self.url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn('token', response.data)
#         self.assertEqual(response.data['user_id'], self.user.id)
#         self.assertEqual(response.data['email'], self.user.email)

# class UserLogoutTest(APITestCase):
#     def setUp(self):
#         self.user = CustomUser.objects.create_user(username='testuser', password='testpassword123')
#         self.token = Token.objects.create(user=self.user)
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
#         self.url = reverse('Users:logout-list')
        
#     def test_user_logout(self):
#         response = self.client.post(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['message'], 'Logout successful')
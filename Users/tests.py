from django.test import TestCase
from Users.serializers import UserSerializer
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
        
        
#----------------------- User-Serializer Test -----------------------

class UserSerializerTest(TestCase):

    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'email': 'testuser@example.com'
        }

    def test_valid_user_serializer(self):
        serializer = UserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        
       
        self.assertEqual(user.username, self.user_data['username'])
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(check_password(self.user_data['password'], user.password))
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_user_serializer_invalid_data(self):
        invalid_data = {
            'username': '',
            'password': 'testpassword123',
            'email': 'testuser@example.com'
        }
        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)

    def test_password_write_only(self):
        user = CustomUser.objects.create_user(**self.user_data)
        serializer = UserSerializer(user)
        self.assertNotIn('password', serializer.data)
    
    def test_favorite_videos_read_only(self):
        user = CustomUser.objects.create_user(**self.user_data)
        data = self.user_data.copy()
        data['favorite_videos'] = [1, 2, 3] 
        serializer = UserSerializer(user, data=data)
        self.assertTrue(serializer.is_valid())
        self.assertNotIn('favorite_videos', serializer.validated_data)
        
        
#----------------------- User-Viwes Test -----------------------

class UserRegistrationTest(APITestCase):
    def test_user_registration(self):
        url = reverse('Users:register-list')
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword123',
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['user_id'], CustomUser.objects.get(username='testuser').id)
        self.assertEqual(response.data['email'], 'testuser@example.com')

class UserLoginTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword123')
        self.url = reverse('Users:login-list')
        
    def test_user_login(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword123',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['user_id'], self.user.id)
        self.assertEqual(response.data['email'], self.user.email)

class UserLogoutTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('Users:logout-list')
        
    def test_user_logout(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Logout successful')
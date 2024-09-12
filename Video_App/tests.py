from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Video, FavoriteVideo
from Users.models import CustomUser

class VideoViewSetTest(APITestCase):
    
    def setUp(self):
       
        self.user = CustomUser.objects.create_user(username='testuser', email='test@test.de', password='password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)  
        
      
        self.video_file = SimpleUploadedFile("video1.mp4", b"file_content", content_type="video/mp4")
        
       
        self.video1 = Video.objects.create(title='Test Video 1', category='Music', video_file=self.video_file)
        self.video2 = Video.objects.create(title='Test Video 2', category='Movie', video_file=self.video_file)
        
    def test_get_videos(self):
        """
        Testet das Abrufen aller Videos.
        """
        url = '/videos/get_videos/'  
        response = self.client.get(url)
        
        print(f"Anzahl der Videos in der Antwort: {len(response.data)}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  

    def test_favorites(self):
        """
        Testet das Favorisieren eines Videos.
        """
        
        FavoriteVideo.objects.create(user=self.user, video=self.video1)
        
        url = '/videos/get_videos/favorites/' 
        response = self.client.get(url)
        
        print(f"Anzahl der Videos in der Antwort: {len(response.data)}")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  

    def test_toggle_favorite(self):
        """
        Testet das Hinzufügen und Entfernen eines Videos zu den Favoriten.
        """
        url = '/videos/get_videos/toggle_favorite/'  
        data = {'fav_video': self.video1.id} 
        
        print(f"11111111",data )
    
      
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
        
        self.assertTrue(FavoriteVideo.objects.filter(user=self.user, video=self.video1).exists())
    
       
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
        
        self.assertFalse(FavoriteVideo.objects.filter(user=self.user, video=self.video1).exists())
        
    def test_category_videos(self):
        """
        Testet das Abrufen von Videos, die nach Kategorie gefiltert sind.
        """
        url = f'/videos/get_videos/category/{self.video1.category}/'  
        response = self.client.get(url)
    
       
        print(f"22222222 categroy '{self.video1.category}': {response.data}")
    
        self.assertEqual(response.status_code, status.HTTP_200_OK)
       
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.video1.title)        
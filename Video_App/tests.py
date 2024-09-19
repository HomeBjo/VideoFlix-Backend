from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Video, FavoriteVideo
from Users.models import CustomUser

class VideoViewSetTest(APITestCase):
    
    def setUp(self):
        # Set up einen Test-User und Videos für den Test
        self.user = CustomUser.objects.create_user(username='testuser', email='test@test.de', password='password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)  # Nutzer authentifizieren
        
        # Verwende SimpleUploadedFile um eine Testdatei zu simulieren
        self.video_file = SimpleUploadedFile("video1.mp4", b"file_content", content_type="video/mp4")
        
        # Erstelle ein paar Test-Videos
        self.video1 = Video.objects.create(title='Test Video 1', category='Music', video_file=self.video_file)
        self.video2 = Video.objects.create(title='Test Video 2', category='Movie', video_file=self.video_file)
        
    def test_get_videos(self):
        """
        Testet das Abrufen aller Videos.
        """
        url = '/videos/get_videos/'  # Direkte URL als String
        response = self.client.get(url)
        
        print(f"Anzahl der Videos in der Antwort: {len(response.data)}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Wir haben 2 Videos erstellt

    def test_favorites(self):
        """
        Testet das Favorisieren eines Videos.
        """
        # Erst füge ein Video zu den Favoriten hinzu
        FavoriteVideo.objects.create(user=self.user, video=self.video1)
        
        url = '/videos/get_videos/favorites/'  # Direkte URL als String
        response = self.client.get(url)
        
        print(f"Anzahl der Videos in der Antwort: {len(response.data)}")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Wir haben nur ein Favoriten-Video

    def test_toggle_favorite(self):
        """
        Testet das Hinzufügen und Entfernen eines Videos zu den Favoriten.
        """
        url = '/videos/get_videos/toggle_favorite/'  # Direkte URL als String
        data = {'fav_video': self.video1.id}  # Verwende das korrekte Feld 'fav_videos'
        
        print(f"11111111",data )
    
        # Füge das Video zu den Favoriten hinzu
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
        # Stelle sicher, dass das Video zu den Favoriten hinzugefügt wurde
        self.assertTrue(FavoriteVideo.objects.filter(user=self.user, video=self.video1).exists())
    
        # Entferne das Video aus den Favoriten
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
        # Stelle sicher, dass das Video entfernt wurde
        self.assertFalse(FavoriteVideo.objects.filter(user=self.user, video=self.video1).exists())
        
    def test_category_videos(self):
        """
        Testet das Abrufen von Videos, die nach Kategorie gefiltert sind.
        """
        url = f'/videos/get_videos/category/{self.video1.category}/'  # Direkte URL als String mit Kategorie
        response = self.client.get(url)
    
        # Ausgabe der Antwort, um zu prüfen, ob sie korrekt ist (optional)
        print(f"22222222 categroy '{self.video1.category}': {response.data}")
    
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Stelle sicher, dass nur ein Video mit der entsprechenden Kategorie zurückgegeben wird
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.video1.title)        
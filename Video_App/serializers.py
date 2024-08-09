
import os
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Video, FavoriteVideo

# class VideoSerializer(serializers.ModelSerializer):
#     is_favorite = serializers.SerializerMethodField()
#     class Meta:
#         model = Video
#         fields = '__all__'
        
        
#     def get_is_favorite(self, obj):
#         user = self.context['request'].user
#         if user.is_authenticated:
#             return FavoriteVideo.objects.filter(user=user, video=obj).exists()
#         return False


class VideoSerializer(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField()
    video_folder = serializers.SerializerMethodField()
    screenshot = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['id', 'is_favorite', 'title', 'url', 'created_at', 'description', 'video_folder', 'screenshot', 'category']

    def get_is_favorite(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return FavoriteVideo.objects.filter(user=user, video=obj).exists()
        return False

    def get_video_folder(self, obj):
      if obj.video_file:
        # Extrahiere den Ordnerpfad ohne den Dateinamen
        video_folder = os.path.dirname(obj.video_file.url)
    
        # Extrahiere den Basename der Videodatei ohne Erweiterung
        base_name = os.path.splitext(os.path.basename(obj.video_file.url))[0]
        
        # Kombiniere den Pfad, um den spezifischen Ordner mit dem Videonamen zu erstellen
        video_folder = os.path.join(video_folder, base_name).replace(f'/{base_name}/{base_name}', f'/{base_name}', 1).replace('\\', '/')
        print(f"Video folder: {video_folder}")
        return video_folder.replace('/videos/videos/', '/videos/')
      return None

    def get_screenshot(self, obj):
        if obj.video_file:
            # Extrahiere den Dateinamen ohne die Erweiterung
            base_name = os.path.splitext(os.path.basename(obj.video_file.url))[0]
            video_folder = self.get_video_folder(obj).replace('\\', '/')  # Stelle sicher, dass nur Forward Slashes verwendet werden'
            # Setze den Screenshot-Pfad zusammen
            screenshot_path = f"{video_folder}/{base_name}_screenshot.png"
            print(f"Screenshot path: {screenshot_path}")  # Debug-Ausgabe
            
            # Erstelle den vollständigen Screenshot-Pfad
            full_screenshot_path = os.path.join(obj.video_file.storage.location, screenshot_path.lstrip('/')).replace('\\', '/')
            
            # Entferne doppeltes 'media' im full_screenshot_path
            full_screenshot_path = full_screenshot_path.replace('/media/media', '/media', 1).replace(f'/{base_name}/{base_name}', f'/{base_name}', 1)
    
            print(f"Full screenshot path: {full_screenshot_path}")  # Debug-Ausgabe
            
            if os.path.exists(full_screenshot_path):
                return screenshot_path
    
        return None


       
    
    
    
    
    
    
    
    
class FavoriteVideoSerializer(serializers.Serializer):
    fav_videos = serializers.ListField(
        child=serializers.IntegerField()
    )

    def update(self, instance, validated_data):
        fav_videos = validated_data['fav_videos']
        user = instance

        existing_favorites = set(FavoriteVideo.objects.filter(user=user).values_list('video_id', flat=True))

        for video_id in fav_videos:
            video = get_object_or_404(Video, id=video_id)
            if video_id in existing_favorites:
                FavoriteVideo.objects.filter(user=user, video=video).delete()
                existing_favorites.remove(video_id)
            else:
                FavoriteVideo.objects.create(user=user, video=video)
                existing_favorites.add(video_id)

        return user

    def to_representation(self, instance):
        user = instance
        favorite_videos = FavoriteVideo.objects.filter(user=user).values_list('video_id', flat=True)
        return {'fav_videos': list(favorite_videos)}
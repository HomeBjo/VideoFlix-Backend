
import os
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Video, FavoriteVideo


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
# also hier wird über serializer und dann das object mit den pfad über eine get anfrage wieder gegeben
    def get_video_folder(self, obj):
        request = self.context.get('request')
        if obj.video_file:
            video_folder = os.path.dirname(obj.video_file.url)
            base_name = os.path.splitext(os.path.basename(obj.video_file.url))[0]
            video_folder = os.path.join(video_folder, base_name+'_master.m3u8').replace(f'/{base_name}/{base_name}', f'/{base_name}', 1).replace('\\', '/')
            
            full_url = request.build_absolute_uri(video_folder.replace('/videos/videos/', '/videos/'))
            return full_url
        return None

    def get_screenshot(self, obj):
        request = self.context.get('request')
        if obj.video_file:
            base_name = os.path.splitext(os.path.basename(obj.video_file.url))[0]
            video_folder = self.get_video_folder(obj).replace('_master.m3u8', '').replace(f'/{base_name}/{base_name}', f'/{base_name}', 1)
            screenshot_path = f"{video_folder}/{base_name}_screenshot.png"

            full_url = request.build_absolute_uri(screenshot_path)
            return full_url
    
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
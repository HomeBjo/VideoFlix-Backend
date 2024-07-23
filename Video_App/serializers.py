from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Video, FavoriteVideo

class VideoSerializer(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField()
    class Meta:
        model = Video
        fields = '__all__'
        
        
    def get_is_favorite(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return FavoriteVideo.objects.filter(user=user, video=obj).exists()
        return False
    
    
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
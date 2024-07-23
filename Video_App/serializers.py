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
        # Entferne bestehende Favoriten
        FavoriteVideo.objects.filter(user=user).delete()
        # Füge neue Favoriten hinzu
        for video_id in fav_videos:
            video = Video.objects.get(id=video_id)
            FavoriteVideo.objects.create(user=user, video=video)
        return user
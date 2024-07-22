from rest_framework import serializers
from .models import Video, FavoriteVideo

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'
        
        
    def get_is_favorite(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return FavoriteVideo.objects.filter(user=user, video=obj).exists()
        return False

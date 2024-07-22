from rest_framework import serializers
from Users.models import CustomUser
from Video_App.serializers import VideoSerializer

class UserSerializer(serializers.ModelSerializer):
    favorite_videos = VideoSerializer(many=True, read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'email', 'favorite_videos')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
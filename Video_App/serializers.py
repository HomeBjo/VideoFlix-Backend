
import os
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Video, FavoriteVideo


class VideoSerializer(serializers.ModelSerializer):
    """
    Serializer for the Video model.

    This serializer provides fields for displaying video details, including whether the video is marked as a favorite by the current user, 
    the video's folder location, and a screenshot URL.

    Fields:
    -------
    - id (IntegerField): The unique ID of the video.
    - is_favorite (BooleanField): A boolean indicating whether the current user has favorited the video.
    - title (CharField): The title of the video.
    - url (URLField): The URL of the video.
    - created_at (DateField): The date the video was created.
    - description (CharField): A short description of the video.
    - video_folder (CharField): The folder URL where the video file is stored.
    - screenshot (CharField): The URL for the video's screenshot or thumbnail.
    - category (CharField): The category of the video.

    Methods:
    --------
    - get_is_favorite(obj):
        Determines if the current user has favorited the video.

    - get_video_folder(obj):
        Returns the absolute URL of the folder containing the video file.

    - get_screenshot(obj):
        Returns the absolute URL of the video's screenshot image.
    """
    is_favorite = serializers.SerializerMethodField()
    video_folder = serializers.SerializerMethodField()
    screenshot = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['id', 'is_favorite', 'title', 'url', 'created_at', 'description', 'video_folder', 'screenshot', 'category']

    def get_is_favorite(self, obj):
        """
        Checks if the current user has marked the video as a favorite.

        Args:
        -----
        obj (Video): The video object.

        Returns:
        --------
        bool: True if the current user has favorited the video, False otherwise.
        """
        user = self.context['request'].user
        if user.is_authenticated:
            return FavoriteVideo.objects.filter(user=user, video=obj).exists()
        return False

    def get_video_folder(self, obj):
        """
        Retrieves the URL of the folder containing the video file.

        Args:
        -----
        obj (Video): The video object.

        Returns:
        --------
        str: The absolute URL of the folder containing the video file, or None if no video file exists.
        """
        request = self.context.get('request')
        if obj.video_file:
            video_folder = os.path.dirname(obj.video_file.url)
            base_name = os.path.splitext(os.path.basename(obj.video_file.url))[0]
            video_folder = os.path.join(video_folder, base_name+'_master.m3u8').replace(f'/{base_name}/{base_name}', f'/{base_name}', 1).replace('\\', '/')
            
            full_url = request.build_absolute_uri(video_folder.replace('/videos/videos/', '/videos/'))
            return full_url
        return None

    def get_screenshot(self, obj):
        """
        Retrieves the URL of the video's screenshot.

        Args:
        -----
        obj (Video): The video object.

        Returns:
        --------
        str: The absolute URL of the screenshot image, or None if no video file exists.
        """
        request = self.context.get('request')
        if obj.video_file:
            base_name = os.path.splitext(os.path.basename(obj.video_file.url))[0]
            video_folder = self.get_video_folder(obj).replace('_master.m3u8', '').replace(f'/{base_name}/{base_name}', f'/{base_name}', 1)
            screenshot_path = f"{video_folder}/{base_name}_screenshot.png"

            full_url = request.build_absolute_uri(screenshot_path)
            return full_url
    
        return None


class FavoriteVideoSerializer(serializers.Serializer):
    """
    Serializer for handling favorite video actions.

    This serializer allows users to add or remove videos from their list of favorites by specifying a video ID.

    Fields:
    -------
    - fav_video (IntegerField): The ID of the video to be favorited or unfavorited.

    Methods:
    --------
    - update(instance, validated_data):
        Toggles the favorite status of a video for the current user.

    - to_representation(instance):
        Returns a list of the current user's favorite videos.
    """
    fav_video = serializers.IntegerField()

    def update(self, instance, validated_data):
        """
        Toggles the favorite status of a video for the current user.

        Args:
        -----
        instance (CustomUser): The user instance.
        validated_data (dict): The validated data containing the video ID.

        Returns:
        --------
        CustomUser: The updated user instance.
        """
        video_id = validated_data['fav_video']
        user = instance

        existing_favorites = set(FavoriteVideo.objects.filter(user=user).values_list('video_id', flat=True))

        video = get_object_or_404(Video, id=video_id)
        if video_id in existing_favorites:
            FavoriteVideo.objects.filter(user=user, video=video).delete()
            existing_favorites.remove(video_id)
        else:
            FavoriteVideo.objects.create(user=user, video=video)
            existing_favorites.add(video_id)

        return user

    def to_representation(self, instance):
        """
        Returns a list of the user's favorite video IDs.

        Args:
        -----
        instance (CustomUser): The user instance.

        Returns:
        --------
        dict: A dictionary containing a list of favorite video IDs.
        """
        user = instance
        favorite_videos = FavoriteVideo.objects.filter(user=user).values_list('video_id', flat=True)
        return {'fav_videos': list(favorite_videos)}

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
    image  = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['id', 'is_favorite', 'title', 'url', 'created_at', 'description', 'video_folder', 'category', 'image']

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
            video_folder = os.path.join(video_folder, base_name + '_master.m3u8').replace('\\', '/')
            
            full_url = request.build_absolute_uri(video_folder.replace('/videos/videos/', '/videos/'))
            print(f"Generated video folder URL: {full_url}")
            return full_url
        return None

    def get_image(self, obj):
        """
        Retrieves the URL of the video's screenshot image.

        This method searches for an image file in the directory where the video file is stored and returns its URL.

        Args:
        -----
        - obj (Video): The video object.

        Returns:
        --------
        - str: The absolute URL of the screenshot image, or None if no image is found.
        """
        request = self.context.get('request')
        if obj.video_file:
            video_file_path = obj.video_file.path
            print('video_file path:', video_file_path)
            screenshot_dir = os.path.dirname(video_file_path).replace('\\', '/')
            image_dir = screenshot_dir.replace('/videos/videos/', '/videos/')
            image_extensions = ['.jpg', '.png', '.webp']
            screenshot_name = None

            for ext in image_extensions:
                for filename in os.listdir(image_dir):
                    if filename.endswith(ext):
                        screenshot_name = filename
                        break
                if screenshot_name:
                    break

            if screenshot_name:
                folder_name = os.path.basename(image_dir)
                image_path = f"/media/videos/{folder_name}/{screenshot_name}"
                return request.build_absolute_uri(image_path)
            
        return None

    def update(self, instance, validated_data):
        """
        Update the Video instance with the provided validated data.

        This method checks for changes in the `video_file` and `image` fields and performs specific actions
        (like updating image paths) only when necessary. Other fields like `description` are updated directly.

        Args:
        -----
        - instance (Video): The existing video instance to be updated.
        - validated_data (dict): The data with which to update the instance.

        Returns:
        --------
        - Video: The updated video instance.
        """

        video_file = validated_data.get('video_file', instance.video_file)
        image = validated_data.get('image', instance.image)

        if video_file != instance.video_file or image != instance.image:
            if video_file:
                folder_name = os.path.splitext(os.path.basename(video_file.name))[0]

                if image and hasattr(image, 'file'):
                    original_image_name = os.path.basename(image.name)
                    new_image_name = os.path.join(folder_name, original_image_name)

                    instance.image.name = new_image_name
                    instance.image.save(instance.image.name, instance.image.file, save=False)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
    
        instance.save()

        return instance





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
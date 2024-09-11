from datetime import date
from django.db import models
from Users.models import CustomUser


class Video(models.Model):
    """
    Model representing a video with metadata such as title, URL, description, category, and related media files.

    Fields:
    -------
    - title (CharField): The title of the video (max length 255 characters).
    - url (URLField): The URL of the video (optional).
    - created_at (DateField): The date when the video was created, defaults to today's date.
    - description (CharField): A short description of the video (max length 500 characters).
    - video_file (FileField): The video file associated with this video, optional.
    - category (CharField): The category of the video, defaults to 'all_videos'.
    - screenshot (ImageField): A screenshot or thumbnail of the video, optional.

    Methods:
    --------
    - __str__():
        Returns a string representation of the video object, including its title and video file name (if available).
    """
    title = models.CharField(max_length=255)
    url = models.URLField(blank=True, null=True)
    created_at = models.DateField(default=date.today)
    description = models.CharField(max_length=500)
    video_file = models.FileField(upload_to='videos', blank=True, null=True)
    category = models.CharField(max_length=100, default='all_videos') 
    screenshot = models.ImageField(upload_to='screenshots', blank=True, null=True)
    
    
    def __str__(self):
        """
        Returns the title of the video and the name of the associated video file (if available).
        """
        video_file_name = self.video_file.name if self.video_file else "Keine Videodatei"
        return f"title: {self.title} || video_data_name: {video_file_name}"
    
    
class FavoriteVideo(models.Model):
    """
    Model representing a user's favorite video, linking a user to a specific video.

    Fields:
    -------
    - user (ForeignKey): A reference to the `CustomUser` who marked the video as a favorite.
    - video (ForeignKey): A reference to the `Video` that is marked as a favorite.

    Meta:
    -----
    - unique_together: Ensures that a user can only favorite a specific video once.

    Methods:
    --------
    - __str__():
        Returns a string representation of the favorite video object, including the user's name, ID, and the video file name (if available).
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
   
    def __str__(self):
        """
        Returns the username, user ID, and the name of the associated video file (if available).
        """
        user_name = self.user.username
        user_id = self.user.id
        video_file_name = self.video.video_file.name if self.video.video_file else "Keine Videodatei"
        return f"user_name: {user_name} , user_id: {user_id} || video_data_name: {video_file_name}"
        
    class Meta:
        unique_together = ('user', 'video')
        
        
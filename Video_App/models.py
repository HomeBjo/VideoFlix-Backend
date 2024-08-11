from datetime import date
from django.db import models
from Users.models import CustomUser


class Video(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField(blank=True, null=True)
    created_at = models.DateField(default=date.today)
    description = models.CharField(max_length=500)
    video_file = models.FileField(upload_to='videos', blank=True, null=True)
    category = models.CharField(max_length=100, default='all_videos') 
    screenshot = models.ImageField(upload_to='screenshots', blank=True, null=True)
    
    
    def __str__(self):
        video_file_name = self.video_file.name if self.video_file else "Keine Videodatei"
        return f"title: {self.title} || video_data_name: {video_file_name}"
    
    
class FavoriteVideo(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
   
    def __str__(self):
        user_name = self.user.username
        user_id = self.user.id
        video_file_name = self.video.video_file.name if self.video.video_file else "Keine Videodatei"
        return f"user_name: {user_name} , user_id: {user_id} || video_data_name: {video_file_name}"
        
    class Meta:
        unique_together = ('user', 'video')
        
        
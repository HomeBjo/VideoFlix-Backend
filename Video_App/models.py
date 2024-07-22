from datetime import date
from django.db import models
from Users.models import CustomUser


class Video(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField(blank=True, null=True)
    created_at = models.DateField(default=date.today)
    description = models.CharField(max_length=500)
    video_file = models.FileField(upload_to='videos', blank=True, null=True)
    
    
    
    def __str__(self):
        return self.title
    
    
class FavoriteVideo(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    favorite = models.BooleanField(default=False)
        
    class Meta:
        unique_together = ('user', 'video')
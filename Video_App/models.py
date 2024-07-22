from django.db import models
from Users.models import CustomUser


class Video(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
  
    favorite = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.title
    
    
class FavoriteVideo(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
        
    class Meta:
        unique_together = ('user', 'video')
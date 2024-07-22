
from django.db import models


# class EditVideos(models.Model):
#     favorite = models.BooleanField(default=False)
    
    
class Video(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    # editVideo = models.OneToOneField(EditVideos, on_delete=models.CASCADE, default=False)
    favorite = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.title
    
    
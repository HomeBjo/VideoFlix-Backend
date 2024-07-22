from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.title
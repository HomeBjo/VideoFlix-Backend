
import os
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from Video_App.models import Video



@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print('Video saved')
    if created:
        print('New Video uploaded')


@receiver(post_delete, sender=Video)
def delete_video_file(sender, instance, **kwargs):
    print('Video start delete')
    if instance.video_file:
        print('Video ###################')
        if os.path.isfile(instance.video_file.path):
            print('Video deleted')
            os.remove(instance.video_file.path)
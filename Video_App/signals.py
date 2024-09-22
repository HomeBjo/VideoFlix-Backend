import os
import shutil
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from Video_App.models import Video
from Video_App.tasks import convert_video_480p, convert_video_720p, convert_video_1080p
import django_rq
from django.conf import settings


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    """
    Handles the post-save signal for the Video model.

    If a new video is uploaded, it creates a folder based on the video file's base name,
    moves the video file into this folder, updates the video file's path, and queues video conversion tasks.

    Parameters:
    -----------
    - sender: The model class (Video).
    - instance: The saved Video instance.
    - created: Boolean indicating if a new record was created.
    - **kwargs: Additional keyword arguments.
    """
    if created:
        print('New Video uploaded')
        folder_name = os.path.splitext(instance.video_file.name)[0]
        folder = os.path.join(settings.MEDIA_ROOT, folder_name)
        print(f'found folder: {folder}')
        os.makedirs(folder, exist_ok=True)
        
        original_video_path = instance.video_file.path
        new_video_path = os.path.join(folder, os.path.basename(original_video_path))
        os.rename(original_video_path, new_video_path)
        
        instance.video_file.name = os.path.join('videos', folder_name, os.path.basename(original_video_path))
        instance.save()

        queue = django_rq.get_queue('default', autocommit=True)
        new_video_path = new_video_path.replace('\\', '/')
        print(f'new video path: {new_video_path}')
        queue.enqueue(convert_video_480p, new_video_path)
        queue.enqueue(convert_video_720p, new_video_path)
        queue.enqueue(convert_video_1080p, new_video_path)
        
        

@receiver(post_delete, sender=Video)
def delete_video_file(sender, instance, **kwargs):
    """
    Handles the post-delete signal for the Video model.

    Deletes the folder containing the video and associated files when a Video instance is removed.

    Parameters:
    -----------
    - sender: The model class (Video).
    - instance: The deleted Video instance.
    - **kwargs: Additional keyword arguments.
    """
    if instance.video_file:
        folder_name = os.path.splitext(os.path.basename(instance.video_file.name))[0]
        folder = os.path.join(settings.MEDIA_ROOT, folder_name)
        new_folder_path = folder.replace('\\', '/')
        print(f'found folder: {new_folder_path}')
        if os.path.isdir(new_folder_path):
            print(f'Folder deleted: {new_folder_path}')
            shutil.rmtree(new_folder_path)

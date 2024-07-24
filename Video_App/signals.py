
import os
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from Video_App.models import Video
from Video_App.tasks import convert_video_480p



@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print('Video saved')
    if created:
        convert_video_480p(instance.video_file.path)
        print('New Video uploaded')


@receiver(post_delete, sender=Video)
def delete_video_file(sender, instance, **kwargs):
    print('Video start deleting')
    if instance.video_file:
        print(f'Video: {instance.video_file} deleting')
        if os.path.isfile(instance.video_file.path):
            print('Video deleted')
            os.remove(instance.video_file.path)
            
            
############ anfang einer filter delte Video funktion 
# @receiver(post_delete, sender=Video)
# def delete_video_file(sender, instance, **kwargs):
#     print('Video start deleting')
#     if instance.video_file:
#         base_path = instance.video_file.path
#         base_name, ext = os.path.splitext(base_path)  # Trennt den Dateinamen von der Erweiterung

#         # Muster für die zu löschenden Dateien erstellen
#         pattern = f"{base_name}_*{ext}"
#         files_to_delete = glob.glob(pattern)

#         # Alle gefundenen Dateien löschen
#         for file_path in files_to_delete:
#             if os.path.isfile(file_path):
#                 print(f'Deleting {file_path}')
#                 os.remove(file_path)

#         # Schließlich das Originalvideo löschen
#         if os.path.isfile(base_path):
#             print(f'Deleting original video: {base_path}')
#             os.remove(base_path)

import os
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from Video_App.models import Video
from Video_App.tasks import convert_video_480p
import django_rq



@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    if created:
        print('New Video uploaded')
        folder_name = os.path.splitext(instance.video_file.name)[0]
        folder = os.path.join('C:/DevProjekte/Backend/Modul8/Videoflix_backend/Videoflix/media', folder_name)
        os.makedirs(folder, exist_ok=True)
        
        original_video_path = instance.video_file.path
        new_video_path = os.path.join(folder, os.path.basename(original_video_path))
        os.rename(original_video_path, new_video_path)
        
        instance.video_file.name = os.path.join('videos', folder_name, os.path.basename(original_video_path))
        instance.save()

        queue = django_rq.get_queue('default', autocommit=True)
        new_video_path = new_video_path.replace('\\', '/')
        queue.enqueue(convert_video_480p, new_video_path)
        # queue.enqueue(convert_video_720p, new_video_path)



@receiver(post_delete, sender=Video)
def delete_video_file(sender, instance, **kwargs):
    print('Video start deleting')
    if instance.video_file:
        print(f'found Video: {instance.video_file}')
        if os.path.isfile(instance.video_file.path):
            print(f'Video deleted: {instance.video_file.path}')
            os.remove(instance.video_file.path)
            
            video_480p = os.path.splitext(instance.video_file.path)[0] + '_480p.mp4'
            if os.path.isfile(video_480p):
                os.remove(video_480p)
                print(f'Video 480p deleted: {video_480p}')
                
            video_720p = os.path.splitext(instance.video_file.path)[0] + '_720p.mp4'
            if os.path.isfile(video_720p):
                os.remove(video_720p)
                print(f'Video 720p deleted: {video_720p}')

            
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

# @receiver(post_delete, sender=Video)
# def delete_video_file(sender, instance, **kwargs):
#     if instance.video_file:
#         base_path = os.path.splitext(instance.video_file.path)[0]
#         file_extensions = ['', '_480p.mp4', '_720p.mp4']
        
#         for extension in file_extensions:
#             file_path = base_path if extension == '' else base_path + extension
#             if os.path.isfile(file_path):
#                 os.remove(file_path)
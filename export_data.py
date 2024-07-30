import django
import os

# Set the default Django settings module for the 'shell' command.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Videoflix.settings')

# Initialize Django
django.setup()

from Video_App.admin import VideoResource, FavoriteVideoResource
from Users.admin import CustomUserResource

# Export data from VideoResource
video_resource = VideoResource()
video_dataset = video_resource.export()
with open('videos.json', 'w') as f:
    f.write(video_dataset.json)

# Export data from FavoriteVideoResource
favorite_video_resource = FavoriteVideoResource()
favorite_video_dataset = favorite_video_resource.export()
with open('favorite_videos.json', 'w') as f:
    f.write(favorite_video_dataset.json)

# Export data from CustomUserResource
custom_user_resource = CustomUserResource()
custom_user_dataset = custom_user_resource.export()
with open('custom_users.json', 'w') as f:
    f.write(custom_user_dataset.json)

print("Data exported successfully")

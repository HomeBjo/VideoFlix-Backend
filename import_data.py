import django
import os
import json
from tablib import Dataset

# Set the default Django settings module for the 'shell' command.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Videoflix.settings')

# Initialize Django
django.setup()

from Video_App.admin import VideoResource, FavoriteVideoResource
from Users.admin import CustomUserResource

# Import data into VideoResource
video_resource = VideoResource()
with open('videos.json', 'r') as f:
    video_data = f.read()
video_dataset = Dataset().load(video_data, format='json')
video_resource.import_data(video_dataset, format='json')

# Import data into FavoriteVideoResource
favorite_video_resource = FavoriteVideoResource()
with open('favorite_videos.json', 'r') as f:
    favorite_video_data = f.read()
favorite_video_dataset = Dataset().load(favorite_video_data, format='json')
favorite_video_resource.import_data(favorite_video_dataset, format='json')

# Import data into CustomUserResource
custom_user_resource = CustomUserResource()
with open('custom_users.json', 'r') as f:
    custom_user_data = f.read()
custom_user_dataset = Dataset().load(custom_user_data, format='json')
custom_user_resource.import_data(custom_user_dataset, format='json')

print("Data imported successfully")

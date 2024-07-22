from django.contrib import admin

from Users.forms import CostomUserCreationForm
from .models import FavoriteVideo, Video



admin.site.register(Video)
admin.site.register(FavoriteVideo)


    
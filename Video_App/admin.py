from django.contrib import admin
from import_export import resources
from .models import FavoriteVideo, Video
from import_export.admin import ImportExportModelAdmin


class VideoResource(resources.ModelResource):
    class Meta:
        model = Video
        
class FavoriteVideoResource(resources.ModelResource):
    class Meta:
        model = FavoriteVideo
        
            
@admin.register(Video)
class VideoAdmin(ImportExportModelAdmin):
    resource_class = VideoResource

@admin.register(FavoriteVideo)
class FavoriteVideoAdmin(ImportExportModelAdmin):
    resource_class = FavoriteVideoResource

    
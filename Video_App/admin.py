from django.contrib import admin
from import_export import resources
from .models import FavoriteVideo, Video
from import_export.admin import ImportExportModelAdmin


class VideoResource(resources.ModelResource):
    """
    Resource class for the Video model, enabling import/export functionality.
    
    This class is used to define the import/export capabilities for the `Video` model using the django-import-export package.
    
    Meta:
    -----
    - model: Video (The model to be imported/exported).
    """
    class Meta:
        model = Video
        
class FavoriteVideoResource(resources.ModelResource):
    """
    Resource class for the FavoriteVideo model, enabling import/export functionality.
    
    This class is used to define the import/export capabilities for the `FavoriteVideo` model using the django-import-export package.
    
    Meta:
    -----
    - model: FavoriteVideo (The model to be imported/exported).
    """
    class Meta:
        model = FavoriteVideo
        
            
@admin.register(Video)
class VideoAdmin(ImportExportModelAdmin):
    """
    Admin interface for managing Video instances.
    
    This class extends `ImportExportModelAdmin` from the django-import-export package, enabling import/export functionality
    for the `Video` model in the Django admin interface.

    Attributes:
    -----------
    - resource_class: Links the `VideoResource` class to enable import/export actions for the `Video` model.
    """
    resource_class = VideoResource

@admin.register(FavoriteVideo)
class FavoriteVideoAdmin(ImportExportModelAdmin):
    """
    Admin interface for managing FavoriteVideo instances.
    
    This class extends `ImportExportModelAdmin` from the django-import-export package, enabling import/export functionality
    for the `FavoriteVideo` model in the Django admin interface.

    Attributes:
    -----------
    - resource_class: Links the `FavoriteVideoResource` class to enable import/export actions for the `FavoriteVideo` model.
    """
    resource_class = FavoriteVideoResource

    
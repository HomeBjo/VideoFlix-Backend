from django.contrib import admin
from Users.forms import CustomUserCreationForm
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin



class CustomUserResource(resources.ModelResource):
    """
    Resource class for the import/export functionality of CustomUser data.
    
    This class provides configuration for exporting and importing `CustomUser` model data 
    using django-import-export package.
    
    Meta:
    -----
    - model: CustomUser (The model to be imported/exported).
    """
    class Meta:
        model = CustomUser



@admin.register(CustomUser)
class CustomUserAdmin(ImportExportModelAdmin, UserAdmin):
    """
    Admin interface for managing CustomUser instances.
    
    This class extends both `UserAdmin` from `django.contrib.auth` for handling user-specific functionality 
    and `ImportExportModelAdmin` from `django-import-export` for allowing data import/export.

    Attributes:
    -----------
    - add_form: The form used for creating new users (`CustomUserCreationForm`).
    - fieldsets: Customizes the admin interface to include additional user-specific fields like `custom`, `address`, and `phone`.
    - resource_class: The resource class used for handling import/export actions.

    Custom fieldsets:
    -----------------
    - Individuelle Daten: Includes the fields 'custom', 'address', and 'phone'.
    """
    add_form = CustomUserCreationForm
    fieldsets = (
        (
            'Individuelle Daten',
            {
                'fields': (
                    'custom', 
                    'address', 
                    'phone',
                )
            }
        ),
        *UserAdmin.fieldsets 
    )
    resource_class = CustomUserResource


    



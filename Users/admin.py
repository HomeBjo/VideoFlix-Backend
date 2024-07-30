from django.contrib import admin
from Users.forms import CustomUserCreationForm
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin



class CustomUserResource(resources.ModelResource):
    class Meta:
        model = CustomUser



@admin.register(CustomUser)
class CustomUserAdmin(ImportExportModelAdmin, UserAdmin):
    add_form = CustomUserCreationForm
    fieldsets = (
        # *UserAdmin.fieldsets, # Admininterfaceanzeige unten
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
        *UserAdmin.fieldsets # Admininterfaceanzeige oben
    )
    resource_class = CustomUserResource


    



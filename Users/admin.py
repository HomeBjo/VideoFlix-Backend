from django.contrib import admin
from .models import CustomUser
from .forms import CostomUserCreationForm
from django.contrib.auth.admin import UserAdmin


@admin.register(CustomUser)
class CostomUserAdmin(admin.ModelAdmin):
    add_form = CostomUserCreationForm
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



import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Videoflix.settings')

# Initialize Django
django.setup()

from django.contrib.auth import views as auth_views

print("PasswordResetView:", auth_views.PasswordResetView)
print("PasswordResetDoneView:", auth_views.PasswordResetDoneView)
print("PasswordResetConfirmView:", auth_views.PasswordResetConfirmView)
print("PasswordResetCompleteView:", auth_views.PasswordResetCompleteView)

from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):  
   custom = models.CharField(max_length=500, default='')    
   address = models.CharField(max_length=150, default='')   
   phone = models.CharField(max_length=25, default='')
   
groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',  # Vermeidet Konflikte
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # Vermeidet Konflikte
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
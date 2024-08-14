from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):  
    custom = models.CharField(max_length=500, default='')    
    address = models.CharField(max_length=150, default='')   
    phone = models.CharField(max_length=25, default='')
    email = models.EmailField(unique=True)  # E-Mail muss eindeutig sein

    # Setze den Benutzernamen als nicht erforderlich
    username = models.CharField(max_length=150, blank=True, null=True)  # optional

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
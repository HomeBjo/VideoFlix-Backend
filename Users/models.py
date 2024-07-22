from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):  
    custom = models.CharField(max_length=500, default='')    
    address = models.CharField(max_length=150, default='')   
    phone = models.CharField(max_length=25, default='')
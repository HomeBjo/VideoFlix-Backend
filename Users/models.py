from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    """
    Custom manager for handling user creation with email as the unique identifier instead of a username.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a regular user with the given email and password.

        Args:
        -----
        email (str): The user's email address, which is required.
        password (str): The user's password. Default is None.
        **extra_fields: Additional fields for the user model.

        Raises:
        -------
        ValueError: If the email is not provided.

        Returns:
        --------
        user: The created user instance.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.

        Args:
        -----
        email (str): The superuser's email address, which is required.
        password (str): The superuser's password. Default is None.
        **extra_fields: Additional fields for the superuser model.

        Raises:
        -------
        ValueError: If is_staff or is_superuser are not set to True.

        Returns:
        --------
        user: The created superuser instance.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser): 
    """
    Custom user model that replaces the username with email as the unique identifier.

    Fields:
    -------
    custom (str): A custom field, default is an empty string.
    address (str): The user's address, default is an empty string.
    phone (str): The user's phone number, default is an empty string.
    email (EmailField): The user's email, must be unique.
    username (str): The user's username, optional and can be null or blank.

    Authentication:
    ---------------
    The email is used as the `USERNAME_FIELD` for authentication.
    The `REQUIRED_FIELDS` are left empty, meaning no additional fields are required on user creation besides the email.
    """
    custom = models.CharField(max_length=500, default='')    
    address = models.CharField(max_length=150, default='')   
    phone = models.CharField(max_length=25, default='')
    email = models.EmailField(unique=True) 

    username = models.CharField(max_length=150, blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager() 

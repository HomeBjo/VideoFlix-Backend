from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Configuration class for the 'Users' application.

    This class inherits from Django's AppConfig and sets up the configuration for the 'Users' app.
    
    Attributes:
    -----------
    - default_auto_field: Specifies the type of auto-incrementing field to use for models in the app. 
      Here, 'BigAutoField' is used by default.
    - name: The name of the app, which is 'Users'.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Users'

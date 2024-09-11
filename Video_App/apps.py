from django.apps import AppConfig


class VideoAppConfig(AppConfig):
    """
    Configuration class for the 'Video_App' application.

    This class extends Django's AppConfig and sets up the configuration for the 'Video_App' application.

    Attributes:
    -----------
    - default_auto_field: Specifies the type of auto-incrementing field to use for models in the app.
      Here, 'BigAutoField' is used by default.
    - name: The name of the app, which is 'Video_App'.

    Methods:
    --------
    - ready():
        This method is executed when the app is ready. It imports the `signals` module to ensure that
        any signal handlers defined in `signals.py` are registered when the app starts.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Video_App'
    
    def ready(self):
        """
        Imports the signals module when the app is ready.

        This method ensures that the signal handlers defined in the `signals` module are registered
        and can respond to events (such as saving or deleting objects).
        """
        from . import signals

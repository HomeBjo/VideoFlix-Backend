from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    A form for creating new users, using the CustomUser model.

    This form extends the built-in UserCreationForm from Django to handle the creation of new users 
    based on the CustomUser model, including all fields defined in that model.

    Meta:
    -----
    - model: CustomUser
    - fields: '__all__' (All fields from the CustomUser model are included in the form.)
    """
    class Meta:
        model = CustomUser
        fields = '__all__'
        
        
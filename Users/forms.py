from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CostomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = '__all__'
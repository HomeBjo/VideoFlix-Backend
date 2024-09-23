from rest_framework import serializers
from Users.models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model.
    
    This serializer handles the serialization and deserialization of CustomUser objects, including user creation and updating.

    Meta:
    -----
    - model: CustomUser
    - fields: All fields in the CustomUser model.

    Methods:
    --------
    - create(validated_data):
        Creates a new CustomUser instance with the provided data, sets the password, marks the user as inactive, and saves the user.
    
    - update(instance, validated_data):
        Updates an existing CustomUser instance with the provided data and saves the updated instance.
    """
    class Meta:
        model = CustomUser
        fields = '__all__'

    def create(self, validated_data):
        """
        Creates a new CustomUser instance.

        Args:
        -----
        validated_data (dict): The validated data for the user.

        Returns:
        --------
        user: The newly created CustomUser instance.
        """
        print(validated_data)
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()
        return user
    
    def update(self, instance, validated_data):
        """
        Updates an existing CustomUser instance.

        Args:
        -----
        instance (CustomUser): The existing user instance to be updated.
        validated_data (dict): The validated data to update the instance.

        Returns:
        --------
        instance: The updated CustomUser instance.
        """
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.address = validated_data.get("address", instance.address)

        instance.save()
        return instance

    
class EmailAuthTokenSerializer(serializers.Serializer):
    """
    Serializer for authenticating users via email and password.
    
    Fields:
    -------
    - email (EmailField): The user's email, used for authentication.
    - password (CharField): The user's password.

    Methods:
    --------
    - validate(attrs):
        Validates the user's email and password, and ensures the user is active.
    
    Raises:
    -------
    - ValidationError: If the email or password is incorrect or the user is inactive.
    """
    
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        """
        Validates the provided email and password.
        
        Args:
        -----
        attrs (dict): The attributes containing the email and password.
        
        Returns:
        --------
        attrs: The validated attributes with the user added.
        
        Raises:
        -------
        ValidationError: If the email or password is incorrect or the user is inactive.
        """
        print(attrs)
        user = get_user_model().objects.filter(email=attrs['email']).first()
        if user and user.check_password(attrs['password']) and user.is_active: 
            attrs['user'] = user 
            return attrs
        raise serializers.ValidationError('Invalid email or password.')
    
    
class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for handling password reset requests.
    
    Fields:
    -------
    - email (EmailField): The email of the user requesting a password reset.

    Methods:
    --------
    - validate_email(value):
        Validates the email field.
    
    - save():
        Initiates the password reset process by sending a password reset email.
    """
    email = serializers.EmailField()

    def validate_email(self, value):
        """
        Validates the provided email.

        Args:
        -----
        value (str): The email to validate.

        Returns:
        --------
        value: The validated email.
        """
        return value

    def save(self):
        """
        Sends a password reset email to the user.

        Process:
        --------
        - Validates the user's email.
        - Sends a password reset email using the provided email template and context.
        """
        request = self.context.get('request')

        current_domain = request.build_absolute_uri('/')[:-1].strip("/")
        if "aleksanderdemyanovych.de" in current_domain:
            frontend_url = "https://videoflix.aleksanderdemyanovych.de"
        elif "xn--bjrnteneicken-jmb.de" in current_domain:
            frontend_url = "https://videoflix.xn--bjrnteneicken-jmb.de"
    

        password_reset_form = PasswordResetForm(data=self.validated_data)
        if password_reset_form.is_valid():
            password_reset_form.save(
                request=request,
                use_https=request.is_secure(),
                from_email=None,  
                html_email_template_name='password_reset_email.html',  
                extra_email_context={'frontend_url': frontend_url}
            )

class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for confirming password reset requests.

    Fields:
    -------
    - new_password1 (CharField): The first input for the new password.
    - new_password2 (CharField): The second input for the new password, should match the first.

    Methods:
    --------
    - validate(attrs):
        Ensures the two password fields match.
    
    - save(user):
        Saves the new password for the user.
    """
    new_password1 = serializers.CharField()
    new_password2 = serializers.CharField()

    def validate(self, attrs):
        """
        Validates that the two new passwords match.

        Args:
        -----
        attrs (dict): The attributes containing the new passwords.

        Returns:
        --------
        attrs: The validated attributes.

        Raises:
        -------
        ValidationError: If the passwords do not match.
        """
        if attrs['new_password1'] != attrs['new_password2']:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def save(self, user):
        """
        Saves the new password for the user.

        Args:
        -----
        user (CustomUser): The user whose password is being reset.
        """
        user.set_password(self.validated_data['new_password1'])
        user.save()
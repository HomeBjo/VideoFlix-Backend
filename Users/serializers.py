from rest_framework import serializers
from Users.models import CustomUser
from Video_App.serializers import VideoSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def create(self, validated_data):
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
        Serializes an email and password for authentication. '' das ist anstatt user login  das wir email mit nehmen als login parameter''
    """
    
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        print(attrs)
        user = get_user_model().objects.filter(email=attrs['email']).first() # filtert den user raus
        if user and user.check_password(attrs['password']) and user.is_active: # überprüft ob der user aktiv ist und das passwort stimmt
            attrs['user'] = user # user wird in attrs gespeichert(siehe für atts den print)
            return attrs
        raise serializers.ValidationError('Invalid email or password.')
    
    
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        # Optional: Hier kannst du benutzerdefinierte Validierungen hinzufügen
        return value

    def save(self):
        request = self.context.get('request')
        frontend_url = "http://localhost:4200"  # Hier die URL deiner Angular-Anwendung
        
        password_reset_form = PasswordResetForm(data=self.validated_data)
        if password_reset_form.is_valid():
            # E-Mail versenden, wobei die benutzerdefinierte Vorlage verwendet wird
            password_reset_form.save(
                request=request,
                use_https=request.is_secure(),
                from_email=None,
                # email_template_name='password_reset_email.html'    
                html_email_template_name='password_reset_email.html',  #als html anzeigen damit das klappt
                extra_email_context={'frontend_url': frontend_url}  # Hier übergeben wir die frontend_url
            )

class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password1 = serializers.CharField()
    new_password2 = serializers.CharField()

    def validate(self, attrs):
        if attrs['new_password1'] != attrs['new_password2']:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def save(self, user):
        user.set_password(self.validated_data['new_password1'])
        user.save()
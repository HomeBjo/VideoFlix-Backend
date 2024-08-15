from rest_framework import serializers
from Users.models import CustomUser
from Video_App.serializers import VideoSerializer
from django.contrib.auth import get_user_model


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
    
    
class PasswordChangeSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def save(self, user):
        user.set_password(self.validated_data['new_password1'])
        user.save()
        return user

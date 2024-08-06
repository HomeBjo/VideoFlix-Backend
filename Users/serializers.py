from rest_framework import serializers
from Users.models import CustomUser
from Video_App.serializers import VideoSerializer


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
            phone=validated_data['phone'],
        )
        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()
        return user


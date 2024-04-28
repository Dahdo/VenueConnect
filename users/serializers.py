from rest_framework import serializers
from .models import CustomUser, Profile


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'phone_number', 'email']
    

class ProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Profile
        fields = ['user', 'avatar', 'bio', 'languages_spoken']

    def update(self, instance, validated_data):
        # Update fields of the embedded user model
        user_data = validated_data.pop('user', {})
        user = instance.user
        user.username = user_data.get('username', user.username)
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.email = user_data.get('email', user.email)
        user.phone_number = user_data.get('phone_number', user.phone_number)
        user.save()

        # Update fields of the main model
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.languages_spoken = validated_data.get('languages_spoken', instance.languages_spoken)
        instance.save()

        return instance



class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username','password', 'first_name', 'last_name', 'phone_number', 'email']

    def create(self, validated_data):
        phone_number_data = validated_data.pop('phone_number')
        username_data = validated_data.pop('username')
        password_data = validated_data.pop('password')
        first_name_data = validated_data.pop('first_name')
        last_name_data = validated_data.pop('last_name')
        email_data = validated_data.pop('email')

        user = CustomUser.objects.create(username=username_data, first_name=first_name_data, last_name=last_name_data
                                         , email=email_data, phone_number = phone_number_data)
        user.set_password(password_data)
        user.save()
        return user


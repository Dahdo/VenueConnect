from rest_framework import serializers
from .models import PhoneNumber, CustomUser, Profile

class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ['number', 'is_verified']
        read_only_fields = ['is_verified']


class CustomUserSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberSerializer()
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'phone_number', 'email']
        depth = 1
    

class ProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    class Meta:
        model = Profile
        fields = ['user', 'avatar_url', 'bio', 'languages_spoken']
        read_only_fields = ['avatar_url']


    def update(self, instance, validated_data):
        # Update fields of the main model instance
        instance.user.username = validated_data.get('username', instance.user.username)
        instance.user.first_name = validated_data.get('first_name', instance.user.first_name)
        instance.user.last_name = validated_data.get('last_name', instance.user.last_name)
        instance.user.email = validated_data.get('email', instance.user.email)

        phone_number_data = validated_data.pop('phone_number')
        if phone_number_data:
            instance.user.phone_number, _ = PhoneNumber.objects.get_or_create(**phone_number_data)

        instance.user.save()
        instance.save()
        return instance



class UserRegistrationSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberSerializer()
    class Meta:
        model = CustomUser
        fields = ['username','password', 'first_name', 'last_name', 'phone_number', 'email']
        depth = 1

    def create(self, validated_data):
        phone_number_data = validated_data.pop('phone_number')
        username_data = validated_data.pop('username')
        password_data = validated_data.pop('password')
        first_name_data = validated_data.pop('first_name')
        last_name_data = validated_data.pop('last_name')
        email_data = validated_data.pop('email')


        # Create PhoneNumber object associated with the user
        phone_number_obj = PhoneNumber.objects.create(**phone_number_data)

        user = CustomUser.objects.create(username=username_data, first_name=first_name_data, last_name=last_name_data
                                         , email=email_data, phone_number = phone_number_obj)
        user.set_password(password_data)
        user.save()
        return user


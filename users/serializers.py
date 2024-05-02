from rest_framework import serializers
from .models import CustomUser, Profile

# For phone number validation
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from phonenumber_field.phonenumber import PhoneNumber, to_python

def validate_international_phonenumber(value):
    phone_number = to_python(value)
    if isinstance(phone_number, PhoneNumber) and not phone_number.is_valid():
        raise ValidationError(
            _("The phone number entered is not valid."), code="invalid_phone_number"
        )
    

class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    phone_number = serializers.CharField(source='user.phone_number')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = Profile
        fields = ['id', 'username', 'first_name', 'last_name', 'phone_number', 'email', 'avatar', 'bio', 'languages_spoken']
    

    def get_avatar(self, profile):
        request = self.context.get('request')
        if profile.avatar:
            return request.build_absolute_uri(profile.avatar.url)
        else:
            return request.build_absolute_uri('/media/avatars/placeholder.jpg')
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Check if the avatar field is set
        if not instance.avatar:
            # If not set, assign the default avatar URL
            request = self.context.get('request')
            data['avatar'] = request.build_absolute_uri('/media/avatars/placeholder.jpg')
        return data

    def validate_username(self, value):
        instance = self.instance 
        if instance and instance.user.username == value:
            return value  # Allow the current user to keep their username

        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username not available!")
        return value
    
    def validate_phone_number(self, value):
        instance = self.instance
        # Phone number should be unique but allow the user to keep theirs
        if CustomUser.objects.filter(phone_number=value).exists() and instance.user.phone_number != value:
            raise serializers.ValidationError("Phone number already in use!")
        validate_international_phonenumber(value)
        return value
    
    def update(self, instance, validated_data):
        # Update fields of the main model instance
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


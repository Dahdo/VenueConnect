from rest_framework import serializers
from venues.models import CustomUser, Venue, Address


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ['name', 'description', 'owner', 'price', 'pricing_unit',
                   'capacity', 'rating', 'rating_count', 'available', 'picture_url', 'address']

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
        instance.user.phone_number = validated_data.get('phone_number', instance.user.phone_number)

        instance.user.save()
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


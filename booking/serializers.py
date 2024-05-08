from rest_framework import serializers
from .models import Bookings
from venues.models import Venue
from users.models import CustomUser
from django.core.exceptions import ValidationError


class BookingsSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    venue_id = serializers.IntegerField()

    class Meta:
        model = Bookings
        fields = ['id', 'user_id', 'venue_id', 'state', 'check_in', 'check_out']
        read_only_filds = ['id']

    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        venue_id = validated_data.pop('venue_id')
        user = CustomUser.objects.get(id=user_id)
        venue = Venue.objects.get(id=venue_id)
        check_in = validated_data.get('check_in')
        check_out = validated_data.get('check_out')
        # Check for conflicting bookings
        conflicting_bookings = venue.bookings.filter(
            check_in__lt=check_out,
            check_out__gt=check_in,
            state='active'
        )
        if conflicting_bookings.exists():
            # If there are conflicting bookings, raise an error
            raise ValidationError("There is an active booking conflicting with the requested time bounds.")
        else:
            # If there are no conflicting bookings, create the new booking
            booking = Bookings.objects.create(user=user, venue=venue, **validated_data)
            return booking
from rest_framework import serializers
from .models import Bookings
from venues.models import Venue
from users.models import CustomUser


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
        bookings = Bookings.objects.create(user=user, venue=venue, **validated_data)
        return bookings
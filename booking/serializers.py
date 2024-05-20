from rest_framework import serializers
from .models import Bookings, Review
from venues.models import Venue
from users.models import CustomUser
from django.core.exceptions import ValidationError


class ReviewSerializer(serializers.ModelSerializer):
    booking_id = serializers.IntegerField()
    user_id = serializers.IntegerField(read_only=True, source='booking.user.id')

    class Meta:
        model = Review
        fields = ['id', 'booking_id', 'user_id', 'rating', 'comment']
        read_only_fields = ['id', 'user_id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user_id'] = instance.booking.user.id
        return representation

    def create(self, validated_data):
        booking_id = validated_data.pop('booking_id')
        booking = Bookings.objects.get(id=booking_id)
        review = Review.objects.create(booking=booking, **validated_data)
        return review

    def update(self, instance, validated_data):
        booking_id = validated_data.get('booking_id', instance.booking.id)
        instance.booking = Bookings.objects.get(id=booking_id)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance


class BookingsSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    venue_id = serializers.IntegerField()
    review = ReviewSerializer(read_only=True, source='user_review')

    class Meta:
        model = Bookings
        fields = ['id', 'user_id', 'venue_id', 'state', 'check_in', 'check_out', 'total_price', 'number_of_guests', 'review']
        read_only_fields = ['id']

    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        venue_id = validated_data.pop('venue_id')
        user = CustomUser.objects.get(id=user_id)
        venue = Venue.objects.get(id=venue_id)
        number_of_guests = validated_data.get('number_of_guests', 1)
        total_price = validated_data.get('total_price')
        state = validated_data.get('state', 'active')
        check_in = validated_data.get('check_in')
        check_out = validated_data.get('check_out')

        # Check whether number_of_guests doesn't exceed the venue capacity

        if number_of_guests > venue.capacity:
            raise ValidationError(f"The venue capacity can't exceed {venue.capacity}")
        
        if check_out < check_in:
            raise ValidationError(f"Checkout can't be earlier than checkin")

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
            # Calculate the total price
            duration = check_out - check_in
            if total_price is None or total_price == '':
                total_price = duration.days * venue.price
            # Create new booking
            booking = Bookings.objects.create(user=user, venue=venue, number_of_guests=number_of_guests,state=state,
                                              total_price=total_price, check_in=check_in, check_out=check_out)
            return booking
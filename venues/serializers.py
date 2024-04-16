from rest_framework import serializers
from venues.models import CustomUser, Venue
from users.serializers import CustomUserSerializer


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ['id', 'name', 'description', 'price', 'pricing_unit',
                   'capacity', 'rating', 'available', 'picture_url', 'latitude', 'longitude']
        read_only_fields = ['picture_url']
    
    def create(self, validated_data):
        name_data = validated_data.pop('name', "")
        description_data = validated_data.pop('description', "")
        price_data = validated_data.pop('price', None)
        pricing_unit_data = validated_data.pop('pricing_unit')
        capacity_data = validated_data.pop('capacity', None)
        rating_data = validated_data.pop('rating')
        available_data = validated_data.pop('available')
        latitude_data = validated_data.pop('latitude', None)
        longitude_data = validated_data.pop('longitude', None)

        venue = Venue.objects.create(name=name_data, description=description_data, price=price_data, 
                                          pricing_unit=pricing_unit_data,capacity=capacity_data, rating=rating_data, 
                                          available=available_data, latitude= latitude_data, longitude=longitude_data)
        venue.save()
        return venue
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.pricing_unit = validated_data.get('pricing_unit', instance.pricing_unit)
        instance.capacity = validated_data.get('capacity', instance.capacity)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.rating_count = validated_data.get('rating_count', instance.rating_count)
        instance.available = validated_data.get('available', instance.available)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.longitude = validated_data.get('longitude', instance.longitude)

        instance.save()
        return instance

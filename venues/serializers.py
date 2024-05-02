from rest_framework import serializers
from venues.models import Venue, VenueImages, Address

class VenueSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    upload_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, write_only=True, use_url=False),
        required=False
    )

    city = serializers.CharField(source='address.city', allow_null=True)
    street = serializers.CharField(source='address.street', allow_null=True)
    postal_code = serializers.CharField(source='address.postal_code', allow_null=True)
    latitude = serializers.DecimalField(source='address.latitude', max_digits=9, decimal_places=6, allow_null=True)
    longitude = serializers.DecimalField(source='address.longitude', max_digits=9, decimal_places=6, allow_null=True)

    class Meta:
        model = Venue
        fields = ['id', 'name', 'description', 'price', 'pricing_unit',
                   'capacity', 'rating', 'available_from', 'available_till','city', 'street', 
                   'postal_code', 'latitude', 'longitude', 'images','upload_images' ]
        
    def get_images(self, obj):
        request = self.context.get('request')
        return [request.build_absolute_uri(image.image.url) for image in obj.images.all()]
    
    def create(self, validated_data):
        address_data = validated_data.pop('address', None)
        uploaded_images = validated_data.pop('upload_images', [])

        name_data = validated_data.pop('name')
        description_data = validated_data.pop('description')
        price_data = validated_data.pop('price')
        pricing_unit_data = validated_data.pop('pricing_unit')
        capacity_data = validated_data.pop('capacity')
        rating_data = validated_data.pop('rating')
        available_from_data = validated_data.pop('available_from')
        available_till_data = validated_data.pop('available_till')
        venue = Venue.objects.create(name=name_data, description=description_data, price=price_data,
                                     pricing_unit=pricing_unit_data, capacity=capacity_data, rating=rating_data,
                                     available_from=available_from_data, available_till=available_till_data)
        venue.save()
        for image in uploaded_images:
            VenueImages.objects.create(venue=venue, image=image)
        
        if address_data:
            address = Address.objects.create(**address_data)
            venue.address = address
            venue.save()

        return venue
    
    def update(self, instance, validated_data):
        if 'upload_images' in validated_data:
            instance.images.all().delete() # Delete existing images
            uploaded_images = validated_data.pop('upload_images')
            for image in uploaded_images:
                VenueImages.objects.create(venue=instance, image=image)

        address_data = validated_data.pop('address', None)
        address = instance.address

        if address_data:
            address.city = address_data.get('city', address.city)
            address.street = address_data.get('street', address.street)
            address.postal_code = address_data.get('postal_code', address.postal_code)
            address.latitude = address_data.get('latitude', address.latitude)
            address.latitude = address_data.get('latitude', address.longitude)
            address.save()

        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.pricing_unit = validated_data.get('pricing_unit', instance.pricing_unit)
        instance.capacity = validated_data.get('capacity', instance.capacity)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.rating_count = validated_data.get('rating_count', instance.rating_count)
        instance.available_from = validated_data.get('available_from', instance.available_from)
        instance.available_till = validated_data.get('available_till', instance.available_till)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()
        return instance


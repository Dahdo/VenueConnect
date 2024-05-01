from rest_framework import serializers
from venues.models import Venue, VenueImages


class VenueImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VenueImages
        fields = ['image']


class VenueSerializer(serializers.ModelSerializer):
    # images = VenueImagesSerializer(many=True, read_only=True)
    upload_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, write_only=True, use_url=False),
        required=False
    )
    class Meta:
        model = Venue
        fields = ['id', 'name', 'description', 'price', 'pricing_unit',
                   'capacity', 'rating', 'available','images','upload_images', 'latitude', 'longitude']
    
    def create(self, validated_data):
        uploaded_images = validated_data.get('upload_images', [])
        venue = Venue.objects.create(**validated_data)
        venue.save()
        for image in uploaded_images:
            VenueImages.objects.create(venue=venue, image=image)
        return venue
    
    def update(self, instance, validated_data):
        if 'upload_images' in validated_data:
            instance.images.all().delete() # Delete existing images
            uploaded_images = validated_data.pop('upload_images')
            for image in uploaded_images:
                VenueImages.objects.create(venue=instance, image=image)

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


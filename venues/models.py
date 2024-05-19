from django.db import models
from users.models import CustomUser
from uuid import uuid4
import os


class Address(models.Model):
    city = models.CharField(max_length=100, blank=True, null=True)
    street = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.user.get_full_name()


class Venue(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(CustomUser, related_name='venue', on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField()
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=5)
    rating_count = models.IntegerField(null=True, blank=True)
    address = models.ForeignKey(Address, related_name='venue', on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_reviews(self):
        from booking.models import Review
        return Review.objects.filter(booking__venue=self)

def image_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"venue_{instance.venue.id}_{uuid4()}.{ext}"
    return os.path.join('venues', filename)

class VenueImages(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=image_upload_to)
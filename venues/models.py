from django.db import models
from users.models import CustomUser

class Address(models.Model):
    city = models.CharField(max_length=100, blank=True, null=True)
    street = models.CharField(max_length=100, blank=True, null=True)
    apartment = models.CharField(max_length=100, blank=True, null=True)
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
    PRICING_CHOICES = (
        ('day', 'Per Day'),
        ('week', 'Per Week'),
        ('month', 'Per Month'),
    )
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(CustomUser, related_name='venue', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pricing_unit = ricing_unit = models.CharField(max_length=10, choices=PRICING_CHOICES, default='day')
    capacity = models.IntegerField()
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    rating_count = models.IntegerField()
    picture = models.ImageField(upload_to='venue', blank=True, null=True)
    available = models.BooleanField(default=True)
    address = models.ForeignKey(Address, related_name='venue', on_delete=models.NULL)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def picture_url(self):
        try:
            url = self.avatar.url
        except:
            url = ''
        return url
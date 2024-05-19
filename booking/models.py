from django.db import models
from users.models import CustomUser
from venues.models import Venue
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class Bookings(models.Model):
    STATE_CHOICES = (
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookings')
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='bookings')
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='active')
    number_of_guests = models.IntegerField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    check_in = models.DateTimeField(null=True)
    check_out = models.DateTimeField(null=True)
    review = models.TextField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=5)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.venue.name} - {self.check_in} to {self.check_out}"
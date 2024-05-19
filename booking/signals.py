from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Bookings

@receiver(post_save, sender=Bookings)
def update_booking_state(sender, instance, **kwargs):
    # Check if the booking's state is 'active' and the check_out time has passed
    if instance.state == 'active' and instance.check_out <= timezone.now():
        # Prevent recursive signal calls
        instance.state = 'completed'
        instance.save(update_fields=['state'])

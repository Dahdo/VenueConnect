from django.utils import timezone
from .models import Bookings

def update_bookings_state():
    now = timezone.now()
    bookings = Bookings.objects.filter(state='active', check_out__lte=now)
    for booking in bookings:
        booking.state = 'completed'
        booking.save(update_fields=['state'])
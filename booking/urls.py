from django.urls import path
from .views import UserBookingListView, BookingListView, BookingDetailView, BookingCancelView, BookingCompleteView, BookingDeleteView

urlpatterns = [
    # Endpoint to get all bookings for a specific user
    path('bookings/user/<int:user_id>/', UserBookingListView.as_view(), name='user-booking-list'),

    # Endpoint to post, get all bookings (for admins only)
    path('bookings/', BookingListView.as_view(), name='booking-list'),

    # Endpoint to get, update a specific booking for a specific user
    path('bookings/<int:booking_id>/user/<int:user_id>/', BookingDetailView.as_view(), name='booking-detail'),

    # Endpoint to cancel a specific booking
    path('bookings/<int:booking_id>/cancel/', BookingCancelView.as_view(), name='booking-cancel'),

    # Endpoint to mark a specific booking as completed
    path('bookings/<int:booking_id>/complete/', BookingCompleteView.as_view(), name='booking-complete'),

    # Endpoint to delete a specific booking (need to be an admin)
    path('bookings/<int:booking_id>/delete/', BookingDeleteView.as_view(), name='bookings-delete')
]
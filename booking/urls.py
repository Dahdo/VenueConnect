from django.urls import path
from .views import UserBookingsListView, BookingsListView, BookingDetailView, BookingsCancelView, BookingsCompleteView, BookingDeleteView

urlpatterns = [
    # Endpoint to get all bookings for a specific user
    path('bookings/user/<int:user_id>/', UserBookingsListView.as_view(), name='user-bookings-list'),

    # Endpoint to post, get all bookings (for admins only)
    path('bookings/', BookingsListView.as_view(), name='bookings-list'),

    # Endpoint to get, update a specific bookings for a specific user
    path('bookings/<int:booking_id>/user/<int:user_id>/', BookingDetailView.as_view(), name='bookings-detail'),

    # Endpoint to cancel a specific bookings
    path('bookings/<int:booking_id>/cancel/', BookingsCancelView.as_view(), name='bookings-cancel'),

    # Endpoint to mark a specific bookings as completed
    path('bookings/<int:booking_id>/complete/', BookingsCompleteView.as_view(), name='bookings-complete'),

    # Endpoint to delete a specific bookings (need to be an admin)
    path('bookings/<int:booking_id>/delete/', BookingDeleteView.as_view(), name='bookings-delete')
]
from django.urls import path
from .views import *
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

    # Endpoint to mark a specific bookings as active
    path('bookings/<int:booking_id>/activate/', BookingsActivateView.as_view(), name='bookings-activate'),

    # Endpoint to delete a specific bookings (need to be an admin)
    path('bookings/<int:booking_id>/delete/', BookingDeleteView.as_view(), name='bookings-delete'),

    # Endpoint to retrieve all venue owner's booking grouped by venues
    path('bookings/venue-owner/<int:venue_owner_id>/', OwnerVenueBookings.as_view(), name='bookings-owner'),

    # Endpoint to retrieve all active venue owner's booking grouped by venues
    path('bookings/venue-owner/<int:venue_owner_id>/active/', OwnerVenueBookingsActive.as_view(), name='bookings-owner-active'),

     # Endpoint to retrieve all cancelled venue owner's booking grouped by venues
    path('bookings/venue-owner/<int:venue_owner_id>/cancelled/', OwnerVenueBookingsCancelled.as_view(), name='bookings-owner-cancelled'),

     # Endpoint to retrieve all completed venue owner's booking grouped by venues
    path('bookings/venue-owner/<int:venue_owner_id>/completed/', OwnerVenueBookingsCompleted.as_view(), name='bookings-owner-completed'),
]
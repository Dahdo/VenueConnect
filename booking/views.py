from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Bookings
from .serializers import BookingsSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.core.exceptions import ValidationError
from venues.models import Venue
from venues.serializers import VenueSerializer

class UserBookingsListView(APIView): # Get all for a specific user
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        bookings = Bookings.objects.filter(user_id=user_id)
        serializer = BookingsSerializer(bookings, many=True)
        return Response(serializer.data)
    
class BookingsListView(APIView): # for all users
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = Bookings.objects.all()
        serializer = BookingsSerializer(bookings, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = BookingsSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
            except ValidationError as e:
                return Response(e, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.http import Http404 
class BookingDetailView(APIView):  # for a specific user and bookings
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id, booking_id):
        try:
            bookings = Bookings.objects.get(user_id=user_id, id=booking_id)
        except Bookings.DoesNotExist:
            raise Http404("booking does not exist")

        serializer = BookingsSerializer(bookings)
        return Response(serializer.data)

    def put(self, request, user_id, booking_id):
        try:
            bookings = Bookings.objects.get(user_id=user_id, id=booking_id)
        except Bookings.DoesNotExist:
            raise Http404("booking does not exist")

        serializer = BookingsSerializer(bookings, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class BookingsCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, booking_id):
        bookings = get_object_or_404(Bookings, pk=booking_id)
        bookings.state = 'cancelled'
        bookings.save()
        serializer = BookingsSerializer(bookings)
        return Response(serializer.data)

class BookingsCompleteView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, booking_id):
        bookings = get_object_or_404(Bookings, pk=booking_id)
        bookings.state = 'completed'
        bookings.save()
        serializer = BookingsSerializer(bookings)
        return Response(serializer.data)

class BookingsActivateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, booking_id):
        bookings = get_object_or_404(Bookings, pk=booking_id)
        bookings.state = 'active'
        bookings.save()
        serializer = BookingsSerializer(bookings)
        return Response(serializer.data)
    
class BookingDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, booking_id):
        bookings = get_object_or_404(Bookings, pk=booking_id)
        bookings.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class OwnerVenueBookings(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, venue_owner_id):
        venues = Venue.objects.filter(owner_id=venue_owner_id)
        results = {}
        for venue in venues:
            bookings = Bookings.objects.filter(venue_id=venue.id)
            if bookings.exists():
                bookings_serializer = BookingsSerializer(bookings, many=True)
                results[venue.id] = bookings_serializer.data
        return Response(results)

class OwnerVenueBookingsCancelled(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, venue_owner_id):
        venues = Venue.objects.filter(owner_id=venue_owner_id)
        results = {}
        for venue in venues:
            bookings = Bookings.objects.filter(venue_id=venue.id, state='cancelled')
            if bookings.exists():
                bookings_serializer = BookingsSerializer(bookings, many=True)
                results[venue.id] = bookings_serializer.data
        return Response(results)

class OwnerVenueBookingsActive(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, venue_owner_id):
        venues = Venue.objects.filter(owner_id=venue_owner_id)
        results = {}
        for venue in venues:
            bookings = Bookings.objects.filter(venue_id=venue.id, state='active')
            if bookings.exists():
                bookings_serializer = BookingsSerializer(bookings, many=True)
                results[venue.id] = bookings_serializer.data
        return Response(results)

class OwnerVenueBookingsCompleted(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, venue_owner_id):
        venues = Venue.objects.filter(owner_id=venue_owner_id)
        results = {}
        for venue in venues:
            bookings = Bookings.objects.filter(venue_id=venue.id, state='completed')
            if bookings.exists():
                bookings_serializer = BookingsSerializer(bookings, many=True)
                results[venue.id] = bookings_serializer.data
        return Response(results)
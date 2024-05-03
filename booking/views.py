from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Booking
from .serializers import BookingSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class UserBookingListView(APIView): # Get all for a specific user
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        bookings = Booking.objects.filter(user_id=user_id)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
    
class BookingListView(APIView): # for all users
    permission_classes = [IsAdminUser]

    def get(self, request):
        bookings = Booking.objects.all()
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

from django.http import Http404 
class BookingDetailView(APIView):  # for a specific user and booking
    def get(self, request, user_id, booking_id):
        try:
            booking = Booking.objects.get(user_id=user_id, id=booking_id)
        except Booking.DoesNotExist:
            raise Http404("Booking does not exist")

        serializer = BookingSerializer(booking)
        return Response(serializer.data)

    def put(self, request, user_id, booking_id):
        try:
            booking = Booking.objects.get(user_id=user_id, id=booking_id)
        except Booking.DoesNotExist:
            raise Http404("Booking does not exist")

        serializer = BookingSerializer(booking, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class BookingCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, booking_id):
        booking = get_object_or_404(Booking, pk=booking_id)
        booking.state = 'cancelled'
        booking.save()
        serializer = BookingSerializer(booking)
        return Response(serializer.data)

class BookingCompleteView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, booking_id):
        booking = get_object_or_404(Booking, pk=booking_id)
        booking.state = 'completed'
        booking.save()
        serializer = BookingSerializer(booking)
        return Response(serializer.data)
    
class BookingDeleteView(APIView):
    permission_classes = [IsAdminUser]
    def delete(self, request, booking_id):
        booking = get_object_or_404(Booking, pk=booking_id)
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Bookings
from .serializers import BookingsSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser

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
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

from django.http import Http404 
class BookingDetailView(APIView):  # for a specific user and bookings
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id, booking_id):
        try:
            bookings = Bookings.objects.get(user_id=user_id, id=booking_id)
        except Bookings.DoesNotExist:
            raise Http404("bookings does not exist")

        serializer = BookingsSerializer(bookings)
        return Response(serializer.data)

    def put(self, request, user_id, booking_id):
        try:
            bookings = Bookings.objects.get(user_id=user_id, id=booking_id)
        except Bookings.DoesNotExist:
            raise Http404("bookings does not exist")

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
    
class BookingDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, booking_id):
        bookings = get_object_or_404(Bookings, pk=booking_id)
        bookings.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

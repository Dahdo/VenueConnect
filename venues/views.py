from rest_framework import status
from django.http import Http404
from rest_framework.response import Response
from venues.serializers import VenueSerializer
from rest_framework import viewsets
from venues.models import Venue
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.filters import BaseFilterBackend
from datetime import datetime
from django.db.models import Q
from .permissions import VenuePermissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

class BookingsRangeFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        check_in = request.query_params.get('check_in')
        check_out = request.query_params.get('check_out')

        if check_in and check_out:
            check_in_datetime = datetime.strptime(check_in, '%Y-%m-%dT%H:%M:%S')
            check_out_datetime = datetime.strptime(check_out, '%Y-%m-%dT%H:%M:%S')
            queryset = queryset.exclude(
                bookings__check_in__lt=check_out_datetime,
                bookings__check_out__gt=check_in_datetime,
                bookings__state='active'
            )

        return queryset

class VenueViewset(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [VenuePermissions]
    parser_class = [MultiPartParser, FormParser]

    # For filter/search
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter, BookingsRangeFilterBackend]
    filterset_fields = {
        'price': ['gte', 'lte'],
        'capacity': ['gte', 'lte'],
        'rating': ['gte'],
        'address__city': ['exact']
    }
    search_fields = ['name', 'description', 'address__city']
    ordering_fields = ['price', 'rating', 'capacity']

    
    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset
    
    def get_object(self, pk):
        try:
            return Venue.objects.get(pk=pk)
        except Venue.DoesNotExist:
            raise Http404
    
    def list(self, request):
        # Check if there are any query parameters
        if not request.query_params:
            venues = Venue.objects.all()
        else:
            venues = self.filter_queryset(Venue.objects.all())
        paginator = PageNumberPagination()
        paginator.page_size = 12
        venues_page = paginator.paginate_queryset(venues, request)
        serializer = VenueSerializer(venues_page, context={'request': request}, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def create(self, request):
        serializer = VenueSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def retrieve(self, request, pk=None):
        venue = self.get_object(pk)
        serializer = VenueSerializer(venue, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        venue = self.get_object(pk)
        self.check_object_permissions(request, venue) # Enforce object level permissions checking
        serializer = VenueSerializer(venue, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        venue = self.get_object(pk)
        self.check_object_permissions(request, venue) # Enforce object level permissions checking
        serializer = VenueSerializer(venue, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        venue = self.get_object(pk)
        self.check_object_permissions(request, venue) # Enforce object level permissions checking
        venue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'], url_path='owner/(?P<owner_id>[^/.]+)', permission_classes = [IsAuthenticated])
    def list_by_owner(self, request, owner_id=None):
        venues = Venue.objects.filter(owner_id=owner_id)
        paginator = PageNumberPagination()
        paginator.page_size = 12
        venues_page = paginator.paginate_queryset(venues, request)
        serializer = VenueSerializer(venues_page, context={'request': request}, many=True)
        return paginator.get_paginated_response(serializer.data)
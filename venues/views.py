from rest_framework import status
from django.http import Http404
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from venues.serializers import VenueSerializer
from rest_framework import viewsets
from venues.models import Venue
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.filters import BaseFilterBackend
from datetime import datetime


class VenueViewset(viewsets.ViewSet):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [UserPermissions]
    parser_class = [MultiPartParser, FormParser]
    
    def get_object(self, pk):
        try:
            return Venue.objects.get(pk=pk)
        except Venue.DoesNotExist:
            raise Http404
    
    def list(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 12
        venues = paginator.paginate_queryset(Venue.objects.all(), request)
        serializer = VenueSerializer(venues, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)
    
    def create(self, request):
        serializer = VenueSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def retrieve(self, request, pk=None):
        venue = self.get_object(pk)
        # self.check_object_permissions(request, venue) # Enforce object level permissions checking
        serializer = VenueSerializer(venue, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        venue = self.get_object(pk)
        # self.check_object_permissions(request, venue) # Enforce object level permissions checking
        serializer = VenueSerializer(venue, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        venue = self.get_object(pk)
        # self.check_object_permissions(request, venue) # Enforce object level permissions checking
        serializer = VenueSerializer(venue, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        venue = self.get_object(pk)
        # self.check_object_permissions(request, venue) # Enforce object level permissions checking
        # Deleting the associated user deletes the profile automatically
        venue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AvailabilityRangeFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')

        if start_time and end_time:
            start_datetime = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S')
            end_datetime = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S')
            queryset = queryset.filter(
                availability__start_time__lte=start_datetime,
                availability__end_time__gte=end_datetime
            )
        
        return queryset

class VenueSearchFilter(viewsets.ViewSet):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter, AvailabilityRangeFilterBackend]
    filterset_fields = {
        'price': ['gte', 'lte'],
        'capacity': ['gte', 'lte'],
        'rating': ['gte'],
        'address__city': ['exact']
    }
    search_fields = ['name', 'description', 'address__city']
    ordering_fields = ['price']

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset
    
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
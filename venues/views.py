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
from rest_framework import status
from django.http import Http404
from rest_framework.response import Response
from users.models import Profile
from users.serializers import ProfileSerializer
from rest_framework.reverse import reverse
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from users.serializers import UserRegistrationSerializer
from rest_framework import viewsets


class ProfileViewSet(viewsets.ViewSet):
    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404
        
    def list(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)
    
    # No Post method needed since for each user created, an associated profile is created automatically
    
    def retrieve(self, request, pk=None):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def update(self, request, pk=None):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        profile = self.get_object(pk)
        # Deleting the associated user deletes the profile automatically
        profile.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






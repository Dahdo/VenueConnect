from rest_framework import status
from django.http import Http404
from rest_framework.response import Response
from users.models import Profile, CustomUser
from users.serializers import ProfileSerializer
from rest_framework.reverse import reverse
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from users.serializers import UserRegistrationSerializer
from rest_framework import viewsets
from users.permissions import UserPermissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import MultiPartParser, FormParser


class ProfileViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [UserPermissions]
    parser_classes = (MultiPartParser, FormParser)
    
    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk).profile # Get the profile associated with the user pk
        except Profile.DoesNotExist:
            raise Http404
        
    def list(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, context={'request': request}, many=True)
        return Response(serializer.data)
    
    # No Post method needed since for each user created, an associated profile is created automatically
    
    def retrieve(self, request, pk=None):
        profile = self.get_object(pk)
        self.check_object_permissions(request, profile) # Enforce object level permissions checking
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        profile = self.get_object(pk)
        self.check_object_permissions(request, profile) # Enforce object level permissions checking
        serializer = ProfileSerializer(profile, context={'request': request}, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        profile = self.get_object(pk)
        self.check_object_permissions(request, profile) # Enforce object level permissions checking
        serializer = ProfileSerializer(profile,context={'request': request}, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        profile = self.get_object(pk)
        self.check_object_permissions(request, profile) # Enforce object level permissions checking
        # Deleting the associated user deletes the profile automatically
        profile.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class RegistrationViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # Ensure that the username is provided and non-empty
            if not serializer.validated_data.get('username'):
                return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class LoginViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    def create(self, request):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'id': user.id})
        else:
            return Response({'error': 'Invalid credentials'}, status=401)


class LogoutViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    def create(self, request):
        token = request.headers.get('Authorization').split()[1]
        try:
            Token.objects.get(key=token).delete()
            return Response({'success': 'User logged out successfully'}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

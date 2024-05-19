from rest_framework import permissions    

class VenuePermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.is_authenticated
        else:
            return True

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        elif view.action in ['update', 'partial_update', 'destroy']:
            return obj.owner == request.user or request.user.is_superuser
        else:
            return True
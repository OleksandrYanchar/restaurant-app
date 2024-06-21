from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Custom permission to only allow owners of a restaurant to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the requesting user is an owner of the restaurant.
        return obj.restaurant.owner == request.user

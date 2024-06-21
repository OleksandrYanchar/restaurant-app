from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Custom permission to only allow owners of a restaurant to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the requesting user is an owner of the restaurant.
        return obj.employee_set.filter(user=request.user, role='owner').exists()


class IsOwnerOrAdmin(BasePermission):
    """
    Custom permission to only allow owners or admins of a restaurant to add employees.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the requesting user is an owner or admin of the restaurant.
        return obj.employee_set.filter(user=request.user, role__in=['owner', 'admin']).exists()
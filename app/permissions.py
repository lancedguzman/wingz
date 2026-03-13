from rest_framework.permissions import BasePermission

class IsAdminRole(BasePermission):
    """
    Allows access only to users where role == 'admin'.
    """
    message = "Access denied. Admin role required."

    def has_permission(self, request, view):
        # Check if the user was successfully authenticated and has the 'admin' role
        return bool(
            request.user and 
            getattr(request.user, 'role', None) == 'admin'
        )

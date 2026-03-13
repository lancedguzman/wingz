from rest_framework import authentication
from rest_framework import exceptions
from .models import User

class CustomHeaderAuthentication(authentication.BaseAuthentication):
    """
    Custom authentication to identify the user from our custom User model.
    Expects a header like: 'X-User-Id: 1'
    """
    def authenticate(self, request):
        # Django automatically prefixes custom headers with HTTP_ and converts hyphens to underscores
        user_id = request.META.get('HTTP_X_USER_ID')
        
        if not user_id:
            return None  # Authentication not attempted

        try:
            user = User.objects.get(id_user=user_id)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid user ID provided.')

        # DRF expects a tuple of (user, auth)
        return (user, None)

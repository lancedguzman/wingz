from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RideViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'rides', RideViewSet, basename='ride')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('api/', include(router.urls)),
]

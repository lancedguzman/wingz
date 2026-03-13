from django.utils import timezone
from datetime import timedelta
from django.db.models import Prefetch, F
from django.db.models.functions import Sqrt, Power
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Ride, RideEvent
from .serializers import RideSerializer

class RideViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A ViewSet for viewing ride instances.
    Provides list and retrieve actions.
    """
    serializer_class = RideSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    
    # Support filtering Ride status, Rider email
    filterset_fields = ['status', 'id_rider__email']
    
    # Support for sorting by pickup_time
    ordering_fields = ['pickup_time', 'distance'] 

    def get_queryset(self):
        # 1. Calculate 24 hours ago
        twenty_four_hours_ago = timezone.now() - timedelta(hours=24)

        # 2. Setup the Advanced Prefetch for 'todays_ride_events'
        # This executes Query #2 and binds it to the 'todays_ride_events' attribute
        events_prefetch = Prefetch(
            'events', # Matches the related_name we set in models.py
            queryset=RideEvent.objects.filter(created_at__gte=twenty_four_hours_ago),
            to_attr='todays_ride_events'
        )

        # 3. Base Queryset (Executes Query #1 for the Rides/Users and the Pagination Count)
        queryset = Ride.objects.select_related(
            'id_rider', 'id_driver'
        ).prefetch_related(
            events_prefetch
        )

        # 4. Handle Distance Calculation & Sorting
        # Expected query params: ?lat=37.77&lon=-122.41&ordering=distance
        lat = self.request.query_params.get('lat')
        lon = self.request.query_params.get('lon')

        if lat and lon:
            try:
                lat = float(lat)
                lon = float(lon)
                # Annotate the queryset with the mathematical distance
                # This pushes the math to the database, keeping it highly performant
                queryset = queryset.annotate(
                    distance=Sqrt(
                        Power(F('pickup_latitude') - lat, 2) + 
                        Power(F('pickup_longitude') - lon, 2)
                    )
                )
            except ValueError:
                # If lat/lon aren't valid floats, just ignore the distance annotation
                pass

        return queryset

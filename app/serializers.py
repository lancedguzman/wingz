from rest_framework import serializers
from .models import Ride, User, RideEvent

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model, exposing only relevant fields."""
    class Meta:
        model = User
        fields = [
            'id_user', 'role',
            'first_name', 'last_name',
            'email', 'phone_number'
        ]

class RideEventSerializer(serializers.ModelSerializer):
    """Serializer for the RideEvent model, exposing relevant fields."""
    class Meta:
        model = RideEvent
        fields = ['id_ride_event', 'description', 
                  'created_at']

class RideSerializer(serializers.ModelSerializer):
    """Serializer for the Ride model, including nested User and RideEvent serializers."""
    # Map the foreign keys to the nested User serializers
    rider = UserSerializer(source='id_rider', read_only=True)
    driver = UserSerializer(source='id_driver', read_only=True)
    
    # This will map to the dynamically prefetched attribute
    todays_ride_events = RideEventSerializer(many=True, read_only=True)

    class Meta:
        model = Ride
        fields = [
            'id_ride', 'status', 'pickup_latitude', 
            'pickup_longitude', 'dropoff_latitude',
            'dropoff_longitude', 'pickup_time', 
            'rider', 'driver', 'todays_ride_events'
        ]

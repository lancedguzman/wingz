from django.db import models

class User(models.Model):
    """Model representing a user in the ride-sharing application."""
    id_user = models.AutoField(primary_key=True) 
    role = models.CharField(max_length=50)  # e.g., 'admin' 
    first_name = models.CharField(max_length=150) 
    last_name = models.CharField(max_length=150) 
    email = models.EmailField(unique=True) 
    phone_number = models.CharField(max_length=20) 

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"


class Ride(models.Model):
    """Model representing a ridein the ride-sharing application."""
    id_ride = models.AutoField(primary_key=True) 
    status = models.CharField(max_length=50) # e.g., 'en-route', 'pickup', 'dropoff' 
    
    # Using db_column to strictly match the requested 'id_rider' and 'id_driver' names
    id_rider = models.ForeignKey(User, related_name='rides_as_rider', on_delete=models.CASCADE, db_column='id_rider') 
    id_driver = models.ForeignKey(User, related_name='rides_as_driver', on_delete=models.CASCADE, db_column='id_driver') 
    
    pickup_latitude = models.FloatField() 
    pickup_longitude = models.FloatField() 
    dropoff_latitude = models.FloatField() 
    dropoff_longitude = models.FloatField() 
    pickup_time = models.DateTimeField() 

    def __str__(self):
        return f"Ride {self.id_ride} - {self.status}"

class RideEvent(models.Model):
    """Model representing an event related to a ride in the ride-sharing application."""
    id_ride_event = models.AutoField(primary_key=True) 
    id_ride = models.ForeignKey(Ride, related_name='events', on_delete=models.CASCADE, db_column='id_ride') 
    description = models.CharField(max_length=255) 
    created_at = models.DateTimeField() 

    class Meta:
        # Renaming the table to explicitly match the spec if desired
        db_table = 'Ride_Event'

    def __str__(self):
        return f"Event {self.id_ride_event} for Ride {self.id_ride_id}"

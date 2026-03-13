<template>
  <div class="ride-list-container">
    <h2>Wingz Ride List</h2>
    
    <div class="controls">
      <button @click="fetchRides">Refresh Rides</button>
    </div>

    <table v-if="rides.length">
      <thead>
        <tr>
          <th>Ride ID</th>
          <th>Status</th>
          <th>Pickup Time</th>
          <th>Rider Email</th>
          <th>Recent Events</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="ride in rides" :key="ride.id_ride">
          <td>{{ ride.id_ride }}</td>
          <td>{{ ride.status }}</td>
          <td>{{ new Date(ride.pickup_time).toLocaleString() }}</td>
          <td>{{ ride.rider_email }}</td>
          <td>{{ ride.todays_ride_events?.length || 0 }} events</td>
        </tr>
      </tbody>
    </table>
    <p v-else>Loading rides...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const rides = ref([]);

// Setup your Axios instance pointing to your Django backend
const api = axios.create({
  baseURL: 'http://localhost:8000/api/',
  // We'll add auth headers here later for the 'admin' requirement
});

const fetchRides = async () => {
  try {
    // You will implement pagination, filtering, and GPS sorting params here later
    const response = await api.get('rides/'); 
    rides.value = response.data.results; // Assuming DRF pagination
  } catch (error) {
    console.error("Error fetching rides:", error);
  }
};

onMounted(() => {
  fetchRides();
});
</script>

<style scoped>
/* Add some quick basic styling to make it readable */
table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
th { background-color: #f2f2f2; }
</style>

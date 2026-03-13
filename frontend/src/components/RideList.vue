<template>
  <div class="ride-list-container">
    <h2>Wingz Ride List</h2>

    <div class="controls">
      <div class="filter-group">
        <label>Status:</label>
        <select v-model="filters.status">
          <option value="">All</option>
          <option value="en-route">En-route</option>
          <option value="pickup">Pickup</option>
          <option value="dropoff">Dropoff</option>
        </select>
      </div>

      <div class="filter-group">
        <label>Rider Email:</label>
        <input type="text" v-model="filters.id_rider__email" placeholder="Search exact email..." />
      </div>

      <div class="filter-group">
        <label>Sort By:</label>
        <select v-model="filters.ordering">
          <option value="pickup_time">Pickup Time (Asc)</option>
          <option value="-pickup_time">Pickup Time (Desc)</option>
          <option value="distance">Distance to GPS (Closest)</option>
        </select>
      </div>

      <div class="filter-group" v-if="filters.ordering === 'distance'">
        <label>My GPS Lat:</label>
        <input type="number" step="0.01" v-model="filters.lat" placeholder="e.g. 37.77" />
        <label>My GPS Lon:</label>
        <input type="number" step="0.01" v-model="filters.lon" placeholder="e.g. -122.41" />
      </div>

      <button @click="fetchRides()">Apply & Fetch</button>
    </div>

    <table v-if="rides.length">
      <thead>
        <tr>
          <th>Ride ID</th>
          <th>Status</th>
          <th>Pickup Time</th>
          <th>Rider Email</th>
          <th>Recent Events (24h)</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="ride in rides" :key="ride.id_ride">
          <td>{{ ride.id_ride }}</td>
          <td>{{ ride.status }}</td>
          <td>{{ new Date(ride.pickup_time).toLocaleString() }}</td>
          <td>{{ ride.rider?.email || 'N/A' }}</td>
          <td>{{ ride.todays_ride_events?.length || 0 }} events</td>
        </tr>
      </tbody>
    </table>
    <p v-else-if="!loading">No rides found matching your criteria.</p>
    <p v-if="loading">Loading rides...</p>

    <div class="pagination" v-if="nextPage || prevPage">
      <button :disabled="!prevPage" @click="fetchRides(prevPage)">Previous</button>
      <button :disabled="!nextPage" @click="fetchRides(nextPage)">Next</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue';
import axios from 'axios';

const rides = ref([]);
const loading = ref(false);
const nextPage = ref(null);
const prevPage = ref(null);

// Reactive object to hold all our query parameters
const filters = reactive({
  status: '',
  id_rider__email: '',
  ordering: '-pickup_time',
  lat: '',
  lon: ''
});

// Setup Axios instance with the custom authentication header
const api = axios.create({
  baseURL: 'http://localhost:8000/api/',
  headers: {
    // Assuming a user with ID 1 exists in your DB and has role='admin'
    'X-User-Id': '1' 
  }
});

const fetchRides = async (url = 'rides/') => {
  loading.value = true;
  try {
    // If no specific pagination URL is passed, we build the query params from our filters
    let config = {};
    if (url === 'rides/') {
      // Clean up empty params so we don't send messy URLs to Django
      const params = Object.fromEntries(
        Object.entries(filters).filter(([_, v]) => v !== '')
      );
      config = { params };
    }

    const response = await api.get(url, config); 
    
    // Handle DRF PageNumberPagination format
    rides.value = response.data.results; 
    nextPage.value = response.data.next;
    prevPage.value = response.data.previous;

  } catch (error) {
    console.error("Error fetching rides:", error);
    if (error.response?.status === 403) {
      alert("Authentication failed: Ensure user ID 1 is an admin in your database.");
    }
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchRides();
});
</script>

<style scoped>
.ride-list-container { font-family: sans-serif; padding: 20px; }
.controls { display: flex; flex-wrap: wrap; gap: 15px; margin-bottom: 20px; padding: 15px; background: #f9f9f9; border-radius: 8px; }
.filter-group { display: flex; align-items: center; gap: 8px; }
table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
th { background-color: #f2f2f2; }
.pagination { margin-top: 20px; display: flex; gap: 10px; }
button { padding: 6px 12px; cursor: pointer; }
</style>
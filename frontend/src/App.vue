<template>
  <main>
    <RideList />
  </main>
</template>

<script setup>
// Adjust this path if your RideList.vue is saved somewhere else!
import RideList from './components/RideList.vue';
</script>

<style>
/* Optional: Adds a little breathing room to the app */
main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}
</style>

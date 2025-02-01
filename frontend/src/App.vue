<template>
  <v-app>
    <v-main class="main-content">
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
// Component logic here
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
  overflow: hidden;
}

.main-content {
  width: 100%;
  height: 100vh;
  max-width: 100vw;
}

.v-application {
  width: 100vw;
  min-height: 100vh;
}

:root {
  --v-layout-top: 0px !important;
}
</style>
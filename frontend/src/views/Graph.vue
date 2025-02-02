<template>
  <div class="graph-page">
    <div class="header">
      <h1>Network Visualization</h1>
      <p class="description">Interactive graph visualization of the network state</p>
    </div>
    <div class="graph-container">
      <GraphVisualization />
    </div>
  </div>
</template>

<script setup lang="ts">
import GraphVisualization from '../components/GraphVisualization.vue'
</script>

<style scoped>
.graph-page {
  padding: 24px;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f8f9fa;
}

.header {
  margin-bottom: 24px;
}

.header h1 {
  font-size: 24px;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.9);
  margin: 0;
}

.description {
  color: rgba(0, 0, 0, 0.6);
  margin: 8px 0 0 0;
}

.graph-container {
  flex: 1;
  min-height: 0;
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  padding: 16px;
}
</style> 
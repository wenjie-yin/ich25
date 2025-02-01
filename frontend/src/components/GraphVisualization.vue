<template>
  <div ref="sigmaContainer" class="sigma-container"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import Graph from 'graphology'
import Sigma from 'sigma'

const sigmaContainer = ref<HTMLElement | null>(null)
let sigma: any = null
let intervalId: number | null = null

// Multiple dummy states
const dummyStates = [
  [
    [0, 1, 0, 1, 0],
    [1, 0, 1, 0, 0],
    [0, 1, 0, 1, 1],
    [1, 0, 1, 0, 1],
    [0, 0, 1, 1, 0]
  ],
  [
    [0, 1, 1, 0, 0],
    [1, 0, 0, 1, 1],
    [1, 0, 0, 1, 0],
    [0, 1, 1, 0, 1],
    [0, 1, 0, 1, 0]
  ],
  [
    [0, 0, 1, 1, 1],
    [0, 0, 1, 0, 1],
    [1, 1, 0, 0, 0],
    [1, 0, 0, 0, 1],
    [1, 1, 0, 1, 0]
  ]
]

const updateGraph = (matrix: number[][]) => {
  const graph = new Graph()
  const n = matrix.length
  const radius = 5

  // Create nodes in a circle
  for (let i = 0; i < n; i++) {
    const angle = (i * 2 * Math.PI) / n
    const x = radius * Math.cos(angle)
    const y = radius * Math.sin(angle)
    
    graph.addNode(`n${i}`, {
      x,
      y,
      size: 8,
      label: `Node ${i}`,
      color: '#1a73e8'
    })
  }

  // Add edges based on matrix
  for (let i = 0; i < n; i++) {
    for (let j = i + 1; j < n; j++) {
      if (matrix[i][j] === 1) {
        graph.addEdge(`n${i}`, `n${j}`, {
          size: 2,
          color: '#666'
        })
      }
    }
  }

  // Kill previous sigma instance if it exists
  if (sigma) {
    sigma.kill()
  }

  // Initialize new Sigma instance
  if (sigmaContainer.value) {
    sigma = new Sigma(graph, sigmaContainer.value, {
      defaultNodeColor: '#999',
      defaultEdgeColor: '#ccc',
      renderEdgeLabels: false,
      minCameraRatio: 0.2,
      maxCameraRatio: 2,
    })
  }
}

onMounted(() => {
  let currentStateIndex = 0
  
  // Initial graph
  updateGraph(dummyStates[currentStateIndex])

  // Update graph every 3 seconds
  intervalId = window.setInterval(() => {
    currentStateIndex = (currentStateIndex + 1) % dummyStates.length
    updateGraph(dummyStates[currentStateIndex])
  }, 3000)
})

onUnmounted(() => {
  if (sigma) {
    sigma.kill()
  }
  if (intervalId !== null) {
    clearInterval(intervalId)
  }
})
</script>

<style scoped>
.sigma-container {
  width: 100%;
  height: 100%;
  background: #fff;
  border: 1px solid #eee;
  border-radius: 8px;
}
</style> 
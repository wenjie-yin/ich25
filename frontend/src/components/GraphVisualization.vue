<template>
  <div ref="sigmaContainer" class="sigma-container"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import Graph from 'graphology'
import Sigma from 'sigma'

const props = defineProps<{
  beliefs: number[]
  matrix: number[][]
}>()

const sigmaContainer = ref<HTMLElement | null>(null)
let sigma: any = null
let previousCamera = { x: 0, y: 0, ratio: 1 }

// Helper function to convert belief value to color
const beliefToColor = (belief: number): string => {
  // Ensure belief is between 0 and 1
  belief = Math.max(0, Math.min(1, belief))
  
  // Convert to RGB
  const r = Math.round(255 * (1 - belief))
  const g = Math.round(255 * belief)
  const b = 0
  
  return `rgb(${r}, ${g}, ${b})`
}

const updateGraph = () => {
  const graph = new Graph()
  const n = props.matrix.length
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
      label: `Node ${i} (${props.beliefs[i].toFixed(2)})`,
      color: beliefToColor(props.beliefs[i])
    })
  }

  // Add edges based on matrix
  for (let i = 0; i < n; i++) {
    for (let j = i + 1; j < n; j++) {
      if (props.matrix[i][j] === 1) {
        graph.addEdge(`n${i}`, `n${j}`, {
          size: 2,
          color: '#666'
        })
      }
    }
  }

  // Store current camera state if sigma exists
  if (sigma) {
    const camera = sigma.getCamera()
    previousCamera = {
      x: camera.x,
      y: camera.y,
      ratio: camera.ratio
    }
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

    // Restore previous camera state
    const camera = sigma.getCamera()
    camera.setState(previousCamera)
  }
}

// Watch for changes in props
watch(() => props.beliefs, updateGraph, { deep: true })
watch(() => props.matrix, updateGraph, { deep: true })

onMounted(() => {
  updateGraph()
})

onUnmounted(() => {
  if (sigma) {
    sigma.kill()
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
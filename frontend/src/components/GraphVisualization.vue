<template>
  <div ref="sigmaContainer" class="sigma-container">
    <canvas ref="particleCanvas" class="particle-canvas"></canvas>
  </div>

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
const particleCanvas = ref<HTMLCanvasElement | null>(null)
let sigma: any = null
let previousCamera = { x: 0.5, y: 0.5, ratio: 1.25 }
let animationFrameId: number | null = null
let particles: Array<{
  x: number
  y: number
  targetX: number
  targetY: number
  progress: number
  edge: [string, string]
}> = []

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

// Helper function to create a particle
const createParticle = (graph: any, edge: [string, string]) => {
  const sourceNode = graph.getNodeAttributes(edge[0])
  const targetNode = graph.getNodeAttributes(edge[1])
  return {
    x: sourceNode.x,
    y: sourceNode.y,
    targetX: targetNode.x,
    targetY: targetNode.y,
    progress: 0,
    edge
  }
}

// Animation function
const animateParticles = () => {
  if (!sigma || !particleCanvas.value) {
    animationFrameId = requestAnimationFrame(animateParticles)
    return
  }

  const ctx = particleCanvas.value.getContext('2d')
  if (!ctx) {
    animationFrameId = requestAnimationFrame(animateParticles)
    return
  }

  // Clear canvas while preserving transparency
  ctx.clearRect(0, 0, particleCanvas.value.width, particleCanvas.value.height)

  // Add new particles using current graph
  if (Math.random() < 0.1) {
    const edges = sigma.getGraph().edges()
    if (edges.length > 0) {
      const randomEdge = edges[Math.floor(Math.random() * edges.length)]
      const [source, target] = sigma.getGraph().extremities(randomEdge)
      const sourceIdx = parseInt(source.slice(1))
      const targetIdx = parseInt(target.slice(1))
      const weight = props.matrix[sourceIdx][targetIdx] || props.matrix[targetIdx][sourceIdx]
      
      if (Math.random() < weight) {
        particles.push(createParticle(sigma.getGraph(), [source, target]))
      }
    }
  }

  // Update and draw particles
  ctx.strokeStyle = 'rgba(255, 0, 0, 0.8)'
  ctx.fillStyle = 'rgba(255, 0, 0, 0.8)'
  ctx.lineWidth = 0.5

  particles = particles.filter(particle => {
    // Check if the edge still exists in the current graph
    const edgeExists = sigma.getGraph().hasEdge(particle.edge[0], particle.edge[1])
    if (!edgeExists) return false  // Remove particle if the edge no longer exists

    particle.progress += 0.02
    if (particle.progress >= 1) return false

    const currentX = particle.x + (particle.targetX - particle.x) * particle.progress
    const currentY = particle.y + (particle.targetY - particle.y) * particle.progress

    const screenCoords = sigma.graphToViewport({ x: currentX, y: currentY })
    ctx.beginPath()
    ctx.arc(screenCoords.x, screenCoords.y, 3, 0, Math.PI * 2)
    ctx.fill()

    return true
  })

  // Schedule next frame
  animationFrameId = requestAnimationFrame(animateParticles)
}

const updateGraph = () => {
  particles = []
  const graph = new Graph()
  const n = props.matrix.length
  const radius = 5

  // Ensure canvas size matches container
  if (particleCanvas.value && sigmaContainer.value) {
    particleCanvas.value.width = sigmaContainer.value.clientWidth
    particleCanvas.value.height = sigmaContainer.value.clientHeight
  }

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
      color: beliefToColor(props.beliefs[i]),
      labelSize: 14,
      labelColor: '#eee'
    })
  }

  // Add edges based on matrix
  for (let i = 0; i < n; i++) {
    for (let j = i + 1; j < n; j++) {
      const weight = props.matrix[i][j]
      if (weight > 0) {
        // Convert weight to grayscale (0 = black, 255 = white)
        const intensity = Math.round(255 * weight)
        const color = `rgb(${intensity}, ${intensity}, ${intensity})`
        graph.addEdge(`n${i}`, `n${j}`, {
          size: 2,
          color: color
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
  }

  // Cancel existing animation
  if (animationFrameId !== null) {
    cancelAnimationFrame(animationFrameId)
    animationFrameId = null
  }

  // Initialize new Sigma instance if it doesn't exist
  if (sigmaContainer.value) {
    if (!sigma) {
      sigma = new Sigma(graph, sigmaContainer.value, {
        defaultNodeColor: '#ccc',
        defaultEdgeColor: '#888',
        renderLabels: true,
        renderEdgeLabels: false,
        minCameraRatio: 0.2,
        maxCameraRatio: 2,
        labelColor: { color: '#eee' },
        labelSize: 14,
        labelWeight: 'bold'
      })

    } else {
      // Update the existing sigma instance with the new graph
      sigma.setGraph(graph)
    }

    // Restore previous camera state
    const camera = sigma.getCamera()
    camera.setState(previousCamera)

    // Start particle animation after Sigma renders
    const onRender = () => {
      animateParticles()
      sigma.off('afterRender', onRender)  // Remove listener after first render
    }
    sigma.on('afterRender', onRender)  // Wait for Sigma to complete initial render
  }
}

// Watch for changes in props
watch(() => props.beliefs, updateGraph, { deep: true })
watch(() => props.matrix, updateGraph, { deep: true })

onMounted(() => {
  // Set canvas size before initializing graph
  if (particleCanvas.value && sigmaContainer.value) {
    particleCanvas.value.width = sigmaContainer.value.clientWidth
    particleCanvas.value.height = sigmaContainer.value.clientHeight
  }
  updateGraph()
})

onUnmounted(() => {
  if (sigma) {
    sigma.kill()
  }
  if (animationFrameId !== null) {
    cancelAnimationFrame(animationFrameId)
  }
})
</script>

<style scoped>
.sigma-container {
  width: 100%;
  height: 100%;
  background: #1e1e1e;
  border: 1px solid #444;
  border-radius: 8px;
  position: relative; /* Ensure canvas is positioned correctly */
}

.particle-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none; /* Ensure canvas doesn't block interactions */
}
</style> 
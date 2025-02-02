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
      // Create a weighted edge set for random selection
      const weightedEdges = new Set()
      edges.forEach((edge: any) => {
        const [source, target] = sigma.getGraph().extremities(edge)
        const sourceIdx = parseInt(source.slice(1))
        const targetIdx = parseInt(target.slice(1))
        const weight = props.matrix[sourceIdx][targetIdx] || props.matrix[targetIdx][sourceIdx]
        
        // Add edge multiple times based on weight (0-1 maps to 0-10 entries)
        const entries = Math.round(weight * 10)
        for (let i = 0; i < entries; i++) {
          weightedEdges.add(edge)
        }
      })
      
      // Convert set back to array for random selection
      const edgeArray = Array.from(weightedEdges)
      const randomEdge = edgeArray[Math.floor(Math.random() * edgeArray.length)]
      const [source, target] = sigma.getGraph().extremities(randomEdge)
      particles.push(createParticle(sigma.getGraph(), [source, target]))
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
  // Define layout boundaries
  const margin = 2  // Keep some space from edges
  const width = 1  // Total width of layout space
  const height = 6  // Total height of layout space

  // Calculate positions based on beliefs
  const positions = []
  for (let i = 0; i < n; i++) {
    // X position based on belief (left to right)
    const x = margin + (width - 2 * margin) * props.beliefs[i]
    
    // Y position distributed evenly
    let y = margin + (height - 2 * margin) * (i / (n - 1))
    // Center y if only one node
    if (n === 1) y = height / 2
    
    // Offset alternate nodes for better edge visibility
    const xOffset = (i % 2) * 0.5
    positions.push({ x: x - width/2 + xOffset, y: y - height/2 })
  }

  // Apply force-directed layout
  const iterations = 50
  const springLength = 2
  const springStrength = 0.1
  
  for (let iter = 0; iter < iterations; iter++) {
    // Calculate forces
    const forces = positions.map(() => ({ x: 0, y: 0 }))
    
    // Apply spring forces based on connectivity weights
    for (let i = 0; i < n; i++) {
      for (let j = 0; j < n; j++) {
        if (i !== j) {
          const weight = props.matrix[i][j] || props.matrix[j][i] || 0
          if (weight > 0) {
            const dx = positions[j].x - positions[i].x
            const dy = positions[j].y - positions[i].y
            const distance = Math.sqrt(dx * dx + dy * dy)
            const force = (distance - springLength) * springStrength * weight
            
            // Limit horizontal movement to maintain belief-based positioning
            forces[i].x += (dx / distance) * force * 0.1  // Reduced horizontal force
            forces[i].y += (dy / distance) * force
            forces[j].x -= (dx / distance) * force * 0.1  // Reduced horizontal force
            forces[j].y -= (dy / distance) * force
          }
        }
      }
    }
    
    // Apply forces to positions
    for (let i = 0; i < n; i++) {
      positions[i].x += forces[i].x
      positions[i].y += forces[i].y
    }
  }

  // Create nodes with calculated positions
  for (let i = 0; i < n; i++) {
    graph.addNode(`n${i}`, {
      x: positions[i].x,
      y: positions[i].y,
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
        const color = `rgb(${intensity}, ${intensity}, ${intensity}, ${weight > 0 ? 1 : 0})`
        graph.addEdge(`n${i}`, `n${j}`, {
          size: 2,
          color: color
        })
      }
    }
  }

  // Ensure canvas size matches container
  if (particleCanvas.value && sigmaContainer.value) {
    particleCanvas.value.width = sigmaContainer.value.clientWidth
    particleCanvas.value.height = sigmaContainer.value.clientHeight
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
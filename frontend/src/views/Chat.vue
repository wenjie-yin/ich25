<template>
  <div class="chat-container">
    <!-- Title Bar -->
    <div class="title-bar">
      <h1>{{ belief }}</h1>
    </div>

    <div class="content-container">
      <!-- Left Column -->
      <div class="left-column">
        <!-- Message History -->
        <div class="message-history">
          <h2>Message History</h2>
          <div class="message-list">
            <div v-for="(message, index) in messages" :key="index" class="message-item">
              <div class="message-time">{{ message.time }}</div>
              <div class="messege-sender">Node_{{ message.sender }}</div>
              <div class="message-content">{{ message.content }}</div>
            </div>
          </div>
        </div>

        <!-- Message Input -->
        <div class="input-area">
          <div class="input-container">
            <t-textarea
              v-model="newMessage"
              placeholder="Message..."
              @keydown="handleKeydown"
            />
            <t-button 
              theme="primary" 
              class="send-button"
              :disabled="!newMessage.trim()"
              @click="sendMessage"
            >
              Send
            </t-button>
          </div>
        </div>
      </div>

      <!-- Right Column -->
      <div class="right-column">
        <!-- Graph Visualization -->
        <div class="graph-section">
          <GraphVisualization 
            :beliefs="worldState.belief_vector"
            :matrix="worldState.connectivity_matrix"
          />
        </div>

        <!-- Scoreboard -->
        <div class="scoreboard">
          <h2>Node Beliefs</h2>
          <div class="belief-list">
            <div v-for="(belief, index) in worldState.belief_vector" :key="index" class="belief-item">
              <div class="node-label">Node {{ index }}</div>
              <div class="belief-bar-container">
                <div 
                  class="belief-bar" 
                  :style="{ 
                    width: `${belief * 100}%`,
                    backgroundColor: beliefToColor(belief)
                  }"
                ></div>
                <span class="belief-value">{{ (belief * 100).toFixed(1) }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import axios from 'axios'
import { MessagePlugin } from 'tdesign-vue-next'
import GraphVisualization from '../components/GraphVisualization.vue'

interface Message {
  content: string
  time: string
  sender: string
}

interface WorldState {
  belief_vector: number[]
  connectivity_matrix: number[][]
  current_message: string
}

const belief = ref<String>('')
const userMessages = ref<Message[]>([])
const newMessage = ref('')
const messages = ref<Message[]>([])
const worldState = ref<WorldState>({
  belief_vector: [0, 0, 0, 0, 0],  // Initial state with 5 nodes
  connectivity_matrix: [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
  ],
  current_message: ''
})

let pollInterval: number | null = null

const beliefToColor = (belief: number): string => {
  belief = Math.max(0, Math.min(1, belief))
  const r = Math.round(255 * (1 - belief))
  const g = Math.round(255 * belief)
  const b = 0
  return `rgb(${r}, ${g}, ${b})`
}

// Helper function to format date to ISO-like format
const formatDateTime = (date: Date): string => {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  const seconds = String(date.getSeconds()).padStart(2, '0')
  const milliseconds = String(date.getMilliseconds()).padStart(3, '0')
  return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}.${milliseconds}`
}

const sendMessage = async () => {
  if (!newMessage.value.trim()) return

  try {
    const token = localStorage.getItem('token')
    if (!token) {
      MessagePlugin.error('Not authenticated')
      return
    }
    // Add message to history
    userMessages.value.unshift({
      content: newMessage.value.trim(),
      time: formatDateTime(new Date()),
      sender: 'Me'
    })
    
    messages.value.unshift({
      content: newMessage.value.trim(),
      time: formatDateTime(new Date()),
      sender: 'Me'
    })
    
    const m = newMessage.value.trim()

    // Clear input after successful send
    newMessage.value = ''
    await axios.post('http://0.0.0.0:8000/chat', 
      { message: m },
      {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      }
    )

    

  } catch (error: any) {
    console.error('Chat error:', error)
    if (error.response?.status === 401) {
      MessagePlugin.error('Session expired. Please login again.')
    } else {
      MessagePlugin.error('Failed to send message')
    }
  }
}

const fetchWorldState = async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) return

    const response = await axios.get('http://0.0.0.0:8000/world', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    worldState.value = response.data
    const feeds = response.data.feed
    messages.value = feeds.filter((feed: any) => feed.sender).map((feed: any) => ({
      content: feed.message,
      time: feed.timestamp,
      sender: feed.sender
    }))
    // Merge and sort userMessages with messages from the feed
    messages.value = [...messages.value, ...userMessages.value].sort((a, b) => {
      return (new Date(b.time).getTime() - new Date(a.time).getTime())
    })
  } catch (error) {
    console.error('Failed to fetch world state:', error)
    // Keep previous state on error
  }
}

const handleKeydown = (e: KeyboardEvent) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    sendMessage()
  }
}

const fetchBelief = async () => {
  const token = localStorage.getItem('token')
  if (!token) return

  const response = await axios.get('http://0.0.0.0:8000/belief', {
    headers: { 'Authorization': `Bearer ${token}` }
  })
  belief.value = response.data.belief
}

onMounted(() => {
  // Fetch initial state
  fetchWorldState()
  fetchBelief()
  
  // Start polling every 3 seconds
  pollInterval = window.setInterval(fetchWorldState, 3000)
})

onUnmounted(() => {
  if (pollInterval !== null) {
    clearInterval(pollInterval)
  }
})
</script>

<style scoped>
/* Reset any default margins that might cause scrolling */
:deep(*) {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #121212;
  padding: 16px;
  box-sizing: border-box;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
  color: #eee;
}

.title-bar {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0 16px;
  height: 64px;
  background: #1e1e1e;
  border-radius: 12px;
  margin-bottom: 16px;
}

.title-bar h1 {
  font-size: 24px;
  font-weight: 600;
  color: #eee;
  margin: 0;
}

/* Main content container */
.content-container {
  display: flex;
  gap: 24px;
  flex: 1;
  min-height: 0;
}

.left-column {
  width: 400px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-height: 0;
}

.right-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-width: 0;
  height: 100%;
  min-height: 0;
}

.message-history {
  flex: 1;
  background: #1e1e1e;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  padding: 16px;
  display: flex;
  flex-direction: column;
  min-height: 0; /* Allow container to shrink */
}

.message-history h2 {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 16px 0;
  color: #eee;
}

.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 0 16px;
  margin: 0 -16px;
  min-height: 0;
}

.message-item {
  padding: 12px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.message-time {
  font-size: 12px;
  color: #eee;
  margin-bottom: 4px;
}

.message-content {
  font-size: 14px;
  color: #eee;
  white-space: pre-wrap;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.input-area {
  background: #1e1e1e;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  padding: 16px;
  height: 120px; /* Fixed height for input area */
  display: flex;
  flex-direction: column;
}

.input-container {
  position: relative;
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.graph-section {
  flex: 2;
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden; /* Ensure graph doesn't overflow */
}

.scoreboard {
  /* flex: 1;  */
  background: #1e1e1e;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  padding: 16px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.scoreboard h2 {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 16px 0;
  color: #eee;
}

.belief-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.belief-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.node-label {
  flex: 0 0 80px;
  font-size: 14px;
  color: #eee;
}

.belief-bar-container {
  flex: 1;
  height: 24px;
  background: #f0f0f0;
  border-radius: 4px;
  position: relative;
  overflow: hidden;
}

.belief-bar {
  height: 100%;
  transition: width 0.3s ease, background-color 0.3s ease;
}

.belief-value {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 12px;
  color: black;
}

:deep(.t-textarea) {
  background-color: #ffffff;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  padding: 8px 64px 8px 16px;
  font-size: 14px;
  line-height: 1.5;
}

.send-button {
  position: absolute;
  right: 8px;
  bottom: 8px;
  background-color: #000000;
  border: none;
  padding: 4px 12px;
  border-radius: 6px;
  font-size: 14px;
}

:deep(.send-button:hover:not(:disabled)) {
  background-color: #2d2d2d !important;
}

:deep(.send-button:disabled) {
  background-color: rgba(0, 0, 0, 0.1) !important;
}
</style> 
<template>
  <div class="chat-container">
    <div class="chat-content">
      <div class="messages" ref="messagesContainer">
        <div v-for="(message, index) in messages" :key="index" class="message" :class="message.role">
          <div class="message-content">
            <t-avatar class="avatar" :image="message.role === 'user' ? userAvatar : botAvatar" />
            <div class="text">{{ message.content }}</div>
          </div>
        </div>
      </div>
      
      <div class="input-area">
        <div class="input-container">
          <t-textarea
            v-model="newMessage"
            placeholder="Message..."
            :autosize="{ minRows: 1, maxRows: 5 }"
            @keydown.enter.prevent="sendMessage"
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
        <div class="input-footer">
          Free Research Preview. ChatGPT may produce inaccurate information.
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

const messages = ref<Message[]>([
  {
    role: 'assistant',
    content: 'Hello! How can I help you today?'
  }
])

const newMessage = ref('')
const messagesContainer = ref<HTMLElement | null>(null)
const userAvatar = 'https://api.dicebear.com/7.x/avataaars/svg?seed=user'
const botAvatar = 'https://api.dicebear.com/7.x/bottts/svg?seed=gpt'

const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const sendMessage = async () => {
  if (!newMessage.value.trim()) return

  // Add user message
  messages.value.push({
    role: 'user',
    content: newMessage.value.trim()
  })

  // Clear input
  newMessage.value = ''

  // Scroll to bottom
  await scrollToBottom()

  // Simulate response (replace with actual API call)
  setTimeout(() => {
    messages.value.push({
      role: 'assistant',
      content: 'This is a simulated response. Replace this with actual API integration.'
    })
    scrollToBottom()
  }, 1000)
}

onMounted(() => {
  scrollToBottom()
})
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #ffffff;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}

.chat-content {
  display: flex;
  flex-direction: column;
  height: 100%;
  max-width: 800px;
  margin: 0 auto;
  width: 100%;
}

.messages {
  flex-grow: 1;
  overflow-y: auto;
  padding: 24px;
  scroll-behavior: smooth;
}

.message {
  margin-bottom: 24px;
}

.message-content {
  display: flex;
  gap: 16px;
  padding: 16px;
  max-width: 100%;
}

.message.assistant {
  background-color: rgba(247, 247, 248);
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 4px;
}

.text {
  font-size: 16px;
  line-height: 1.5;
  white-space: pre-wrap;
  padding-right: 16px;
}

.input-area {
  border-top: 1px solid rgba(0, 0, 0, 0.1);
  padding: 24px;
  background-color: #ffffff;
}

.input-container {
  position: relative;
  max-width: 800px;
  margin: 0 auto;
}

:deep(.t-textarea) {
  background-color: #ffffff;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  padding: 8px 64px 8px 16px;
  font-size: 16px;
  line-height: 1.5;
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.1);
}

:deep(.t-textarea:focus) {
  box-shadow: 0 0 0 1px #000000;
  border-color: #000000;
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
  cursor: not-allowed;
}

.input-footer {
  text-align: center;
  color: rgba(0, 0, 0, 0.5);
  font-size: 12px;
  margin-top: 12px;
}

/* Scrollbar styling */
.messages::-webkit-scrollbar {
  width: 8px;
}

.messages::-webkit-scrollbar-track {
  background: transparent;
}

.messages::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

.messages::-webkit-scrollbar-thumb:hover {
  background-color: rgba(0, 0, 0, 0.3);
}
</style> 
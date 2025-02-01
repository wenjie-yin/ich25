<template>
  <div class="chat-wrapper">
    <!-- Header -->
    <v-app-bar color="white" elevation="1">
      <v-container class="px-4">
        <div class="d-flex align-center justify-space-between">
          <div class="d-flex align-center">
            <v-icon icon="mdi-chat" color="primary" class="mr-2" size="large"></v-icon>
            <span class="text-h6">Chat</span>
          </div>
          <v-btn
            color="primary"
            @click="handleLogout"
            prepend-icon="mdi-logout"
          >
            Logout
          </v-btn>
        </div>
      </v-container>
    </v-app-bar>

    <!-- Chat Content -->
    <v-main>
      <v-container fluid class="pa-0 fill-height chat-content">
        <v-row no-gutters class="fill-height">
          <v-col cols="12" class="d-flex flex-column">
            <!-- Messages Area -->
            <div class="messages-container" ref="messagesContainer">
              <v-container class="px-4">
                <v-row justify="center" v-for="(message, index) in messages" :key="index">
                  <v-col cols="12" sm="10" md="8" lg="6">
                    <v-card
                      :color="message.role === 'user' ? 'grey-lighten-4' : 'white'"
                      :elevation="0"
                      class="mb-4"
                    >
                      <v-card-text class="text-body-1">
                        {{ message.content }}
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>
              </v-container>
            </div>

            <!-- Input Area -->
            <div class="input-section">
              <v-container>
                <v-row justify="center">
                  <v-col cols="12" sm="10" md="8" lg="6">
                    <v-form @submit.prevent="sendMessage">
                      <v-card variant="outlined" class="pa-2">
                        <v-textarea
                          v-model="newMessage"
                          rows="1"
                          auto-grow
                          hide-details
                          density="comfortable"
                          variant="plain"
                          placeholder="Message..."
                          @keydown.enter.prevent="sendMessage"
                          ref="messageInput"
                          class="message-input"
                        ></v-textarea>
                        
                        <v-card-actions class="pa-0 justify-end">
                          <v-btn
                            :disabled="!newMessage.trim()"
                            color="primary"
                            icon
                            @click="sendMessage"
                          >
                            <v-icon>mdi-send</v-icon>
                          </v-btn>
                        </v-card-actions>
                      </v-card>
                      
                      <div class="text-center text-caption text-grey mt-2">
                        Free Research Preview. ChatGPT may produce inaccurate information.
                      </div>
                    </v-form>
                  </v-col>
                </v-row>
              </v-container>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

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
const messageInput = ref<HTMLTextAreaElement | null>(null)
const messagesContainer = ref<HTMLElement | null>(null)

const handleLogout = () => {
  localStorage.removeItem('user')
  router.push('/login')
}

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
    content: newMessage.value
  })

  // Clear input
  newMessage.value = ''

  // Scroll to bottom
  await scrollToBottom()

  // Simulate response (replace with actual API call)
  setTimeout(() => {
    messages.value.push({
      role: 'assistant',
      content: 'This is a simulated response. Replace with actual API integration.'
    })
    scrollToBottom()
  }, 1000)
}

onMounted(() => {
  if (messageInput.value) {
    messageInput.value.focus()
  }
})
</script>

<style scoped>
.chat-wrapper {
  height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
}

.chat-content {
  flex: 1;
  overflow: hidden;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  width: 100%;
  background-color: white;
  height: calc(100vh - 180px); /* Adjust for header and input area */
}

.input-section {
  width: 100%;
  background-color: white;
  border-top: 1px solid rgba(0, 0, 0, 0.12);
  padding: 16px 0;
}

:deep(.message-input) {
  width: 100%;
}

:deep(.v-textarea textarea) {
  min-height: 24px !important;
}

:deep(.v-container) {
  width: 100%;
  max-width: 100%;
}

:deep(.v-app-bar) {
  position: sticky;
  top: 0;
  z-index: 1000;
}
</style> 
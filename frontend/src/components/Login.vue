<template>
  <div class="login-wrapper">
    <v-container fluid class="fill-height bg-grey-lighten-4">
      <v-row align="center" justify="center" class="mx-0">
        <v-col cols="12" sm="8" md="6" lg="4" class="pa-4">
          <v-card class="pa-8" elevation="2" width="100%">
            <v-card-title class="text-h4 text-center mb-6">
              Welcome Back
            </v-card-title>
            
            <v-form @submit.prevent="handleLogin" class="login-form">
              <v-text-field
                v-model="email"
                label="Email address"
                type="email"
                required
                variant="outlined"
                prepend-inner-icon="mdi-email"
                class="mb-4"
              ></v-text-field>

              <v-text-field
                v-model="password"
                label="Password"
                :type="showPassword ? 'text' : 'password'"
                required
                variant="outlined"
                prepend-inner-icon="mdi-lock"
                :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                @click:append-inner="showPassword = !showPassword"
              ></v-text-field>

              <v-btn
                color="primary"
                size="large"
                block
                type="submit"
                class="mt-6"
              >
                Continue
              </v-btn>

              <div class="text-center mt-6">
                <span class="text-grey">Don't have an account?</span>
                <v-btn
                  variant="text"
                  color="primary"
                  class="ml-2"
                  @click="toggleSignup"
                >
                  Sign up
                </v-btn>
              </div>
            </v-form>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const email = ref('')
const password = ref('')
const showPassword = ref(false)

const handleLogin = async () => {
  try {
    // TODO: Replace with actual API call
    // Simulating an API call
    const user = {
      email: email.value,
      token: 'dummy-token-' + Math.random()
    }
    
    // Store user info in localStorage
    localStorage.setItem('user', JSON.stringify(user))
    
    // Navigate to chat
    router.push('/chat')
  } catch (error) {
    console.error('Login failed:', error)
    // TODO: Handle login error
  }
}

const toggleSignup = () => {
  // TODO: Implement signup navigation
  console.log('Toggle signup')
}
</script>

<style scoped>
.login-wrapper {
  width: 100%;
  min-height: 100vh;
}

.login-form {
  width: 100%;
}

:deep(.v-field) {
  width: 100%;
}

:deep(.v-container) {
  max-width: 100%;
}
</style> 
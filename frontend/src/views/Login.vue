<template>
  <div class="container">
    <div class="login-container">
      <div class="login">
        <t-space direction="vertical" size="large">
          <h1 class="title">Welcome back</h1>
          <p class="subtitle">Log in to your account</p>
          <t-form ref="form" :data="formData" :rules="rules" @submit="onSubmit" :require-mark="false">
            <t-form-item name="username">
              <label class="input-label">Email address</label>
              <t-input
                v-model="formData.username"
                size="large"
                placeholder="example@email.com"
                :disabled="loading"
              />
            </t-form-item>
            <t-form-item name="password">
              <label class="input-label">Password</label>
              <t-input
                v-model="formData.password"
                type="password"
                size="large"
                placeholder="Enter your password"
                :disabled="loading"
              />
            </t-form-item>
            <t-form-item>
              <t-button block size="large" type="submit" theme="primary" class="submit-btn" :loading="loading">
                {{ loading ? 'Logging in...' : 'Continue' }}
              </t-button>
            </t-form-item>
          </t-form>
          <p class="footer-text">
            Don't have an account?
            <t-link theme="primary" hover="color" class="signup-link">Sign up</t-link>
          </p>
        </t-space>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { MessagePlugin } from 'tdesign-vue-next'
import axios from 'axios'
import { useRouter } from 'vue-router'

interface FormData {
  username: string;
  password: string;
}

const router = useRouter()
const formData = ref<FormData>({
  username: '',
  password: '',
})

const rules = {
  username: [{ required: true, message: 'Please enter your username or email', type: 'error' }],
  password: [{ required: true, message: 'Please enter your password', type: 'error' }],
}

const form = ref()
const loading = ref(false)

const onSubmit = async ({ validateResult, firstError }: { validateResult: boolean; firstError: string }) => {
  if (!validateResult) {
    MessagePlugin.error(firstError)
    return
  }

  loading.value = true
  try {
    const response = await axios.post('http://0.0.0.0:8000/token', {
      username: formData.value.username,
      password: formData.value.password,
    }, {
      timeout: 5000,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      withCredentials: true
    })

    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token)
      
      MessagePlugin.success('Login successful!')
      
      router.push('/chat')
    } else {
      MessagePlugin.error('Invalid response from server')
    }
  } catch (error: any) {
    console.error('Full error object:', error)
    console.error('Login error:', error)
    
    if (error.code === 'ECONNABORTED') {
      MessagePlugin.error('Request timed out. Please try again.')
    } else if (error.response) {
      const message = error.response.data?.detail || 'Invalid credentials'
      MessagePlugin.error(message)
    } else if (error.request) {
      MessagePlugin.error(error.message)
    } else {
      MessagePlugin.error('An error occurred. Please try again.')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  width: 100%;
  overflow: hidden;
  background: linear-gradient(to bottom right, #ffffff, #f5f5f5);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}

.login-container {
  width: 100%;
  max-width: 400px;
  margin: 0 20px;
}

.login {
  background-color: white;
  border: 1px solid #e5e5e5;
  border-radius: 16px;
  padding: 48px 32px;
}

.title {
  text-align: center;
  color: rgba(0, 0, 0, 0.9);
  margin: 0;
  font-size: 32px;
  font-weight: 600;
  letter-spacing: -0.5px;
}

.subtitle {
  text-align: center;
  color: rgba(0, 0, 0, 0.6);
  margin: -8px 0 0 0;
  font-size: 16px;
  font-weight: 400;
}

.input-label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.8);
}

:deep(.t-input) {
  width: 100%;
}

:deep(.t-input__inner) {
  border-radius: 8px;
  border-color: #e5e5e5;
}

:deep(.t-input__inner:hover) {
  border-color: #000000;
}

:deep(.t-input__inner:focus) {
  border-color: #000000;
  box-shadow: none;
}

.submit-btn {
  margin-top: 8px;
  background-color: #000000;
  border: none;
  border-radius: 8px;
  height: 44px;
  font-weight: 500;
}

:deep(.submit-btn:hover) {
  background-color: #2d2d2d !important;
}

.footer-text {
  text-align: center;
  color: rgba(0, 0, 0, 0.6);
  font-size: 14px;
  margin: 0;
}

.signup-link {
  color: #000000;
  text-decoration: none;
  font-weight: 500;
}

:deep(.signup-link:hover) {
  color: #2d2d2d !important;
}

:deep(.t-form__item) {
  margin-bottom: 24px;
}

:deep(.t-form__label--required::before) {
  display: none !important;
}
</style>
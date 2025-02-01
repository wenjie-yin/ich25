import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/Login.vue'
import Chat from '../components/Chat.vue'

const routes = [
    {
        path: '/',
        redirect: '/chat'
    },
    {
        path: '/chat',
        name: 'Chat',
        component: Chat,
        meta: { requiresAuth: true }
    },
    {
        path: '/login',
        name: 'Login',
        component: Login,
        meta: { guest: true }
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

// Simple auth check - replace with your actual auth logic
const isAuthenticated = () => {
    // Replace this with your actual authentication check
    return localStorage.getItem('user') !== null
}

// Navigation guard for authentication
router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requiresAuth)) {
        if (!isAuthenticated()) {
            next('/login')
        } else {
            next()
        }
    } else if (to.matched.some(record => record.meta.guest)) {
        if (isAuthenticated()) {
            next('/chat')
        } else {
            next()
        }
    } else {
        next()
    }
})

export default router
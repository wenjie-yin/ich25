import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import About from '../views/About.vue'
import Chat from '../views/Chat.vue'
const routes = [
    { path: '/', component: Login },
    { path: '/chat', component: Chat },
    { path: '/about', component: About }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
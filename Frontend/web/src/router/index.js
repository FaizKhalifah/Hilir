import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import login from '@/views/auth/login.vue'
import register from '@/views/auth/register.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'login',
    component: login
  },
  {
    path:'/register',
    name:'register',
    component:register
  }
]

const router = createRouter({
  history: createWebHistory(), // Menggunakan Web History tanpa hash
  routes
})

export default router

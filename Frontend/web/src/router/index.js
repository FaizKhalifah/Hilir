import { createRouter, createWebHistory } from 'vue-router'
import login from '@/views/auth/login.vue'
import register from '@/views/auth/register.vue'
import overview from '@/views/dashboard/overview.vue'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: login
  },
  {
    path:'/register',
    name:'register',
    component:register
  },
  {
    path: '/',
    name: 'home',
    component: overview,
    meta: { requiresAuth: true}
  },
 
  {
    path:'/dashboard',
    name:'dashboard',
    component:overview,
    meta: { requiresAuth: true}
  }
]

const router = createRouter({
  history: createWebHistory(), // Menggunakan Web History tanpa hash
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  console.log('Navigating to:', to.name, 'Token:', token);


  // Memeriksa apakah rute memerlukan autentikasi
  if (to.meta.requiresAuth && !token) {
    next({ name: 'login' }); 
  } else {
    next(); 
  }
});


export default router

import { createRouter, createWebHistory } from 'vue-router'
import overview from '@/views/dashboard/overview.vue'
import authroutes from './authroutes.js'
import dashboardRoutes from './dashboardRoutes.js'
const routes = [
  {
    path: '/',
    name: 'home',
    component: overview,
    meta: { requiresAuth: true}
  },
  ...authroutes,
  ...dashboardRoutes,

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

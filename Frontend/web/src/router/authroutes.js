import login from "@/views/auth/login.vue";
import register from "@/views/auth/register.vue";

export default[
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
]
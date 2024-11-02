import overview from "@/views/dashboard/overview.vue";
import ruangHilir from "@/views/dashboard/ruangHilir.vue";
export default[
     
  {
    path:'/dashboard',
    name:'dashboard',
    component:overview,
    meta: { requiresAuth: true}
  },

  {
    path:'/ruanghilir',
    name:'ruanghilir',
    component:ruangHilir,
    meta: { requiresAuth: true}
  }
]
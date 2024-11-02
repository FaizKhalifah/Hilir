import overview from "@/views/dashboard/overview.vue";
import ruangHilir from "@/views/dashboard/ruangHilir.vue";
import assesment from "@/views/dashboard/assesment.vue";
import exercise from "@/views/dashboard/exercise.vue";
export default[
    {
        path:'/overview',
        name:'overview',
        component:overview,
        meta: { requiresAuth: true}
      },
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
  },
  {
    path: '/assessment/:child_id',
    name: 'Assessment',
    component: assesment,
    props: true
  },
  {
    path: '/exercise/:child_id',
    name: 'Exercise',
    component: exercise,
    props: true
  }
]
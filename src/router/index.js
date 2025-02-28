import { createRouter, createWebHistory } from 'vue-router';
import Register from '../components/register.vue';
import Login from '../components/login.vue';
import NotFound from "../components/NotFound.vue";

   const routes = [
     {
       path: '/',
       redirect: '/register'
     },
     {
       path: '/register',
       name: 'Register',
       component: Register
     },
     {
       path: '/login',
       name: 'Login',
       component: Login
     },
     {
       path: '/:pathMatch(.*)*',
       name: 'NotFound',
       component: NotFound
     }
   ];


const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
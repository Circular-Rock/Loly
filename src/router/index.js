import { createRouter, createWebHistory } from 'vue-router';
import Register from '../components/register.vue';
import Login from '../components/login.vue';
import NotFound from "../components/NotFound.vue";
import ImageDisplay from "../components/ImageDisplay.vue";

   const routes = [
     {
       path: '/',
       redirect: '/ImageDisplay'
     },
     {
       path: '/register',
       name: 'Register',
       component: Register
     },
     {
       path: '/ImageDisplay',
       name: 'ImageDisplay',
       component: ImageDisplay
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
import { createRouter, createWebHistory } from 'vue-router';
import UserRegister from '../components/UserRegister.vue';
import UserLogin from '../components/UserLogin.vue';
import NotFound from "../components/NotFound.vue";
import ImageDisplay from "../components/ImageDisplay.vue";
import UserConsole from "../components/UserConsole.vue";

   const routes = [
     {
       path: '/',
       redirect: '/UserConsole'
     },
     {
       path: '/register',
       name: 'UserRegister',
       component: UserRegister
     },
     {
       path: '/ImageDisplay',
       name: 'ImageDisplay',
       component: ImageDisplay
     },
     {
       path: '/login',
       name: 'UserRegister',
       component: UserLogin
     },
     {
       path: '/console',
       name: 'UserConsole',
       component: UserConsole
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
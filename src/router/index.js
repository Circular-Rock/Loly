import { createRouter, createWebHistory } from 'vue-router';
import UserLogin from '../components/UserLogin.vue';
import NotFound from "../components/NotFound.vue";
import ImageDisplay from "../components/ImageDisplay.vue";
import UserConsole from "../components/UserConsole.vue";
import UserConsole1 from "../components/UserConsole1.vue";

   const routes = [
     {
       path: '/',
       redirect: '/UserLogin'
     },
     {
       path: '/ImageDisplay',
       name: 'ImageDisplay',
       component: ImageDisplay
     },
     {
       path: '/Userlogin',
       name: 'UserLogin',
       component: UserLogin
     },
     {
       path: '/console',
       name: 'UserConsole',
       component: UserConsole
     },
     {
       path: '/console1',
       name: 'UserConsole1',
       component: UserConsole1
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
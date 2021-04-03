import { createRouter, createWebHashHistory } from 'vue-router';
import Home from '../views/Home.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/results/:rule',
    name: 'Results',
    component: () => import('@/views/Results.vue'),
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/views/Settings.vue'),
  },
  {
    path: '/settings/set-api',
    name: 'SetAPI',
    component: () => import('@/views/Settings/SetAPI.vue'),
  },
  {
    path: '/settings/set-rules',
    name: 'SetRules',
    component: () => import('@/views/Settings/SetRules.vue'),
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;

import { tooltipDirective } from '@/directives/_index';

import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';

// eslint-disable-next-line
window.eel._host = 'http://localhost:8123';

createApp(App)
  .use(store)
  .use(router)
  .directive('tooltip', tooltipDirective)
  .mount('#app');

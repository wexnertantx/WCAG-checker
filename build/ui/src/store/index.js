import { createStore } from 'vuex';

import processStore from './process';

export default createStore({
  state: {},
  getters: {},
  mutations: {},
  actions: {},
  modules: {
    process: processStore,
  },
});

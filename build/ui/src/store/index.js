import { createStore } from 'vuex';

import processStore from './process';
import configStore from './config.js';

export default createStore({
  state: {
    pendingPythonAction: false,
  },
  getters: {
    isPendingPythonAction: state => state.pendingPythonAction,
  },
  mutations: {
    /**
     * Event handler that runs when an UI action communicates with Python
     * Blocks every UI action until Python tasks finishes
     */
    OnPythonActionStart(state) {
      state.pendingPythonAction = false;
    },
    /**
     * Event handler that runs when an UI action finished communicating with Python
     * Unblocks every UI action, call from Python with eel.send_python_action_finish_event
     */
    OnPythonActionFinish(state) {
      state.pendingPythonAction = true;
    },
  },
  actions: {},
  modules: {
    process: processStore,
    config: configStore,
  },
});

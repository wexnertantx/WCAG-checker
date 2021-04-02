export default {
  namespaced: true,
  state: {
    website: null,
    status: 'STOPPED',
    rules: {},
    pendingAction: false,
  },
  getters: {
    getWebsite: state => state.website,
    getStatus: state => state.status,
    isActionPending: state => state.pendingAction,
    getRules: state => state.rules,
  },
  mutations: {
    resetResultOfRule(state, ruleId) {
      state.rules[ruleId].status = 'PENDING';
      state.rules[ruleId].result = {
        success: [],
        fail: [],
      };
    },
    addResultToRule(state, result) {
      state.rules[result.rule].result[result.status].push(result.message);
    },
    setWebsite(state, website) {
      state.website = website;
    },
    setStatus(state, status) {
      state.status = status;
    },
    startAction(state) {
      state.pendingAction = true;
    },
    finishAction(state) {
      state.pendingAction = false;
    },
    finishProcess(state) {
      state.status = 'STOPPED';
    },
    finishRule(state, ruleId) {
      state.rules[ruleId].status = 'FINISHED';
    },
  },
  actions: {
    addRule({ state, commit }, ruleData) {
      state.rules[ruleData.id] = ruleData;
      commit('resetResultOfRule', ruleData.id);
      console.log(`Rule ${ruleData.id} has been added!`);
    },
    resetResults({ state, commit }) {
      const keys = Object.keys(state.rules);
      for (let k = 0; k < keys.length; k++) {
        commit('resetResultOfRule', keys[k]);
      }
    },
    async startProcess({ commit, getters, dispatch }, website) {
      if (getters.isActionPending) return;

      commit('setStatus', 'RUNNING');
      commit('startAction');

      if (website !== getters.getWebsite) {
        dispatch('resetResults');
      }

      await window.eel.eel_start_process(website);
      commit('finishAction');
    },
    async pauseProcess({ commit, getters }) {
      if (getters.isActionPending) return;

      commit('setStatus', 'PAUSED');
      commit('startAction');

      console.log('pausing');

      await window.eel.eel_pause_process();
      commit('finishAction');
    },
    async stopProcess({ commit, getters }) {
      if (getters.isActionPending) return;

      commit('setStatus', 'STOPPED');
      commit('startAction');

      await window.eel.eel_stop_process();
    },
  },
};

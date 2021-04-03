export default {
  namespaced: true,
  state: {
    pending: false,
    config: {
      api: {
        detectlanguage: '12341234',
      },
      rules: {
        local: {
          disabled: [],
        },
        external: {
          disabled: [],
        },
      },
    },
  },
  getters: {
    getConfig: state => state.config,
    isConfigActionPending: state => state.pending,
  },
  mutations: {
    setConfig(state, config) {
      state.config = config;
    },
    setConfigByKey(state, { key, config }) {
      state.config[key] = config;
    },
    disableRule(state, { location, rule }) {
      state.config.rules[location].disabled.push(rule.id);
    },
    enableRule(state, { location, rule }) {
      const ruleIndex = state.config.rules[location].disabled.findIndex(r => r === rule.id);
      if (ruleIndex !== -1) {
        state.config.rules[location].disabled.splice(ruleIndex, 1);
      }
    },
    OnConfigActionStart(state) {
      state.pending = true;
    },
    OnConfigActionFinish(state) {
      state.pending = false;
    },
  },
  actions: {
    async saveConfig({ commit, getters }) {
      if (getters.isPending) return;

      // Block all the UI actions until config is saved
      commit('OnConfigActionStart');
      const config = JSON.stringify(getters.getConfig);
      await window.eel.eel_save_config(config)();
      // Config is saved, unblock the UI actions
      commit('OnConfigActionFinish');
    },
    async saveConfigByKey({ commit, getters }, key) {
      if (getters.isPending) return;

      // Block all the UI actions until config is saved
      commit('OnConfigActionStart');
      const config = JSON.stringify(getters.getConfig[key]);
      await window.eel.eel_save_config(config, key)();
      // Config is saved, unblock the UI actions
      commit('OnConfigActionFinish');
    },
    async loadConfig({ commit, getters }) {
      if (getters.isPending) return;

      // Block all the UI actions until config is loaded
      commit('OnConfigActionStart');
      const config = await window.eel.eel_load_config()();
      commit('setConfig', JSON.parse(config));
      // Config is loaded, unblock the UI actions
      commit('OnConfigActionFinish');
    },
    async loadConfigByKey({ commit, getters }, key) {
      if (getters.isPending) return;

      // Block all the UI actions until config is loaded
      commit('OnConfigActionStart');
      const config = await window.eel.eel_load_config(key)();
      commit('setConfigByKey', { key, config: JSON.parse(config) });
      // Config is loaded, unblock the UI actions
      commit('OnConfigActionFinish');
    },
  },
};

export default {
  namespaced: true,
  state: {
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
  },
  mutations: {
    setConfig(state, config) {
      state.config = config;
    },
    setConfigByKey(state, { key, config }) {
      state.config[key] = config;
    },
  },
  actions: {
    async saveConfig({ commit, getters }) {
      if (getters.isPending) return;

      // Block all the UI actions until config is saved
      commit('OnPythonActionStart', null, { root: true });
      const config = JSON.stringify(getters.getConfig);
      await window.eel.eel_save_config(config)();
      // Config is saved, unblock the UI actions
      commit('OnPythonActionFinish', null, { root: true });
    },
    async saveConfigByKey({ commit, getters }, key) {
      if (getters.isPending) return;

      // Block all the UI actions until config is saved
      commit('OnPythonActionStart', null, { root: true });
      const config = JSON.stringify(getters.getConfig[key]);
      await window.eel.eel_save_config(config, key)();
      // Config is saved, unblock the UI actions
      commit('OnPythonActionFinish', null, { root: true });
    },
    async loadConfig({ commit, getters }) {
      if (getters.isPending) return;

      // Block all the UI actions until config is loaded
      commit('OnPythonActionStart', null, { root: true });
      const config = await window.eel.eel_load_config()();
      commit('setConfig', JSON.parse(config));
      // Config is loaded, unblock the UI actions
      commit('OnPythonActionFinish', null, { root: true });
    },
    async loadConfigByKey({ commit, getters }, key) {
      if (getters.isPending) return;

      // Block all the UI actions until config is loaded
      commit('OnPythonActionStart', null, { root: true });
      const config = await window.eel.eel_load_config(key)();
      commit('setConfigByKey', { key, config: JSON.parse(config) });
      // Config is loaded, unblock the UI actions
      commit('OnPythonActionFinish', null, { root: true });
    },
  },
};

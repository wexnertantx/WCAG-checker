import { PROCESS_STATES, RULE_STATES } from '@/lib/enum.js';

export default {
  namespaced: true,
  state: {
    driver: 'chrome',
    website: null,
    status: PROCESS_STATES.STOPPED,
    rules: {},
  },
  getters: {
    /**
     * Returns the selected driver
     * @returns {String}  The name of the driver
     */
    getDriver: state => state.driver,
    /**
     * Returns the status of the process
     * @returns {Number}  The status of the process, see enum.js PROCESS_STATES
     */
    getProcessStatus: state => state.status,
    /**
     * Returns the rules list as an object
     * @returns {Object}  The list containing all the rules
     */
    getRules: state => state.rules,
    /**
     * Returns whether the process is running, paused or stopped
     * @returns {Boolean}  True if the process is running or paused, false otherwise
     */
    isProcessRunning: state => (state.status === PROCESS_STATES.RUNNING || state.status === PROCESS_STATES.PAUSED),
    isRuleDisabled: (state, getters, rootState, rootGetters) => (rule) => {
      const { rules } = rootGetters['config/getConfig'];
      if (rules?.local?.disabled?.includes(rule) || rules?.external?.disabled?.includes(rule)) {
        return true;
      }
      return false;
    },
  },
  mutations: {
    /**
     * Resets the result of a specific rule and set its status to PENDING
     * @param {String} ruleId     - The ID of the rule as loaded from Python
     */
    resetResultOfRule(state, ruleId) {
      state.rules[ruleId].status = RULE_STATES.PENDING;
      state.rules[ruleId].result = {
        success: [],
        fail: [],
      };
    },
    /**
     * Sets the target driver for the process
     * @param {String} website    - The driver to use with selenium
     */
    setDriver(state, driver) {
      state.driver = driver;
    },
    /**
     * Sets the target website for the process
     * @param {String} website    - The website to analyze
     */
    setWebsite(state, website) {
      state.website = website;
    },
    /**
     * Sets the status of the process
     * @param {Number} status      - The status of the process, see enum.js PROCESS_STATES
     */
    setStatus(state, status) {
      state.status = status;
    },
    /**
     * Event handler that runs when the process finishes analyzing
     */
    OnProcessFinish(state) {
      state.status = PROCESS_STATES.STOPPED;
    },
    /**
     * Event handler that runs when a rule result is pushed by Python
     * @param {String} ruleId   - The ID of the rule
     * @param {String} status   - Either 'success' or 'fail' depending if the element respects the WCAG requirements for that rule
     * @param {String} message  - The message of the result (e.g: 'video.vid without-controls' has autoplay enabled but no controls could be found)
     */
    OnRuleResult(state, { ruleId, status, message }) {
      state.rules[ruleId].result[status].push(message);
    },
    /**
     * Event handler that runs when a rule status is changed by Python
     * @param {String} ruleId   - The ID of the rule
     * @param {Number} status   - The status of the rule, see enum.js RULE_STATES
     */
    OnRuleStateChange(state, { ruleId, status }) {
      state.rules[ruleId].status = status;
    },
  },
  actions: {
    /**
     * Adds a rule to the list as retrieved from Python rule list
     * @param {Object} ruleData    - Object holding all the relevant information of a rule
     */
    addRule({ state, commit }, ruleData) {
      state.rules[ruleData.id] = ruleData;
      commit('resetResultOfRule', ruleData.id);
      console.log(`Rule ${ruleData.id} has been added!`);
    },
    /**
     * Resets all results of the rules
     */
    resetResults({ state, commit }) {
      const keys = Object.keys(state.rules);
      for (let k = 0; k < keys.length; k++) {
        commit('resetResultOfRule', keys[k]);
      }
    },
    /**
     * Starts the analyzing process on a website
     * @param {String} website   - The website that will get analyzed
     */
    async startProcess({ commit, getters, dispatch }, website) {
      if (getters.isActionPending) return;

      if (getters.getProcessStatus === PROCESS_STATES.STOPPED) {
        dispatch('resetResults');
      }

      commit('setStatus', PROCESS_STATES.RUNNING);
      commit('OnPythonActionStart', null, { root: true });

      commit('setWebsite', website);
      await window.eel.eel_start_process(getters.getDriver, website)();
    },
    /**
     * Pauses the analyzing process
     */
    async pauseProcess({ commit, getters }) {
      if (getters.isActionPending) return;

      commit('setStatus', PROCESS_STATES.PAUSED);
      commit('OnPythonActionStart', null, { root: true });

      await window.eel.eel_pause_process()();
    },
    /**
     * Stops the analyzing process
     */
    async stopProcess({ commit, getters }) {
      if (getters.isActionPending) return;

      commit('setStatus', PROCESS_STATES.STOPPED);
      commit('OnPythonActionStart', null, { root: true });

      await window.eel.eel_stop_process()();
    },
  },
};

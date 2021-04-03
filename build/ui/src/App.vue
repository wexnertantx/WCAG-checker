<template>
  <Header />
  <div class="body">
    <Sidebar />
    <router-view class="page" v-slot="{ Component }">
      <transition name="switch" mode="out-in">
        <component :key="$route.path" :is="Component" />
      </transition>
    </router-view>
  </div>
</template>

<script>
import Header from '@/components/Header.component.vue';
import Sidebar from '@/components/Sidebar.component.vue';
import { RULE_STATES } from '@/lib/enum.js';

export default {
  components: { Header, Sidebar },
  async created() {
    // Eel bridge functions binding
    window.eel.expose(this.eelOnPythonActionFinish, 'send_python_action_finish_event');
    window.eel.expose(this.eelOnProcessFinish, 'send_process_finish_event');
    window.eel.expose(this.eelOnRuleResult, 'send_rule_result_event');
    window.eel.expose(this.eelOnRuleStateChange, 'send_rule_state_change_event');

    // Load config
    const config = await window.eel.eel_load_config()();
    this.$store.commit('config/setConfig', JSON.parse(config));

    // Request loaded rules from Python
    const rules = await window.eel.eel_request_rules()();
    for (let i = 0; i < rules.length; i++) {
      this.$store.dispatch('process/addRule', rules[i]);
    }
  },
  methods: {
    // Eel bridge functions action
    eelOnPythonActionFinish() {
      try {
        this.$store.commit('OnPythonActionFinish');
      } catch (error) {
        console.error(error);
      }
    },
    eelOnProcessFinish() {
      try {
        this.$store.commit('process/OnProcessFinish');
      } catch (error) {
        console.error(error);
      }
    },
    eelOnRuleResult(ruleId, status, message) {
      try {
        this.$store.commit('process/OnRuleResult', { ruleId, status, message });
      } catch (error) {
        console.error(error);
      }
    },
    eelOnRuleStateChange(ruleId, status) {
      try {
        const disabled = this.$store.getters['process/isRuleDisabled'](ruleId);
        if (status === RULE_STATES.RUNNING && !disabled) {
          this.$router.push({ name: 'Results', params: { rule: ruleId } });
        }
        this.$store.commit('process/OnRuleStateChange', { ruleId, status });
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>

<style lang="scss">
@import '@/scss/_reset';
@import '@/scss/_normalize';
@import '@/scss/_fonts';
@import '@/scss/_animations';

html, body, #app {
  display: flex;
  flex: 1;
  min-height: 100vh;
  font-size: 16px;
  position: relative;
}

#background {
  position: fixed;
  height: 100%;
  width: 100%;
  background: url('./assets/images/dashboard-bg.jpg') no-repeat center center / cover;
  &:after {
    content: '';
    position: fixed;
    width: inherit;
    height: inherit;
    background: url('./assets/images/gradient-bg.jpg') no-repeat center center / cover;
    opacity: .9;
  }
}

#app {
  flex-direction: column;
  font-family: Open-Sans, Helvetica, Arial, sans-serif;
  font-weight: 300;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: $col-text-def;

  .body {
    flex: 1;
    display: flex;
    margin-top: 25px;
    .page {
      flex: 1;
      display: flex;
      flex-direction: column;
      margin: 15px;

      &.settings .settings-section {
        margin-bottom: 40px;
        font-size: 2rem;
        text-align: center;
      }
    }
  }
}

a {
  color: inherit;
  outline: none;
  text-decoration: inherit;
}

input, textarea {
  border: none;
  background: none;
  outline: none;
  overflow: hidden;
  line-height: 0;
  color: rgba($col-text, .6);
}

.switch-enter-active, .switch-leave-active {
  transition: transform .4s ease, opacity .2s ease;
}

.switch-enter-from, .switch-leave-to {
  transform: scale(0.9);
  opacity: 0;
}
</style>

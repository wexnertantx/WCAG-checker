<template>
  <header class="main-header">
    <div class="logo-wrapper">
      <div class="logo"></div>
      <div class="name">CS27</div>
      <div class="dashboard">Dashboard</div>
    </div>
    <div class="process-wrapper">
      <Button v-bind="buttons.toggleDriver" :icon="$store.getters['process/getDriver']" />
      <div class="process">
        <Button v-bind="buttons.startProcess" :icon="getProcessStateIcon" :pending="$store.getters.isPendingPythonAction" />
        <Divider :vertical="true" />
        <input v-model="process.website" placeholder="http://www.amazon.com/" :disabled="$store.getters['process/isProcessRunning']" />
      </div>
      <Button v-if="$store.getters['process/isProcessRunning']" v-bind="buttons.stopProcess" icon="stop" />
    </div>
    <div class="navigation-wrapper">
      <!-- <Button v-bind="buttons.rules" /> -->
      <Button v-bind="buttons.settings" />
      <!-- <Button v-bind="buttons.quit" /> -->
    </div>
  </header>
</template>

<script>
import Divider from '@/components/Divider.component.vue';
import Button from '@/components/Button.component.vue';
import { PROCESS_STATES } from '@/lib/enum.js';

export default {
  components: { Button, Divider },
  data() {
    return {
      process: {
        website: null,
      },
      buttons: {
        toggleDriver: { name: 'toggle-driver', type: 'icon', click: this.toggleDriver },
        stopProcess: { name: 'stop-process', type: 'icon', click: this.stopProcess },
        startProcess: { name: 'start-process', type: 'icon', click: this.toggleProcessState },
        rules: { name: 'rules', type: 'icon', icon: 'calendar-check', click: this.rulesDebug },
        settings: { name: 'settings', type: 'icon', icon: 'settings', href: '/settings' },
        quit: { name: 'exit', type: 'icon', icon: 'power-off', click: this.quit },
      },
    };
  },
  computed: {
    getDriverIcon() {
      return this.$store.getters['process/getDriver'];
    },
    getProcessStateIcon() {
      switch (this.$store.getters['process/getProcessStatus']) {
        case PROCESS_STATES.RUNNING: return 'pause';
        case PROCESS_STATES.PAUSED:
        case PROCESS_STATES.STOPPED:
        default:
          return 'play';
      }
    },
  },
  methods: {
    quit() {
      window.open('', '_self').close();
    },
    rulesDebug() {
      console.log(this.$store);
      const rules = this.$store.getters['process/getRules'];
      const ruleKeys = Object.keys(rules);
      for (let k = 0; k < ruleKeys.length; k++) {
        console.log(rules[ruleKeys[k]]);
      }
    },
    stopProcess() {
      this.$store.dispatch('process/stopProcess');
    },
    toggleProcessState() {
      switch (this.$store.getters['process/getProcessStatus']) {
        case PROCESS_STATES.RUNNING: {
          this.$store.dispatch('process/pauseProcess');
          break;
        }
        case PROCESS_STATES.STOPPED: {
          if (!this.process.website?.length) {
            break;
          }
        }
        // eslint-disable-next-line no-fallthrough
        case PROCESS_STATES.PAUSED:
        default:
          this.$store.dispatch('process/startProcess', this.process.website);
          break;
      }
    },
    toggleDriver() {
      const driver = (this.$store.getters['process/getDriver'] === 'chrome') ? 'firefox' : 'chrome';
      this.$store.commit('process/setDriver', driver);
    },
  },
};
</script>

<style lang="scss">
@import '@/scss/_mixins';

.main-header {
  display: grid;
  grid-template-columns: 3fr 4fr 3fr;
  grid-template-areas: "left middle right";
  column-gap: 10px;
  min-height: 60px;
  padding: 4px 30px;
  border-top: 1px solid $col-bg;

  .logo-wrapper {
    grid-area: left;
    display: flex;
    flex-direction: row;
    align-items: center;
    font-size: 1.2rem;
    .logo {
      width: 40px;
      height: 40px;
      background-color: $col-blue;
      margin-right: 10px;
    }
    .name { margin: 0 4px; }
    .dashboard { font-weight: 600; }
  }

  .process-wrapper {
    grid-area: middle;
    align-self: center;
    display: flex;
    align-items: center;
    justify-content: center;
    column-gap: 10px;
    .btn-toggle-driver {
      width: 24px;
    }
    .process {
      flex: 1;
      display: flex;
      background-color: rgba(black, 0.25);
      border-radius: 4px;
      padding: 10px 20px;
      input {
        flex: 1;
        text-align: center;
        @include set-placeholder(rgba($col-text, .6));
      }
    }
    .button { font-size: 1.4em; }
  }

  .navigation-wrapper {
    grid-area: right;
    align-self: center;
    display: flex;
    flex-direction: row;
    justify-content: flex-end;
    .button {
      margin: 0 15px;
    }
  }
}
</style>

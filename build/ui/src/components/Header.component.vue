<template>
  <header class="main-header">
    <div class="logo-wrapper">
      <div class="logo"></div>
      <div class="name">CS27</div>
      <div class="dashboard">Dashboard</div>
    </div>
    <div class="process-wrapper">
      <div class="process">
        <Button v-bind="buttons.startProcess" :icon="getProcessStateIcon" :pending="isProcessPending" />
        <Divider :vertical="true" />
        <input v-model="process.website" placeholder="http://www.amazon.com/" :disabled="isProcessRunning" />
      </div>
      <Button v-if="isProcessRunning" v-bind="buttons.stopProcess" icon="stop" />
    </div>
    <div class="navigation-wrapper">
      <Button v-bind="buttons.rules" />
      <Button v-bind="buttons.settings" />
      <Button v-bind="buttons.quit" />
    </div>
  </header>
</template>

<script>
import Divider from '@/components/Divider.component.vue';
import Button from '@/components/Button.component.vue';

export default {
  components: { Button, Divider },
  data() {
    return {
      process: {
        website: null,
      },
      buttons: {
        stopProcess: { name: 'stop-process', type: 'icon', click: this.stopProcess },
        startProcess: { name: 'start-process', type: 'icon', click: this.toggleProcessState },
        rules: { name: 'rules', type: 'icon', icon: 'calendar-check', click: this.rulesDebug },
        settings: { name: 'settings', type: 'icon', icon: 'settings', click: () => { } },
        quit: { name: 'exit', type: 'icon', icon: 'power-off', click: this.quit },
      },
    };
  },
  computed: {
    isProcessRunning() {
      const processStatus = this.$store.getters['process/getStatus'];
      if (processStatus === 'RUNNING' || processStatus === 'PAUSED') {
        return true;
      }
      return false;
    },
    isProcessPending() {
      return this.$store.getters['process/isActionPending'];
    },
    getProcessStateIcon() {
      switch (this.$store.getters['process/getStatus']) {
        case 'RUNNING': return 'pause';
        case 'PAUSED':
        case 'STOPPED':
        default:
          return 'play';
      }
    },
  },
  methods: {
    quit() {
      window.close();
    },
    rulesDebug() {
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
      switch (this.$store.getters['process/getStatus']) {
        case 'RUNNING': return this.$store.dispatch('process/pauseProcess');
        case 'PAUSED':
        case 'STOPPED':
        default:
          return this.$store.dispatch('process/startProcess', this.process.website);
      }
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
  min-height: 60px;
  padding: 4px 30px;
  border-top: 1px solid $col-bg;
  // background-color: rgba(white, .2);

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
    .btn-stop-process { margin-left: 10px; }
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

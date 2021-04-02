<template>
  <Header />
  <div class="body">
    <section class="sidebar">
      <Button v-bind="buttons.home">Home</Button>
      <template v-if="getRulesButtons.length">
        <Divider />
        <span class="category">ACCESSIBILITY RULES</span>
        <Button v-for="rule in getRulesButtons" :key="rule.name" v-bind="rule" />
      </template>
    </section>
    <router-view class="page" />
  </div>
</template>

<script>
import Header from '@/components/Header.component.vue';
import Button from '@/components/Button.component.vue';
import Divider from '@/components/Divider.component.vue';

export default {
  components: { Header, Button, Divider },
  data() {
    return {
      buttons: {
        home: { name: 'home', type: 'menu', icon: 'home', href: '/' },
      },
    };
  },
  async created() {
    window.eel.expose(this.eelAddResultToRule, 'add_result_to_rule_js');
    window.eel.expose(this.eelFinishAction, 'finish_action_js');
    window.eel.expose(this.eelFinishProcess, 'finish_process_js');
    window.eel.expose(this.eelFinishRule, 'finish_rule_js');

    const rules = await window.eel.eel_request_rules()();
    for (let i = 0; i < rules.length; i++) {
      this.$store.dispatch('process/addRule', rules[i]);
    }
  },
  computed: {
    isProcessRunning() {
      const processStatus = this.$store.getters['process/getStatus'];
      if (processStatus === 'RUNNING' || processStatus === 'PAUSED') {
        return true;
      }
      return false;
    },
    getRulesButtons() {
      const rules = this.$store.getters['process/getRules'];
      const keys = Object.keys(rules);
      const items = keys.map((key) => {
        if (!this.isProcessRunning && rules[key].status !== 'FINISHED') {
          return false;
        }
        return {
          name: key,
          text: rules[key].name,
          type: (rules[key].status === 'FINISHED') ? 'green menu-sub' : 'menu-sub',
          href: `/rules/${rules[key].id}`,
          icon: (rules[key].status === 'FINISHED') ? 'check-circle' : 'spinner',
        };
      }).filter(item => item !== false);
      return items;
    },
  },
  methods: {
    eelAddResultToRule(rule, status, message) {
      this.$store.commit('process/addResultToRule', { rule, status, message });
    },
    eelFinishProcess() { this.$store.commit('process/finishProcess'); },
    eelFinishAction() { this.$store.commit('process/finishAction'); },
    eelFinishRule(rule) { this.$store.commit('process/finishRule', rule); },
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
  text-align: center;
  color: $col-text-def;

  .body {
    flex: 1;
    display: flex;
    margin-top: 25px;
    .sidebar {
      flex: 0 0 250px;
      display: flex;
      flex-direction: column;
      padding: 0 16px;
      .category {
        font-weight: 600;
        font-size: 12px;
        margin-bottom: 15px;
      }
    }
    .page {
      flex: 1;
      display: flex;
      flex-direction: column;
      // background-color: rgba(pink, .2);
    }
  }
}

a {
  color: inherit;
  outline: none;
  text-decoration: inherit;
  // transition: color .2s ease;
  // &:not(.router-link-active):hover {
  //   color: lighten($col-text-def, 20%);
  //   text-shadow: 0 0 1px $col-text-def;
  // }
}

input, textarea {
  border: none;
  background: none;
  outline: none;
  overflow: hidden;
  line-height: 0;
  color: rgba($col-text, .6);
}
</style>

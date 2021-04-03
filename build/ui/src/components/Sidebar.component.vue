<template>
  <section class="sidebar">
    <Button v-bind="buttons.home">Home</Button>
    <template v-if="isSettingsView">
      <Divider />
      <span class="category">SETTINGS</span>
      <Button v-for="button in buttons.settings" :key="button.name" v-bind="button" />
    </template>
    <template v-else>
      <template v-if="getRulesButtons.length">
        <Divider />
        <span class="category">RESULTS</span>
        <Button v-for="rule in getRulesButtons" :key="rule.name" v-bind="rule" />
      </template>
    </template>
  </section>
</template>

<script>
import Button from '@/components/Button.component.vue';
import Divider from '@/components/Divider.component.vue';
import { RULE_STATES } from '@/lib/enum.js';

export default {
  components: { Button, Divider },
  data() {
    return {
      buttons: {
        home: { name: 'home', type: 'menu', icon: 'home', href: '/' },
        settings: {
          api: { name: 'set-api', type: 'menu', icon: 'settings', href: '/settings/set-api', text: 'Set API Keys' },
          rules: { name: 'set-rules', type: 'menu', icon: 'calendar-check', href: '/settings/set-rules', text: 'Configure Rules' },
        },
      },
    };
  },
  computed: {
    isSettingsView() {
      return this.$route.path.startsWith('/settings');
    },
    /**
     * Returns the success ratio of a specific rule
     * @param {String} ruleId   - The id of the rule
     */
    getRuleSuccessRatio() {
      return (ruleId) => {
        const rules = this.$store.getters['process/getRules'];
        const success = rules?.[ruleId]?.result?.success.length || 0;
        const fail = rules?.[ruleId]?.result?.fail.length || 0;
        if (success) {
          return success / (success + fail);
        }
        return 0;
      };
    },
    /**
     * Gets a list with all the rules and create interface buttons
     */
    getRulesButtons() {
      const rules = this.$store.getters['process/getRules'];
      const keys = Object.keys(rules);
      const items = keys.map((key) => {
        if (!this.$store.getters['process/isProcessRunning'] && rules[key].status === RULE_STATES.PENDING) {
          return false;
        }
        let icon = 'minus-circle';
        let type = 'menu-sub';
        const disabled = this.$store.getters['process/isRuleDisabled'](key);
        if (!disabled) {
          switch (rules[key].status) {
            case RULE_STATES.RUNNING:
              icon = 'spinner2';
              break;
            case RULE_STATES.DISABLED:
              icon = 'minus-circle';
              break;
            case RULE_STATES.FINISHED:
              if (this.getRuleSuccessRatio(key) > 0.6) {
                icon = 'check-circle';
                type = `success ${type}`;
              } else {
                icon = 'x-circle';
                type = `fail ${type}`;
              }
              break;
            case RULE_STATES.FAILED:
              icon = 'alert-circle';
              type = `alert ${type}`;
              break;
            // RULE_STATES.PENDING
            default:
              icon = 'circle';
          }
        }
        return {
          name: key,
          text: rules[key].name,
          type,
          href: `/results/${rules[key].id}`,
          icon,
          disabled,
        };
      }).filter(item => item !== false);
      return items;
    },
  },
};
</script>

<style lang="scss">
.sidebar {
  flex: 0 0 250px;
  display: flex;
  flex-direction: column;
  padding: 0 16px;
  .category {
    font-weight: 600;
    font-size: 12px;
    margin-bottom: 15px;
    text-align: center;
  }
}
</style>

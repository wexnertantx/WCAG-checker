<template>
  <div class="settings set-api">
    <div class="settings-section">Configure Rules</div>
    <div class="settings-wrapper">
      <div class="section local-rules">
        <div class="section-title">LOCAL RULES</div>
        <div class="section-content">
          <div v-if="!getLocalRules.length" class="not-found">
            No local rules found
          </div>
          <div v-else v-for="rule in getLocalRules" :key="rule.id" class="rule-line" :class="{ 'selected': rule.checkbox.selected }">
            <Checkbox v-bind="rule.checkbox" @update:selected="(event) => onCheckboxSelect(event, rule)" />
            <span class="rule-name">{{ rule.name }}</span>
            <span class="rule-id">({{ rule.id }})</span>
          </div>
        </div>
      </div>
      <div class="section external-rules">
        <div class="section-title">EXTERNAL RULES</div>
        <div class="section-content">
          <div v-if="!getExternalRules.length" class="not-found">
            No external rules found
          </div>
          <div v-else v-for="rule in getExternalRules" :key="rule.id" class="rule-line" :class="{ 'selected': rule.checkbox.selected }">
            <Checkbox v-bind="rule.checkbox" @update:selected="(event) => onCheckboxSelect(event, rule.checkbox)" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Checkbox from '@/components/Checkbox.component.vue';

export default {
  components: { Checkbox },
  data() {
    return {
      isChanged: false,
    };
  },
  computed: {
    getAPIConfig() {
      return this.$store.getters['config/getConfig'].api;
    },
    getRulesMapping() {
      const rules = this.$store.getters['process/getRules'];
      const ruleKeys = Object.keys(rules);
      return ruleKeys.map((rule) => {
        const isDisabled = this.$store.getters['process/isRuleDisabled'](rule);
        return {
          ...rules[rule],
          checkbox: {
            id: rule,
            selected: !isDisabled,
            pending: this.$store.getters['config/isConfigActionPending'],
          },
        };
      });
    },
    getLocalRules() {
      return this.getRulesMapping.filter(rule => rule.local);
    },
    getExternalRules() {
      return this.getRulesMapping.filter(rule => !rule.local);
    },
  },
  methods: {
    async onCheckboxSelect(ev, rule) {
      const location = (rule.local) ? 'local' : 'external';
      if (ev) {
        this.$store.commit('config/enableRule', { location, rule });
      } else {
        this.$store.commit('config/disableRule', { location, rule });
      }
      this.$store.dispatch('config/saveConfigByKey', 'rules');
    },
  },
};
</script>

<style lang="scss" scoped>
.settings-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;

  .section {
    margin: 20px 0;
    .section-title {
      font-weight: 600;
      font-size: 12px;
      margin-left: 5px;
      margin-bottom: 5px;
    }
    .section-content {
      display: flex;
      flex-direction: column;
      background-color: rgba(black, .25);
      padding: 8px;
      row-gap: 8px;
      .not-found {
        font-weight: 500;
        font-size: 14px;
      }
      .rule-line {
        display: flex;
        column-gap: 4px;
        align-items: center;
        color: rgba($col-text, .6);
        &.selected {
          color: $col-text-def;
          font-weight: 500;
        }
      }
    }
  }
}
</style>

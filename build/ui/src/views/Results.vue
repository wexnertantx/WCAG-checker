<template>
  <div class="results">
    <div v-if="!isRuleValid" class="not-found">The rule "{{ $route.params.rule }}" is invalid</div>
    <template v-else>
      <header class="rule-header">
        <div class="rule-name">
          <Icon :name="getStatusIcon.icon" class="status" :class="[ getStatusIcon.style ]" />
          <span class="name">{{ getRuleData.name }}</span>
          <span class="id">({{ getRuleData.id }})</span>
          <div class="rule-link">
            <input ref="linkInput" :value="getRuleData.link" class="link-input" />
            <Button v-bind="buttons.link" />
          </div>
        </div>
        <div class="rule-version">
          <span class="version">V.</span>
          <span class="number">{{ getRuleData.version }}</span>
        </div>
      </header>
      <div class="section rule-description">
        <div class="section-title">DESCRIPTION</div>
        <div class="description">{{ getRuleData.description }}</div>
      </div>
      <div v-if="$store.getters['process/isRuleDisabled'](this.getRuleData.id)" class="not-found">This rule is currently disabled</div>
      <template v-else>
        <div class="section rule-results-graph">
          <Widget class="success-widget" v-bind="getSuccessWidgetData" />
          <Widget class="fail-widget" v-bind="getFailWidgetData" />
        </div>
        <div class="section rule-results">
          <div class="section-title">RESULTS</div>
          <div class="results-wrapper">
            <div class="success-results-wrapper">
              <Icon id="success-bg-icon" name="check-circle" />
              <div class="success-results">
                <div v-for="(result, i) in getRuleData.result.success" :key="i" class="result-line">
                  {{ result }}
                </div>
              </div>
            </div>
            <Divider :vertical="true" />
            <div class="fail-results-wrapper">
              <Icon id="fail-bg-icon" name="x-circle" />
              <div class="fail-results">
                <div v-for="(result, i) in getRuleData.result.fail" :key="i" class="result-line">
                  {{ result }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>
    </template>
  </div>
</template>

<script>
import Icon from '@/components/Icon.component.vue';
import Button from '@/components/Button.component.vue';
import Divider from '@/components/Divider.component.vue';
import Widget from '@/components/Widget.component.vue';
import { RULE_STATES } from '@/lib/enum.js';

export default {
  components: { Icon, Button, Divider, Widget },
  data() {
    return {
      buttons: {
        link: { name: 'link', type: 'icon', icon: 'external-link', click: this.copyLink },
      },
    };
  },
  computed: {
    getSuccessWidgetData() {
      return {
        title: 'SUCCESS RATE',
        panels: [
          { header: '# components', data: this.totalResults },
          { header: '# succeeded', data: this.getRuleData.result.success.length },
        ],
        bar: {
          color: '#C8F902',
          ratio: (this.totalResults) ? this.getSuccessRatio : 0,
          info: 'of components have succeeded',
        },
      };
    },
    getFailWidgetData() {
      return {
        title: 'FAILURE RATE',
        panels: [
          { header: '# components', data: this.totalResults },
          { header: '# failed', data: this.getRuleData.result.fail.length },
        ],
        bar: {
          color: '#FF6347',
          ratio: (this.totalResults) ? (1.0 - this.getSuccessRatio) : 0,
          info: 'of components have failed',
        },
      };
    },
    isRuleValid() {
      const rules = this.$store.getters['process/getRules'];
      const keys = Object.keys(rules);
      if (keys.includes(this.$route.params.rule)) {
        return true;
      }
      return false;
    },
    getRuleData() {
      const rules = this.$store.getters['process/getRules'];
      return rules[this.$route.params.rule];
    },
    totalResults() {
      const success = this.getRuleData?.result?.success.length || 0;
      const fail = this.getRuleData?.result?.fail.length || 0;
      return success + fail;
    },
    getSuccessRatio() {
      const success = this.getRuleData?.result?.success.length || 0;
      const fail = this.getRuleData?.result?.fail.length || 0;
      if (success) {
        return success / (success + fail);
      }
      return 0;
    },
    getStatusIcon() {
      const status = this.getRuleData?.status;

      let icon = 'minus-circle';
      let style;
      const disabled = this.$store.getters['process/isRuleDisabled'](this.getRuleData.id);
      if (!disabled) {
        switch (status) {
          case RULE_STATES.RUNNING:
            icon = 'spinner2';
            break;
          case RULE_STATES.DISABLED:
            icon = 'minus-circle';
            break;
          case RULE_STATES.FINISHED:
            if (this.getSuccessRatio > 0.6) {
              icon = 'check-circle';
              style = 'success';
            } else {
              icon = 'x-circle';
              style = 'fail';
            }
            break;
          case RULE_STATES.FAILED:
            icon = 'alert-circle';
            style = 'alert';
            break;
          // RULE_STATES.PENDING
          default:
            icon = 'circle';
        }
      }

      return {
        icon,
        style,
      };
    },
  },
  methods: {
    copyLink() {
      const input = this.$refs.linkInput;
      input.select();
      input.setSelectionRange(0, 99999);
      document.execCommand('copy');
    },
  },
};
</script>

<style lang="scss">
@import '@/scss/_mixins';

.results {
  .not-found {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    text-align: center;
  }
  .rule-header {
    display: flex;
    align-items: center;
    margin-bottom: 40px;
    .rule-name {
      flex: 1;
      display: flex;
      align-items: center;
      font-weight: 300;
      column-gap: 15px;
      .status {
        font-size: 1.25em;
        color: $col-text;
        &.alert { color: $col-alert; }
        &.fail { color: $col-fail; }
        &.success { color: $col-success; }
      }
      .name { font-size: 2.5em; }
      .id {
        color: rgba($col-text, .6);
        font-size: 1.5em;
      }
      .rule-link {
        .button-vue { top: 2px; }
        .link-input {
          position: absolute;
          width: 1px;
          height: 1px;
          left: -9999px;
        }
      }
    }
    .rule-version {
      font-size: 1.5em;
      .version {
        color: rgba($col-text, .6);
        font-weight: 700;
      }
    }
  }
  .section-title {
    font-weight: 600;
    font-size: 12px;
    margin-left: 5px;
    margin-bottom: 5px;
  }
  .section { margin: 20px 0; }
  .rule-description .description {
    padding: 10px;
    border-radius: 8px;
    background-color: rgba(black, .25);
  }
  .rule-results-graph {
    display: flex;
    justify-content: space-evenly;
    column-gap: 10px;
  }
  .rule-results {
    display: flex;
    flex-direction: column;
    .results-wrapper {
      display: flex;
      column-gap: 10px;
      height: 384px;
      .success-results-wrapper, .fail-results-wrapper {
        flex: 1;
        position: relative;
        display: flex;
        flex-direction: column;
        background-color: rgba(black, .25);
        border-radius: 8px;
        padding: 10px 0;
        .icon-vue {
          position: absolute;
          left: 50%;
          top: 50%;
          transform: translate(-50%, -50%);
          font-size: 20rem;
          &#fail-bg-icon { color: rgba($col-fail, .05); }
          &#success-bg-icon { color: rgba($col-success, .05); }
        }
        .success-results, .fail-results {
          position: relative;
          padding: 0 10px;
          overflow-y: auto;
          .result-line {
            font-weight: 600;
            font-size: 14px;
            padding: 4px 8px;
            border-radius: 4px;
            margin: 10px 0;
            &:first-child { margin-top: 0; }
            &:last-child { margin-bottom: 0; }
          }
          &.success-results .result-line {
            border: 1px solid $col-success;
            background-color: rgba($col-success, .1);
            color: $col-success;
          }
          &.fail-results .result-line {
            border: 1px solid $col-fail;
            background-color: rgba($col-fail, .1);
            color: $col-fail;
          }
        }
      }
    }
  }
}
</style>

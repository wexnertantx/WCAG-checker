<template>
  <div class="settings set-api">
    <div class="settings-section">API Key Configuration</div>
    <div class="settings-wrapper">
      <div class="input-wrapper">
        <label for="detectlanguage" class="input-label">DetectLanguage API Key:</label>
        <input id="detectlanguage" v-model="getAPIConfig.detectlanguage" @input="onChange" />
      </div>
    </div>
    <div class="settings-controls">
      <Button v-if="isChanged" v-bind="buttons.reset" :pending="$store.getters['config/isConfigActionPending']">Reset Changes</Button>
      <Button v-if="isChanged" v-bind="buttons.save" :pending="$store.getters['config/isConfigActionPending']">Save Changes</Button>
    </div>
  </div>
</template>

<script>
import Button from '@/components/Button.component.vue';

export default {
  components: { Button },
  data() {
    return {
      isChanged: false,
      buttons: {
        save: { name: 'save', type: 'dialog', icon: 'save', click: this.save },
        reset: { name: 'reset', type: 'dialog', icon: 'x-circle', click: this.reset },
      },
    };
  },
  computed: {
    getAPIConfig() {
      return this.$store.getters['config/getConfig'].api;
    },
  },
  methods: {
    onChange() {
      this.isChanged = true;
    },
    save() {
      this.$store.dispatch('config/saveConfigByKey', 'api');
      this.isChanged = false;
    },
    reset() {
      this.$store.dispatch('config/loadConfigByKey', 'api');
      this.isChanged = false;
    },
  },
};
</script>

<style lang="scss" scoped>
.settings-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.settings-controls {
  display: flex;
  justify-content: center;
}
.input-wrapper {
  display: flex;
  margin: 10px 0;
  align-items: center;
  column-gap: 10px;
  .input-label {
    font-weight: 600;
    font-size: 14px;
  }
  input {
    flex: 1;
    background-color: rgba(black, 0.25);
    border-radius: 4px;
    padding: 4px 8px;
    min-width: 400px;
  }
}
</style>

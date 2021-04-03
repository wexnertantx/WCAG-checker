<template>
  <div class="settings set-api">
    <div class="settings-section">API Key Configuration</div>
    <div class="settings-wrapper">
      <div class="input-wrapper">
        <label for="detectlanguage" class="input-label">DetectLanguage API Key:</label>
        <input id="detectlanguage" v-model="getAPIConfig.detectlanguage" />
      </div>
    </div>
    <div class="settings-controls">
      <Button v-bind="buttons.save">Save Changes</Button>
    </div>
  </div>
</template>

<script>
import Button from '@/components/Button.component.vue';

export default {
  components: { Button },
  data() {
    return {
      buttons: {
        save: { name: 'exit', type: 'dialog', icon: 'power-off', click: this.save },
      },
    };
  },
  computed: {
    getAPIConfig() {
      return this.$store.getters['config/getConfig'].api;
    },
  },
  methods: {
    save() {
      console.log('saving');
    },
  },
};
</script>

<style lang="scss">
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

<template>
  <div class="home">
    <div class="start-wrapper">
      <input placeholder="<website address>" v-model="website" />
      <Button v-bind="buttons.run">Run driver</Button>
    </div>
  </div>
</template>

<script>
import Button from '@/components/Button.component.vue';

export default {
  name: 'Home',
  components: { Button },
  data() {
    return {
      buttons: {
        run: { name: 'run-driver', type: 'dialog', icon: 'arrow_right', inverse: true, click: () => this.run() },
      },
      website: '',
    };
  },
  methods: {
    run() {
      if (!this.website.length) {
        console.error('website is empty');
        return;
      }
      window.eel.run_rules('chrome', this.website);
    },
  },
};
</script>

<style lang="scss">
@import '@/scss/_mixins';

.start-wrapper {
  input {
    @include set-placeholder($apricot);
  }
}
</style>

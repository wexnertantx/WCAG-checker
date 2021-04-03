<template>
  <div class="icon-vue" :class="[ isDisabled ]">
    <img v-if="img" :src="getImage" :class="[ getIcon ]" />
    <i v-else class="icon" :class="[ getIcon ]"></i>
  </div>
</template>

<script>
export default {
  name: 'VUEIcon',
  props: ['name', 'disabled', 'click', 'img'],
  computed: {
    isDisabled() {
      return (this.disabled) ? 'disabled' : false;
    },
    getImage() {
      return require(`../assets/images/${this.img}.png`); // eslint-disable-line
    },
    getIcon() {
      return `icon-${this.name}`;
    },
  },
};
</script>

<style lang="scss" scoped>
@import '@/scss/_mixins';

@include font-face('icon', '../assets/fonts/Icon/cs27-ico', normal, normal, ttf woff svg, 'block', '79mks0');

.icon {
  position: relative;
  display: flex;
  align-items: center;
  font-family: 'icon' !important;
  font-style: normal;
  font-weight: normal;
  font-variant: normal;
  text-transform: none;
  line-height: 1;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.icon-arrow_right:before { content: $icon-arrow_right; }
.icon-settings:before { content: $icon-settings; }
.icon-power-off:before { content: $icon-power-off; }
.icon-refresh:before { content: $icon-refresh; }
.icon-pause:before { content: $icon-pause; }
.icon-stop:before { content: $icon-stop; }
.icon-play:before { content: $icon-play; }
.icon-spinner:before {
  content: $icon-spinner;
  animation: spin 2s linear infinite;
}
.icon-calendar-check:before { content: $icon-calendar-check; }
.icon-home:before { content: $icon-home; }
.icon-cancel-circle:before { content: $icon-cancel-circle; }
.icon-check-circle-f:before { content: $icon-check-circle-f; }
.icon-clear:before { content: $icon-clear; }
.icon-x-circle:before { content: $icon-x-circle; }
.icon-help-circle:before { content: $icon-help-circle; }
.icon-alert-circle:before { content: $icon-alert-circle; }
.icon-minus-circle:before { content: $icon-minus-circle; }
.icon-check-circle:before { content: $icon-check-circle; }
.icon-circle:before { content: $icon-circle; }
.icon-spinner2:before {
  content: $icon-spinner2;
  animation: spin 2s linear infinite;
}
.icon-external-link:before { content: $icon-external-link; }
.icon-save:before { content: $icon-save; }
.icon-key:before { content: $icon-key; }
.icon-check:before { content: $icon-check; }
.icon-firefox:before { content: $icon-firefox; }
.icon-chrome:before { content: $icon-chrome; }
</style>

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
</style>

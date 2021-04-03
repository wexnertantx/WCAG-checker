<template>
  <div class="divider-vue" :class="[ isVertical ]" />
</template>

<script>
export default {
  props: ['vertical'],
  computed: {
    isVertical() {
      return (this.vertical) ? 'vertical' : 'horizontal';
    },
  },
};
</script>

<style lang="scss">
.divider-vue {
  &.horizontal {
    height: 1px;
    background: linear-gradient(to right, rgba(4,6,32,0), rgba(244,244,245,.5), rgba(4,6,32,0));
    margin: 15px 0;
  }
  &.vertical {
    width: 1px;
    background: linear-gradient(rgba(4,6,32,0), rgba(244,244,245,.5), rgba(4,6,32,0));
    margin: 0 15px;
  }
}
</style>

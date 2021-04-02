<template>
  <transition @enter="enter" @leave="leave" @afterEnter="afterEnter" appear>
    <div v-show="visible" class="dropdown-vue" :class="[ type, isInline ]">
      <component v-if="custom" :is="custom" :id="getId" class="dropdown" />
      <div v-else :id="getId" class="dropdown">
        <DropdownButton
          v-for="(item, id) in items"
          :key="id"
          v-bind="item"
          :name="getItemName(id)"
          :click="() => select(item)" />
      </div>
    </div>
  </transition>
</template>

<script>
import Velocity from 'velocity-animate';

import { defineAsyncComponent } from 'vue';

export default {
  name: 'VUEDropdown',
  components: {
    DropdownButton: defineAsyncComponent(() => import('./Button.component')),
  },
  props: ['id', 'custom', 'type', 'items', 'visible', 'selected', 'noselect', 'inline'],
  emits: ['update:selected', 'update:visible'],
  mounted() {
    if (!this.selected) {
      this.select(this.items.find(item => item.default));
    }
  },
  computed: {
    getId() {
      return `dropdown-${this.id}`;
    },
    isInline() {
      return (this.inline) ? 'inline' : null;
    },
  },
  methods: {
    getItemName(item) {
      return `${item}-${this.getId}`;
    },
    select(item) {
      if (this.noselect) return;
      this.$emit('update:visible', false);
      this.$emit('update:selected', item);
    },
    /**
     * Animation functions for enter and leave
     */
    enter(el, done) {
      // Auto determine the height of the dropdown menu
      [el] = el.children;
      el.style.height = 'auto';
      const maxHeight = parseInt(el.style.maxHeight.substr(0, el.style.maxHeight.length - 2));
      const height = (el.offsetHeight > maxHeight) ? maxHeight : el.offsetHeight;
      el.style.height = 0; // eslint-disable-line
      el.style.overflowY = 'hidden';
      Velocity(el, 'stop');
      Velocity(el.children, 'stop');
      Velocity(el, { height }, { easing: 'swing', duration: 200 });
      Velocity(el.children, { opacity: 1 }, { easing: 'swing', duration: 200, delay: 200, complete: done });
    },
    afterEnter(el) {
      [el] = el.children;
      el.style.height = 'auto';
      el.style.overflowY = 'auto';
    },
    leave(el, done) {
      [el] = el.children;
      el.style.overflowY = 'hidden';
      Velocity(el, 'stop');
      Velocity(el.children, 'stop');
      Velocity(el.children, { opacity: 0 }, { easing: 'swing', duration: 200 });
      Velocity(el, { height: 0 }, { easing: 'swing', duration: 200, delay: 200, complete: done });
    },
  },
};
</script>

<style lang="scss">
.dropdown-vue {
  position: relative;
  flex: 1;
  &:not(.inline) {
    position: absolute;
    left: 0;
    right: 0;
    top: 100%;
    padding-top: 10px;
    z-index: 5;
  }
  // &:before, &:after {
  //   content: "";
  //   position: absolute;
  //   &.inline {
  //     position: relative;
  //   }
  //   left: 50%;
  //   transform: translateX(-50%);
  //   border-style: solid;
  //   z-index: 1;
  // }
  // &:before {
  //   bottom: calc(100% - 10px);
  //   border-width: 0 6px 6px 6px;
  //   border-style: solid;
  //   border-color: $col-blue transparent;
  //   z-index: 1;
  // }
  // &:after {
  //   bottom: calc(100% - 11px);
  //   border-width: 0 6px 6px 6px;
  //   border-color: $col-blue transparent;
  // }
  .dropdown {
    display: flex;
    flex-direction: column;
    box-sizing: border-box;
    border-top: 1px solid $apricot;
    background-color: $col-blue;
    border-radius: 4px;
    // box-shadow: 0 0 20px #000;
    overflow-y: auto;
  }
}
</style>

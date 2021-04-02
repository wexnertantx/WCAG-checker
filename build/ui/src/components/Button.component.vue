<template>
  <div class="button-vue" v-tooltip="{ ...tooltip }">
    <router-link v-if="href" :to="href" class="button" :class="[ getName, getStyle, isActive ]">
      <Icon v-if="icon" :name="icon"></Icon>
      <span v-if="getText || $slots.default" class="text"><slot>{{ getText }}</slot></span>
    </router-link>
    <div v-else class="button" :class="[ getName, getStyle, isDisabled, isActive, { 'pending': isPending } ]" @click.capture="OnButtonClick">
      <Icon v-if="icon" :name="getIcon"></Icon>
      <span v-if="getText || $slots.default" class="text"><slot>{{ getText }}</slot></span>
    </div>
    <Dropdown
      v-if="_dropdown && _dropdown.items"
      v-bind="_dropdown"
      v-model:selected="_dropdown.selected"
      v-model:visible="_dropdown.visible"
    />
  </div>
</template>

<script>
import Dropdown from './Dropdown.component';
import Icon from './Icon.component';

export default {
  name: 'VUEButton',
  components: { Icon, Dropdown },
  props: ['name', 'href', 'type', 'icon', 'text', 'click', 'disabled', 'active', 'pending', 'tooltip', 'dropdown'],
  emits: ['update:dropdown'],
  data() {
    return {
      _dropdown: this.dropdown,
    };
  },
  computed: {
    getName() {
      return (this.name) ? `btn-${this.name}` : null;
    },
    getText() {
      let { text } = this;
      if (this._dropdown) {
        text = this._dropdown?.selected?.text || this._dropdown?.title || '...';
      }
      return text;
    },
    getStyle() {
      return (this.type) ? `${this.type}-style` : null;
    },
    getIcon() {
      return (this.isPending) ? 'spinner' : this.icon;
    },
    isActive() {
      return (this._dropdown?.visible || this.$route.path.slice(1) === this.href) ? 'active' : false;
    },
    isDisabled() {
      return (this.disabled) ? 'disabled' : null;
    },
    isPending() {
      return this.pending;
    },
  },
  methods: {
    async OnButtonClick() {
      if (this.disabled) return false;
      if (this._dropdown) {
        this._dropdown.visible = !this._dropdown.visible;
      }
      if (typeof (this.click) !== 'function') return false;
      return this.click();
    },
  },
  watch: {
    _dropdown: {
      deep: true,
      handler(next) {
        this.$emit('update:dropdown', next);
      },
    },
  },
};
</script>

<style lang="scss" scoped>
@import '@/scss/_mixins.scss';

.button-vue {
  display: flex;
  position: relative;
  flex-direction: column;
  .button {
    flex: 1;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    color: black;
    font-weight: 300;
    white-space: nowrap;
    cursor: pointer;
    .text {
      text-align: center;
      &:nth-child(2) { margin-left: 4px; }
    }
    .icon-vue {
      position: relative;
      &:nth-child(2) { margin-left: 4px; }
    }
    &.inversed {
      .text { order: 1; }
      .icon-vue { order: 2; }
    }
    &.disabled {
      cursor: default;
      opacity: .4;
    }
    @include disable-select();
  }

  .icon-style {
    color: rgba($col-text, .6);
    @include transition('color', .4s, ease);
    &:not(.disabled):not(.pending) {
      &.is-active, &:hover {
        color: $col-text;
      }
    }
  }

  .menu-style {
    justify-content: flex-start;
    padding: 20px;
    border-radius: 4px;
    font-size: 14px;
    color: rgba($col-text, .6);
    @include transition('background-color, padding-left', .2s, ease);
    .text:nth-child(2) { margin-left: 15px; }
    .icon-vue {
      font-size: 20px;
      opacity: .4;
    }
    &:not(.disabled):not(.pending) {
      &:hover {
        background-color: rgba(black, .25);
        padding-left: 30px;
      }
      &.is-active, &.router-link-exact-active {
        font-weight: 600;
        color: $col-text-def;
      }
    }
  }

  .menu-sub-style {
    justify-content: flex-start;
    padding: 5px 20px;
    border-radius: 4px;
    font-size: 14px;
    color: rgba($col-text, .6);
    @include transition('background-color, padding-left', .2s, ease);
    .text:nth-child(2) { margin-left: 15px; }
    .icon-vue {
      font-size: 20px;
      opacity: .4;
    }
    &:not(.disabled):not(.pending) {
      &:hover {
        background-color: rgba(black, .25);
        padding-left: 30px;
      }
      &.is-active, &.router-link-exact-active {
        font-weight: 600;
        color: $col-text-def;
      }
    }

    &.red { color: #FF6347; }
    &.green { color: #C8F902; }
  }

  .bzard-style {
    padding: 6px 16px;
    background-color: darken($apricot, 15%);
    color: black;
    box-shadow: 0 1px 1px rgba(black, .3), 0 0 1px 1px rgba(white, .15) inset;
    @include transition('background-color, box-shadow', .2s, ease);
    &:hover:not(.disabled) {
      background-color: darken($apricot, 20%);
    }
  }

  .dialog-style {
    padding: 8px 20px;
    border-top: 1px solid transparent;
    border-bottom: 1px solid transparent;
    border-radius: 3px;
    background: linear-gradient(to bottom, darken($apricot, 10%), darken($apricot, 20%));
    background-blend-mode: screen;
    color: black;
    font-weight: 500;
    box-shadow: 0 1px 2px rgba(black, .8), 0 0 1px 1px rgba(white, .15) inset;
    @include transition('background-color, border', .2s, ease);
    &:not(.disabled) {
      &.is-active, &:hover {
        background-color: darken($apricot, 35%);
        border-color: $apricot;
      }
    }

    &.tag {
      padding: 2px 6px;
      border-radius: 2px;
      color: $apricot;
      font-size: 10px;
      font-weight: 700;
    }

    &.red {
      background: linear-gradient(to bottom, #dd4a36, darken(#dd4a36, 10%));
      color: lighten(#dd4a36, 40%);
      &:hover:not(.disabled) {
        background-color: darken(#c93737, 35%);
        border-color: #c93737;
      }
    }
    &.blue {
      background: linear-gradient(to bottom, #7289da, darken(#7289da, 10%));
      color: lighten(#7289da, 30%);
      &:hover:not(.disabled) {
        background-color: darken(#7289da, 35%);
        border-color: #7289da;
      }
    }
  }

  .border-style {
    padding: 4px 14px;
    border: 1px solid $apricot;
    border-width: 2px 0;
    border-radius: 4px;
    color: $apricot;
    font-weight: 400;
    @include transition('background-color, color', .2s, ease);
    &:hover {
      background-color: rgba($apricot, .1);
      color: lighten($apricot, 10%);
    }
  }

  .search-style {
    padding: 8px 20px;
    border-radius: 0 6px 6px 0;
    background: linear-gradient(to bottom, darken($apricot, 10%), darken($apricot, 20%));
    background-blend-mode: screen;
    font-weight: 600;
    color: black;
    @include transition('background-color, border', .2s, ease);
    &:before {
      content: "";
      position: absolute;
      top: 0;
      bottom: 0;
      left: 0;
      right: 0;
      border-radius: 0 6px 6px 0;
      box-shadow: 1px 0 0 darken($apricot, 45%), -1px 0 0 darken($apricot, 45%);
    }
    &:not(.disabled) {
      &.active, &:hover {
        background-color: darken($apricot, 35%);
        border-color: $apricot;
      }
    }
  }

  .dropdown-style {
    justify-content: flex-start;
    padding: 8px 12px;
    color: $apricot;
    font-size: 14px;
    font-weight: 600;
    @include transition('background-color, color', .4s, ease);
    .text { @include transition('padding', .2s, ease); }
    &:hover, &.active {
      background-color: lighten($dark-apricot, 10%);
      color: lighten($apricot, 20%);
      .text { padding-left: 5px; }
    }
  }
}
</style>

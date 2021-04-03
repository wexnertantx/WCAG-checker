<template>
  <div class="checkbox-vue">
    <input :id="getId" :name="getId" type="checkbox" v-model="model" tabIndex="0" :disabled="pending">
    <label :for="getId"><slot>{{ label }}</slot></label>
  </div>
</template>

<script>
export default {
  name: 'VUECheckbox',
  props: ['id', 'label', 'selected', 'pending'],
  emits: ['update:selected'],
  computed: {
    getId() {
      return (this.id) ? `checkbox-${this.id}` : null;
    },
    model: {
      get() {
        return this.selected;
      },
      set(value) {
        this.$emit('update:selected', value);
      },
    },
  },
};
</script>

<style lang="scss" scoped>
@import '@/scss/_mixins.scss';

.checkbox-vue {
  position: relative;
  display: flex;
  label {
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    font-size: 0.9em;
    font-weight: 600;
    cursor: pointer;
    @include transition('color, text-shadow', .2s, ease);
    &:hover {
      color: lighten($col-lblue, 20%);
      text-shadow: 0 0 1px $col-lblue;
    }
    &:before {
      box-sizing: border-box;
      position: relative;
      content: $icon-check;
      margin-right: 5px;
      border-radius: 4px;
      font-family: 'icon';
      padding: 2px;
      font-size: 18px;
      color: rgba($col-lblue, 0);
      background-color: #040620;
      text-shadow: none;
      @include transition('color', .15s, ease);
    }
    @include disable-select();
  }

  input {
    position: absolute;
    display: none;
    visibility: hidden;
    &:checked + label:before {
      color: $col-lblue;
      text-shadow: none;
    }
  }
}
</style>

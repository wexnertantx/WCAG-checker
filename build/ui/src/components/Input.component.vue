<template>
  <div class="input-vue" :class="[ hasFailed ]">
    <div class="inner-input">
      <label v-if="label" :for="getId" class="label">{{ label }}</label>
      <input v-else :id="getId" :name="getId" :type="getInputType" :placeholder="placeholder" v-model="model" :maxlength="maxlength" tabIndex="0" />
    </div>
    <Icon v-if="error" class="error" name="warning" v-tooltip="{ type: 'alert', text: error }"></Icon>
  </div>
</template>

<script>
import Icon from '@/components/Icon.component';

export default {
  name: 'InputComponent',
  components: { Icon },
  props: ['id', 'label', 'type', 'maxlength', 'placeholder', 'value', 'error', 'condition'],
  emits: ['update:value'],
  computed: {
    getId() {
      return (this.id) ? `input-${this.id}` : null;
    },
    hasFailed() {
      return (this.error) ? 'failed' : null;
    },
    getInputType() {
      return this.type || 'text';
    },
    getCharLimit() {
      return (this.maxlength) ? `Remaining characters: ${this.maxlength - this.value.length}` : null;
    },
    isTextarea() {
      return (this.getInputType === 'textarea');
    },
    isCondition() {
      if (typeof (this.condition) !== 'function') return true;
      return this.condition();
    },
    model: {
      get() {
        return this.value;
      },
      set(value) {
        if (this.maxlength && value.length > this.maxlength) {
          value = value.substring(0, this.maxlength);
        }
        this.$emit('update:value', value);
      },
    },
  },
};
</script>

<style lang="scss">
@import '@/scss/_mixins';

@keyframes fxerror { 0% { opacity: 0; } 50% { opacity: 1; color: lighten($error, 10%); } 100% { color: $error; } }

.input-vue {
  position: relative;
  display: flex;
  margin: 10px 0;
  &:nth-child(1) { margin-top: 20px; }
  &:nth-child(2) { margin-bottom: 20px; }
  .inner-input {
    flex: 1;
    position: relative;
    display: flex;
    flex-direction: column;
    padding: 6px 4px;
    background-color: rgba($col-blue, .1);
    border: 1px solid $col-blue;
    border-top: none;
    border-radius: 4px;
    label {
      display: flex;
      position: absolute;
      font-size: 10px;
      font-weight: 700;
      left: 0; right: 0; top: -4px;
      &::before, &::after {
        content: "";
        position: relative;
        top: 4px;
        height: 0.5px;
        background-color: $col-blue;
      }
      &::before {
        width: 16px;
        left: 2px;
        margin-right: 8px;
      }
      &::after {
        flex: 1;
        right: 2px;
        margin-left: 8px;
      }
      @include disable-select();
    }
    input, textarea {
      position: relative;
      flex: 1;
      font-weight: 600;
      @include set-placeholder($col-blue);
      z-index: 1;
    }
    textarea {
      resize: none;
      min-height: 20px;
    }
    .input-limit {
      position: absolute;
      bottom: 2px; right: 2px;
      font-family: 'Open Sans';
      font-size: 10px;
      font-weight: 600;
      color: rgba($col-blue, .4);
      @include disable-select();
    }
  }
  .error {
    display: flex;
    align-self: center;
    padding: 0 4px;
    color: $error;
    font-size: 18px;
    animation: .4s fxerror ease-in-out;
  }
}
</style>
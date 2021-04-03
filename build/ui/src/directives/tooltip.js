import store from '../store/index';

function show({ type, text } = {}) {
  if (this.getAttribute('unbinding')) return;
  store.commit('showTooltip', { element: this, type, text });
}

function hide() {
  store.commit('hideTooltip');
}

const directive = {
  beforeMount(el, binding) {
    if (!binding.value.text) return;
    el.addEventListener('mouseenter', show.bind(el, binding.value));
    el.addEventListener('mouseleave', hide);
  },
  beforeUnmount(el, binding) {
    if (!binding.value.text) return;
    el.setAttribute('unbinding', true);
    // If a tooltip is active, hide it if belongs to the unbound element
    el.removeEventListener('mouseenter', show.bind(el, binding.value));
    el.removeEventListener('mouseleave', hide);
    if (!store.state.tooltip) return;
    if (el === store.state.tooltip.element) {
      hide();
    }
  },
};

export default directive;

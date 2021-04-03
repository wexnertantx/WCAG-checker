<template>
  <div class="widget-vue">
    <div class="widget-title">{{ getTitle }}</div>
    <div class="widget-data">
      <div v-for="(panel, i) in panels" :key="i" class="widget-panel">
        <div class="widget-panel-header">{{ panel.header }}</div>
        <div class="widget-panel-data">{{ panel.data }}</div>
      </div>
    </div>
    <div v-if="bar" class="widget-info">
      <div class="bar">
        <div class="bar-progress" :style="getBarStyle" />
      </div>
      <div class="info">
        <span class="number">{{ (bar.ratio * 100).toFixed(2) }}%</span>
        <span class="text">&nbsp;{{ bar.info }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['title', 'panels', 'bar'],
  computed: {
    getTitle() {
      return this.title;
    },
    getBarStyle() {
      return {
        width: `${this.bar.ratio * 100}%`,
        backgroundColor: this.bar.color,
      };
    },
  },
};
</script>

<style lang="scss">
.widget-vue {
  position: relative;
  display: flex;
  flex-direction: column;
  width: 400px;
  padding: 0 20px 20px 20px;
  border-radius: 8px;
  background-color: rgba(black, .25);
  .widget-title {
    font-weight: 300;
    font-size: 14px;
    margin: 20px 0;
  }
  .widget-data {
    display: flex;
    column-gap: 40px;
    .widget-panel {
      display: flex;
      flex-direction: column;
      row-gap: 2px;
      .widget-panel-header {
        font-weight: 500;
        font-size: 13px;
      }
      .widget-panel-data { color: rgba($col-text, .6); }
    }
  }
  .widget-info {
    display: flex;
    flex-direction: column;
    .bar {
      position: relative;
      height: 5px;
      margin: 20px 0 5px 0;
      border-radius: 2px;
      background-color: #474d84;
      .bar-progress {
        position: absolute;
        left: 0; top: 0;
        height: 5px;
        border-radius: 2px;
      }
    }
    .info {
      font-size: 13px;
      .number { font-weight: 600; }
      .text { color: rgba($col-text, .6); }
    }
  }
}
</style>

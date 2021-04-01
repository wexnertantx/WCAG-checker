<template>
  <header>
    <div class="logo">
      <div class="logo-img"></div>
      <div class="name">
        <div class="team">CS27</div>
        <div class="dashboard">Dashboard</div>
      </div>
    </div>
    <div class="navigation">
      <Button v-bind="buttons.settings" />
      <Button v-bind="buttons.exit" />
    </div>
  </header>
  <router-view class="page" />
  <!-- <div id="nav">
    <router-link to="/">Home</router-link> |
    <router-link to="/about">About</router-link>
  </div> -->
</template>

<script>
import Button from '@/components/Button.component.vue';

export default {
  components: { Button },
  data() {
    return {
      buttons: {
        settings: { name: 'settings', type: 'bzard', icon: 'settings', click: () => { } },
        exit: { name: 'exit', type: 'bzard', icon: 'power-off', click: this.exit },
      },
    };
  },
  methods: {
    exit() {
      window.close();
    },
  },
};
</script>

<style lang="scss">
@import '@/scss/_reset';
@import '@/scss/_normalize';
@import '@/scss/_fonts';

html, body, #app {
  display: flex;
  flex: 1;
  min-height: 100vh;
  font-size: 14px;
}

#app {
  flex-direction: column;
  font-family: Open-Sans, Helvetica, Arial, sans-serif;
  font-weight: 400;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: $col-blue;

  header {
    display: flex;
    align-items: center;
    min-height: 100px;
    padding: 0 40px;
    border-bottom: 1px solid darken($col-bg, 10%);
    background-color: darken($col-bg, 30%);

    .logo {
      display: flex;
      flex-direction: row;
      align-items: center;
      .logo-img {
        width: 80px;
        height: 80px;
        background-color: $col-blue;
      }
      .name {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        margin-left: 10px;
        font-size: 30px;
        .team {
          font-weight: 600;
        }
      }
    }

    .navigation {
      flex: 1;
      display: flex;
      flex-direction: row;
      justify-content: flex-end;
      > * {
        margin: 0 5px;

      }
    }
  }

  .page {
    background-color: darken($col-bg, 35%);
    border-top: 1px solid darken($col-bg, 50%);
    position: relative;
    display: flex;
    flex: 1;
  }
}

a {
  color: inherit;
  outline: none;
  text-decoration: inherit;
  transition: color .2s ease;
  &/*:not(.router-link-active)*/:hover {
    color: lighten($col-blue, 20%);
    text-shadow: 0 0 1px $col-blue;
  }
}

input, textarea {
  border: none;
  background: none;
  outline: none;
  overflow: hidden;
  color: $apricot;
}
</style>

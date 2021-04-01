module.exports = {
  css: {
    loaderOptions: {
      scss: {
        prependData: '@import "@/scss/_constants.scss";',
      },
    },
  },
};
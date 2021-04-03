module.exports = {
  outputDir: 'build',
  css: {
    loaderOptions: {
      scss: {
        prependData: '@import "@/scss/_constants.scss";',
      },
    },
  },
  chainWebpack: (config) => {
    config
      .plugin('html')
      .tap((args) => {
        args[0].title = 'CS27: WCAG Accesibility Analyzer';
        return args;
      });
  },
};

module.exports = {
  root: true,
  env: {
    node: true,
  },
  extends: [
    'plugin:vue/vue3-essential',
    '@vue/airbnb',
  ],
  parserOptions: {
    parser: 'babel-eslint',
  },
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'max-len': ['error', { code: 150 }],
    'object-curly-newline': ['error', { consistent: true }],
    'arrow-parens': [2, 'as-needed', { requireForBlockBody: true }],
    'no-plusplus': 'off',
    'import/extensions': 'off',
    'no-bitwise': 'off',
    'no-param-reassign': 'off',
    'vue/no-reserved-keys': 'off',
    'no-underscore-dangle': ['error', { allowAfterThis: true }],
    radix: ['error', 'as-needed'],
  },
};

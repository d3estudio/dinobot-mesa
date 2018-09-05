<template>
  <router-view class="uk-background-muted uk-height-viewport"/>
</template>

<style lang="less">
  @import '~uikit/src/less/uikit.theme.less';

  html,
  body {
    height: 100%;
    font-weight: 300;
  }

  @global-primary-background: #bc1931;

  .uk-text-bold {
    font-weight: 700;
  }
</style>

import Vue from 'vue';

import UIkit from 'uikit';
import UIkitIcons from 'uikit/dist/js/uikit-icons';

import App from './App.vue';
import router from './router';
import store from './store';

/**
 * Global Vue config
 */
Vue.config.productionTip = false;

/**
 * Global UIkit config
 */
UIkit.use(UIkitIcons);

/**
 * Initialize Application
 */
global.Application = new Vue({ store, router, render: h => h(App) }).$mount('#app');

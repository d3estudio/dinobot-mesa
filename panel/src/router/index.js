import Vue from 'vue';
import VueRouter from 'vue-router';

import store from '../store';
import login from '../components/Login.vue';
import home from '../components/Home.vue';

Vue.use(VueRouter);

export default new VueRouter({
  linkActiveClass: 'uk-active',
  linkExactActiveClass: 'uk-active',
  routes: [
    {
      path: '/',
      redirect: { name: 'home' },
    },
    {
      path: '/home',
      name: 'home',
      component: home,
      beforeEnter(to, from, next) {
        if (store.getters.isLoggedIn) {
          next();
        } else {
          next({ name: 'login', query: { redirect: to.fullPath } });
        }
      },
    },
    {
      path: '/login',
      name: 'login',
      component: login,
    },
    {
      path: '/logout',
      name: 'logout',
      beforeEnter(to, from, next) {
        store.dispatch('logout');
        next({ name: 'login' });
      },
    },
  ],
});

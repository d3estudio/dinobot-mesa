import Vue from 'vue';
import Vuex from 'vuex';
import Cookie from 'js-cookie';

import Client from '../api';

const AUTH_TOKEN = 'AUTH_TOKEN';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    token: Cookie.get(AUTH_TOKEN),
  },
  mutations: {
    LOGIN(state, { data }) {
      if (data.AuthToken) {
        Object.assign(state, { token: data.AuthToken });
        Cookie.set(AUTH_TOKEN, data.AuthToken);
      }
    },
    LOGOUT(state) {
      Object.assign(state, { token: null });
      Cookie.remove(AUTH_TOKEN);
    },
  },
  actions: {
    async login({ commit }, { domain, email, password }) {
      const response = await Client.post('auth/authenticate-user', {
        Domain: domain,
        Login: email,
        LoginType: 1,
        Password: password,
      });
      commit('LOGIN', response);
    },
    async logout({ commit }) {
      commit('LOGOUT');
    },
  },
  getters: {
    isLoggedIn: state => !!state.token,
  },
});

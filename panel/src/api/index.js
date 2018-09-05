import axios from 'axios';
import UIkit from 'uikit';

import router from '../router';
import store from '../store';

const Client = axios.create({
  baseURL: 'https://api-erp.marketup.com/v1/',
  responseType: 'json',
  timeout: 60000,
});

Client.interceptors.request.use((config) => {
  const Authorization = `Bearer ${store.state.token}`;

  // Immutably merges Authorization in headers
  const headers = Object.assign({}, config.headers, { Authorization });

  // Immutably merges headers in config
  return Object.assign({}, config, { headers });
});

Client.interceptors.response.use(null, (reason) => {
  // Clears authentication token if expired
  if (reason.response.status === 401) {
    router.push({ name: 'logout' });
  } else {
    UIkit.notification(reason.message, { status: 'danger' });
  }

  return Promise.reject(reason);
});

export default Client;

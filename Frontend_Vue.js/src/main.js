import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify';
import router from './router'
import store from './store'
import VueSweetalert2 from 'vue-sweetalert2';

Vue.config.productionTip = false
Vue.use(VueSweetalert2);

new Vue({
  vuetify,
  router,
  store,
  VueSweetalert2,
  render: h => h(App)
}).$mount('#app')

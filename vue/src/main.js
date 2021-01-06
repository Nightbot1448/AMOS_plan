// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import App from './App';
import router from './router';
import Preparation from './components/Preparation.vue';
import Task from './components/Task.vue';
import PlanningArea from './components/PlanningArea.vue';
import Planning from './components/Planning.vue';
import Conduct from './components/Conduct.vue';
import Processing from './components/Processing.vue';
import Adequacy from './components/Adequacy.vue';
import Docs from './components/Docs.vue';
import { store } from './store'

Vue.config.productionTip = false;
Vue.use(BootstrapVue)
Vue.use(IconsPlugin)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App, Preparation, 
    Task, PlanningArea,  Planning,
    Conduct, Processing, Adequacy, Docs},
  template: '<App/>',
  store: store
});

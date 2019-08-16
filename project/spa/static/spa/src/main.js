import Vue from 'vue'
import router from './router'
import BootstrapVue from 'bootstrap-vue'
import $ from 'jquery'
import bootstrap from 'bootstrap'
import 'malihu-custom-scrollbar-plugin'
import store from './store/Auth'
import App from './App'

Vue.config.productionTip = false
Vue.use(BootstrapVue)

/* Use `eslint-disable` to ignore all warnings in a file. */
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>',
  mounted: function () {
    this.tweakSidebar() // will execute at page load
  },
  methods: {
    tweakSidebar: function () {
      $('#sidebar').mCustomScrollbar({
        theme: 'minimal'
      })
    }
  }
})

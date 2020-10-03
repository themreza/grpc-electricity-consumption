import Vue from 'vue'
import Vuesax from 'vuesax'
import 'vuesax/dist/vuesax.css'
import 'd3-timeseries/src/d3_timeseries.css'
import App from './App.vue'
import { store } from './store/store'

Vue.config.productionTip = false
Vue.use(Vuesax)

new Vue({
  render: h => h(App),
  store,
}).$mount('#app')

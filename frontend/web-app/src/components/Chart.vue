<template>
  <div>
    <vs-alert v-if="error" color="danger" class="alert">
      <template #title>
        Oops - something went wrong!
      </template>
      {{ error }}
      <template #footer>
        <vs-button @click="reloadPage" danger>
          Try Again
        </vs-button>
      </template>
    </vs-alert>
    <div id="chart" class="text-center"></div>
  </div>
</template>

<script>
import d3_timeseries from 'd3-timeseries'
import { mapState } from 'vuex'

export default {
  name: 'Chart',
  data() {
    return {
      chart: null,
      loading: null
    }
  },
  watch: {
    meterData(val) {
      this.loading.close()
      if (this.chart != null) this.chart.remove()
      this.renderChart(val)
    }
  },
  methods: {
    reloadPage() {
      window.location.reload()
    },
    renderChart(data) {
      this.chart = d3_timeseries()
              .addSerie(data,{x:'timestamp',y:'value'},{interpolate:'monotone',color:"#00a87d"})
              .width(1200) // Todo: mobile optimization
      this.chart('#chart')
    }
  },
  mounted() {
    this.loading = this.$vs.loading({
      type: 'circles',
      color: '#00a87d',
      scale: 1
    })
    this.$store.dispatch('loadData')
  },
  computed: mapState([
    'meterData', 'error'
  ]),
}
</script>

<style scoped>
.alert {
  max-width: 600px;
  margin: 30px auto;
}
</style>

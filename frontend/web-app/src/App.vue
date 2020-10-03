<template>
  <div id="app">
    <div class="text-center">
      <h1>gRPC Electricity Consumption Web App</h1>
    </div>
    <chart/>
    <footer>
      Created by <a href="https://tomaraei.com">Mohammad Tomaraei</a>
    </footer>
  </div>
</template>

<script>
import Chart from './components/Chart.vue'

export default {
  name: 'App',
  components: {
    Chart
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  max-width: 1200px;
  text-align: center;
  margin: 30px auto;
}

footer {;
  margin-top: 30px;
}
</style>

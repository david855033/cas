<template>
  <div id="app">
    <patient-collection/>
  </div>
</template>

<script>
import PatientCollection from './components/PatientCollection.vue'

export default {
  name: 'app',
  components: {
    PatientCollection
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>

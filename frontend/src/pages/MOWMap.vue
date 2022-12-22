<template>
  <q-layout view="lHh Lpr lFf">
    <q-page-container>
      <q-page class="q-mx-lg" id="page">
        <h4>Meals on Wheels Delivery Routes</h4>
        <div class="row justify-around">
          <div class="q-mr-lg">
            <h5 class="q-ma-none row">Select Routes</h5>
            <div class="q-pa-md row">
              <q-option-group
                :options="routeOptions"
                type="checkbox"
                v-model="selectedRoutes"
              />
            </div>
            <q-checkbox v-model="showWaitlisted" label="Show Waitlisted" class="row" />
            <q-btn color="primary" label="Print selected" class="row q-mt-md" />
          </div>
          <iframe id="map" class="q-mt-md" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="https://www.openstreetmap.org/export/embed.html?bbox=-123.01851868629457%2C44.046311231687326%2C-123.01467776298524%2C44.05306625383836&amp;layer=mapnik&amp;marker=44.04968883906406%2C-123.01659822463989" style="border: 1px solid black"></iframe>
        </div>
        <q-input v-model="newAddress" label="Add a Delivery Address">
          <template v-slot:prepend>
            <q-icon name="place" />
          </template>
          <template v-slot:append>
            <q-icon name="close" @click="newAddress = ''" class="cursor-pointer" />
          </template>
        </q-input>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<style lang="scss"> 
  #page {
    max-width: 1200px;
  }

  #map {
    width: 900px;
    height: 500px;
  }
</style>

<script lang="ts">

import { Component, Vue } from 'vue-property-decorator'

@Component
export default class MOWMap extends Vue{
  public routeOptions = [
    { label: 'Gateway', value: 'gateway' },
    { label: 'Marcola', value: 'marcola', color: 'green' },
    { label: 'MC', value: 'mc', color: 'purple' },
    { label: 'PU', value: 'pu', color: 'orange' },
    { label: 'Short', value: 'short', color: 'red' },
    { label: 'Long', value: 'long', color: 'pink' },
    { label: 'North', value: 'north', color: 'yellow' },
    { label: 'Will', value: 'will', color: 'indigo' }
  ]
  public selectedRoutes = ['Gateway', 'Marcola', 'MC', 'PU', 'Short', 'Long', 'North', 'Will']
  public newAddress = ''
  public showWaitlisted = true
}
</script>

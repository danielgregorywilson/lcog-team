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
                @input="updateMapVisibility"
              />
            </div>
            <q-checkbox v-model="showWaitlisted" label="Show Waitlisted" class="row" />
            <q-btn color="primary" label="Print selected" class="row q-mt-md" />
          </div>
          <div id="map"></div>
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
import mapboxgl from "mapbox-gl";

@Component
export default class MOWMap extends Vue{
  public routeOptions = [
    { label: 'Gateway', value: 'Gateway', color: 'blue', addresses: [
      {
        'type': 'Feature',
        'geometry': {
          'type': 'Point',
          'coordinates': [-123.0062619, 44.0538149]
        }
      },
      {
        'type': 'Feature',
        'geometry': {
          'type': 'Point',
          'coordinates': [-122.9803587, 44.0482189]
        }
      },
      {
        'type': 'Feature',
        'geometry': {
          'type': 'Point',
          'coordinates': [-122.975543, 44.059392]
          }
      }
    ] 
    },
    { label: 'Marcola', value: 'Marcola', color: 'green', addresses: [] },
    { label: 'MC', value: 'MC', color: 'purple', addresses: [] },
    { label: 'PU', value: 'PU', color: 'orange', addresses: [] },
    { label: 'Short', value: 'Short', color: 'red', addresses: [] },
    { label: 'Long', value: 'Long', color: 'pink', addresses: [] },
    { label: 'North', value: 'North', color: 'yellow', addresses: [] },
    { label: 'Will', value: 'Will', color: 'indigo', addresses: [] }
  ]
  public selectedRoutes = ['Gateway', 'Marcola', 'MC', 'PU', 'Short', 'Long', 'North', 'Will']
  public newAddress = ''
  public showWaitlisted = true

  private accessToken = process.env.VUE_APP_MAP_ACCESS_TOKEN
  private map = {}
  private center = [-123.0044045, 44.0535664]
  private zoom = 13

  private gatewayVisibility() {
    if (this.selectedRoutes.includes('Gateway')) {
      return 'visible'
    } else {
      return 'none'
    }
  }

  private createMap() {
    try {
      this.map = new mapboxgl.Map({
        accessToken: this.accessToken,
        container: "map",
        style: "mapbox://styles/mapbox/streets-v11",
        center: this.center,
        zoom: this.zoom
      })
      this.map.addControl(new mapboxgl.NavigationControl());

      this.map.on('load', () => {
        for(let route of this.routeOptions) {
          // Add the vector tileset as a source.
          this.map.addSource(route.value + 'Routes', {
            'type': 'geojson',
            'data': {
              'type': 'FeatureCollection',
              'features': route.addresses
            }
          });
          
          this.map.addLayer({
            'id': route.value + '-routes',
            'type': 'circle',
            'source': route.value + 'Routes',
            'layout' : {
              'visibility': "visible"
            },
            'paint': {
              'circle-radius': 6,
              'circle-color': route.color
            },
            'filter': ['==', '$type', 'Point']
          });
        }
      });
      
    } catch (err) {
      console.log("Error rendering map:", err)
    }
    
  }

  mounted() {
    this.createMap()
  }

  updateMapVisibility() {
    for (let route of this.routeOptions) {
      if (this.selectedRoutes.includes(route.value)) {
        this.map.setLayoutProperty(route.value + '-routes', 'visibility', 'visible')
      } else {
        this.map.setLayoutProperty(route.value + '-routes', 'visibility', 'none')
      }
    }
  }

}
</script>

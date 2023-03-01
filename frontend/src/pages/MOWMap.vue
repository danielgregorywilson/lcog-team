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
import { VuexStoreGetters } from '../store/types'

type RouteName = 'Gateway' | 'Marcola' | 'MC' | 'PU' | 'Short' | 'Long' | 'North' | 'Will'
type RouteColor = 'blue' | 'green' | 'purple' | 'orange' | 'red' | 'pink' | 'yellow' | 'indigo'
type RouteGetter = 'mealsModule/gatewayStops' | 'mealsModule/marcolaStops' | 'mealsModule/MCStops' | 'mealsModule/PUStops' | 'mealsModule/shortStops' | 'mealsModule/longStops' | 'mealsModule/northStops' | 'mealsModule/willStops'

interface RouteOption {
  label: RouteName,
  value: RouteName,
  color: RouteColor,
  getter: RouteGetter
}

@Component
export default class MOWMap extends Vue{
  private getters = this.$store.getters as VuexStoreGetters

  public routeOptions: Array<RouteOption> = [
    { label: 'Gateway', value: 'Gateway', color: 'blue', getter: 'mealsModule/gatewayStops'},
    { label: 'Marcola', value: 'Marcola', color: 'green', getter: 'mealsModule/marcolaStops'},
    { label: 'MC', value: 'MC', color: 'purple', getter: 'mealsModule/MCStops'},
    { label: 'PU', value: 'PU', color: 'orange', getter: 'mealsModule/PUStops'},
    { label: 'Short', value: 'Short', color: 'red', getter: 'mealsModule/shortStops'},
    { label: 'Long', value: 'Long', color: 'pink', getter: 'mealsModule/longStops'},
    { label: 'North', value: 'North', color: 'yellow', getter: 'mealsModule/northStops'},
    { label: 'Will', value: 'Will', color: 'indigo', getter: 'mealsModule/willStops'}
  ]
  public selectedRoutes = ['Gateway', 'Marcola', 'MC', 'PU', 'Short', 'Long', 'North', 'Will']
  public newAddress = ''
  public showWaitlisted = true

  private accessToken = process.env.VUE_APP_MAP_ACCESS_TOKEN
  private map = {}
  private center = [-122.94329319107005, 44.08711374902461]
  private zoom = 10

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

          let addresses = []
          const stops = this.getters[route.getter]
          for (let address of stops) {
            if (address.route === route.value) {
              addresses.push({
                'type': 'Feature',
                'geometry': {
                  'type': 'Point',
                  'coordinates': [address.longitude, address.latitude]
                }
              })
            }
          }

          // Add the vector tileset as a source.
          this.map.addSource(route.value + 'Routes', {
            'type': 'geojson',
            'data': {
              'type': 'FeatureCollection',
              'features': addresses
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

      // When panning the map, update the center coordinates
      this.map.on('dragend', () => {
        const center = this.map.getCenter()
        this.center = [center.lng, center.lat]
      });
      
    } catch (err) {
      console.log("Error rendering map:", err)
    }
    
  }

  private getMealStops() {
    return new Promise((resolve, reject) => {
      this.$store.dispatch('mealsModule/getMealStops')
        .then(() => {
          resolve('Got meal stops')
        })
        .catch((err) => {
          reject(err)
        })
    })
  }

  mounted() {
    this.getMealStops()
      .then(() => {
        this.createMap()
      })
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

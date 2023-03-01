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
                class="col"
                :options="hotRouteOptions"
                type="checkbox"
                v-model="selectedRoutes"
                @input="updateMapVisibility"
              />
              <q-option-group
                class="col"
                :options="coldRouteOptions"
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

type RouteLabel = 'Gateway' | 'Marcola' | 'MC' | 'Short' | 'Long' | 'North' | 'Will' | 'Tu1' | 'Tu2' | 'Tu3' | 'Thur1' | 'Thur2' | 'Thur3' | 'PU'
type RouteName = 'Gateway' | 'Marcola' | 'MC' | 'Short' | 'Long' | 'North' | 'Will' | 'hotPU' | 'Tu1' | 'Tu2' | 'Tu3' | 'Thur1' | 'Thur2' | 'Thur3' | 'coldPU'
type RouteColor = 'red' | 'orange' | 'yellow' | 'green' | 'blue' | 'indigo' | 'violet' | 'pink'
type RouteGetter = 
  'mealsModule/gatewayStops' | 'mealsModule/marcolaStops' | 'mealsModule/MCStops' | 'mealsModule/shortStops' | 'mealsModule/longStops' |
  'mealsModule/northStops' | 'mealsModule/willStops' | 'mealsModule/hotPUStops' | 'mealsModule/tu1Stops' | 'mealsModule/tu2Stops' |
  'mealsModule/tu3Stops' | 'mealsModule/thur1Stops' | 'mealsModule/thur2Stops' | 'mealsModule/thur3Stops' | 'mealsModule/coldPUStops'

interface RouteOption {
  label: RouteLabel,
  value: RouteName,
  color: RouteColor,
  getter: RouteGetter
}

@Component
export default class MOWMap extends Vue{
  private getters = this.$store.getters as VuexStoreGetters

  public hotRouteOptions: Array<RouteOption> = [
    { label: 'Gateway', value: 'Gateway', color: 'red', getter: 'mealsModule/gatewayStops'},
    { label: 'Marcola', value: 'Marcola', color: 'orange', getter: 'mealsModule/marcolaStops'},
    { label: 'MC', value: 'MC', color: 'yellow', getter: 'mealsModule/MCStops'},
    { label: 'Short', value: 'Short', color: 'green', getter: 'mealsModule/shortStops'},
    { label: 'Long', value: 'Long', color: 'blue', getter: 'mealsModule/longStops'},
    { label: 'North', value: 'North', color: 'indigo', getter: 'mealsModule/northStops'},
    { label: 'Will', value: 'Will', color: 'violet', getter: 'mealsModule/willStops'},
    { label: 'PU', value: 'hotPU', color: 'pink', getter: 'mealsModule/hotPUStops'}
  ]
  public coldRouteOptions: Array<RouteOption> = [
    { label: 'Tu1', value: 'Tu1', color: 'red', getter: 'mealsModule/tu1Stops'},
    { label: 'Tu2', value: 'Tu2', color: 'orange', getter: 'mealsModule/tu2Stops'},
    { label: 'Tu3', value: 'Tu3', color: 'yellow', getter: 'mealsModule/tu3Stops'},
    { label: 'Thur1', value: 'Thur1', color: 'green', getter: 'mealsModule/thur1Stops'},
    { label: 'Thur2', value: 'Thur2', color: 'blue', getter: 'mealsModule/thur2Stops'},
    { label: 'Thur3', value: 'Thur3', color: 'violet', getter: 'mealsModule/thur3Stops'},
    { label: 'PU', value: 'coldPU', color: 'pink', getter: 'mealsModule/coldPUStops'}
  ]
  public selectedRoutes = ['Gateway', 'Marcola', 'MC', 'Short', 'Long', 'North', 'Will']
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
        for(let route of this.hotRouteOptions) {

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
    for (let route of this.hotRouteOptions) {
      if (this.selectedRoutes.includes(route.value)) {
        this.map.setLayoutProperty(route.value + '-routes', 'visibility', 'visible')
      } else {
        this.map.setLayoutProperty(route.value + '-routes', 'visibility', 'none')
      }
    }
  }

}
</script>

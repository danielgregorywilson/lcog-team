<template>
  <q-layout view="lHh Lpr lFf">
    <q-page-container>
      <q-page class="q-mx-lg" id="page">
        <p id="page-title" class="text-h4 q-my-lg text-center">Meals on Wheels Delivery Routes</p>
        <div class="row justify-around">
          <div class="q-mr-lg" id="map-controls">
            <div class="q-pa-md row">
              <div class="col">
                <q-checkbox v-model="allHot" label="All Hot" @input="toggleAllHot" class="all-toggle"></q-checkbox>
                <q-option-group
                  :options="hotRouteOptions"
                  type="checkbox"
                  v-model="selectedHotRoutes"
                  @input="updateMapVisibility"
                />
              </div>
              <div class="col">
                <q-checkbox v-model="allCold" label="All Cold" @input="toggleAllCold" class="all-toggle"></q-checkbox>
                <q-option-group
                  :options="coldRouteOptions"
                  type="checkbox"
                  v-model="selectedColdRoutes"
                  @input="updateMapVisibility"
                />
              </div>
            </div>
            <q-toggle v-model="showWaitlisted" label="Show Waitlisted" class="row" @input="updateMapVisibility" />
            <q-btn color="primary" label="Print selected" class="row q-mt-md" @click="printPage"/>
          </div>
          <div id="map"></div>
        </div>
        <div id="add-address-container">
          <q-input v-model="newAddress" label="Add a Delivery Address">
            <template v-slot:prepend>
              <q-icon name="place" />
            </template>
            <template v-slot:append>
              <q-icon name="close" @click="newAddress = ''" class="cursor-pointer" />
            </template>
          </q-input>
        </div>
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

  .all-toggle {
    border-bottom: 1px solid black;
  }

  @media print {
    @page { size: landscape; }

    #page-title {
      margin-top: 10px;
    }

    #map-controls {
      display: none;
    }

    .mapboxgl-control-container {
      display: none;
    }

    #add-address-container {
      display: none;
    }
  }


</style>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import mapboxgl from "mapbox-gl";
import { VuexStoreGetters } from '../store/types'

type RouteLabel = 'Gateway' | 'Marcola' | 'MC' | 'Short' | 'Long' | 'North' | 'Will' | 'Tu1' | 'Tu2' | 'Tu3' | 'Thur1' | 'Thur2' | 'Thur3' | 'PU'
type RouteValue = 'Gateway' | 'Marcola' | 'MC' | 'Short' | 'Long' | 'North' | 'Will' | 'hotPU' | 'Tu1' | 'Tu2' | 'Tu3' | 'Thur1' | 'Thur2' | 'Thur3' | 'coldPU'
type RouteColor = 'red' | 'orange' | 'yellow' | 'green' | 'blue' | 'indigo' | 'violet' | 'pink'
type RouteGetter = 
  'mealsModule/gatewayStops' | 'mealsModule/marcolaStops' | 'mealsModule/MCStops' | 'mealsModule/shortStops' | 'mealsModule/longStops' |
  'mealsModule/northStops' | 'mealsModule/willStops' | 'mealsModule/hotPUStops' | 'mealsModule/tu1Stops' | 'mealsModule/tu2Stops' |
  'mealsModule/tu3Stops' | 'mealsModule/thur1Stops' | 'mealsModule/thur2Stops' | 'mealsModule/thur3Stops' | 'mealsModule/coldPUStops'
type WaitlistRouteGetter =
  'mealsModule/gatewayWaitlistStops' | 'mealsModule/marcolaWaitlistStops' | 'mealsModule/MCWaitlistStops' | 'mealsModule/shortWaitlistStops' |
  'mealsModule/longWaitlistStops' | 'mealsModule/northWaitlistStops' | 'mealsModule/willWaitlistStops' | 'mealsModule/hotPUWaitlistStops' |
  'mealsModule/tu1WaitlistStops' | 'mealsModule/tu2WaitlistStops' | 'mealsModule/tu3WaitlistStops' | 'mealsModule/thur1WaitlistStops' |
  'mealsModule/thur2WaitlistStops' | 'mealsModule/thur3WaitlistStops' | 'mealsModule/coldPUWaitlistStops'

interface RouteOption {
  label: RouteLabel,
  value: RouteValue,
  color: RouteColor,
  getter: RouteGetter
  waitlistGetter: WaitlistRouteGetter
}

@Component
export default class MOWMap extends Vue{
  private getters = this.$store.getters as VuexStoreGetters
  public allHot = false
  public allCold = false

  public hotRouteOptions: Array<RouteOption> = [
    { label: 'Gateway', value: 'Gateway', color: 'red', getter: 'mealsModule/gatewayStops', waitlistGetter: 'mealsModule/gatewayWaitlistStops'},
    { label: 'Marcola', value: 'Marcola', color: 'orange', getter: 'mealsModule/marcolaStops', waitlistGetter: 'mealsModule/marcolaWaitlistStops'},
    { label: 'MC', value: 'MC', color: 'yellow', getter: 'mealsModule/MCStops', waitlistGetter: 'mealsModule/MCWaitlistStops'},
    { label: 'Short', value: 'Short', color: 'green', getter: 'mealsModule/shortStops', waitlistGetter: 'mealsModule/shortWaitlistStops'},
    { label: 'Long', value: 'Long', color: 'blue', getter: 'mealsModule/longStops', waitlistGetter: 'mealsModule/longWaitlistStops'},
    { label: 'North', value: 'North', color: 'indigo', getter: 'mealsModule/northStops', waitlistGetter: 'mealsModule/northWaitlistStops'},
    { label: 'Will', value: 'Will', color: 'violet', getter: 'mealsModule/willStops', waitlistGetter: 'mealsModule/willWaitlistStops'},
    { label: 'PU', value: 'hotPU', color: 'pink', getter: 'mealsModule/hotPUStops', waitlistGetter: 'mealsModule/hotPUWaitlistStops'}
  ]
  public coldRouteOptions: Array<RouteOption> = [
    { label: 'Tu1', value: 'Tu1', color: 'red', getter: 'mealsModule/tu1Stops', waitlistGetter: 'mealsModule/tu1WaitlistStops'},
    { label: 'Tu2', value: 'Tu2', color: 'orange', getter: 'mealsModule/tu2Stops', waitlistGetter: 'mealsModule/tu2WaitlistStops'},
    { label: 'Tu3', value: 'Tu3', color: 'yellow', getter: 'mealsModule/tu3Stops', waitlistGetter: 'mealsModule/tu3WaitlistStops'},
    { label: 'Thur1', value: 'Thur1', color: 'green', getter: 'mealsModule/thur1Stops', waitlistGetter: 'mealsModule/thur1WaitlistStops'},
    { label: 'Thur2', value: 'Thur2', color: 'blue', getter: 'mealsModule/thur2Stops', waitlistGetter: 'mealsModule/thur2WaitlistStops'},
    { label: 'Thur3', value: 'Thur3', color: 'violet', getter: 'mealsModule/thur3Stops', waitlistGetter: 'mealsModule/thur3WaitlistStops'},
    { label: 'PU', value: 'coldPU', color: 'pink', getter: 'mealsModule/coldPUStops', waitlistGetter: 'mealsModule/coldPUWaitlistStops'}
  ]
  private allRouteOptions = [...this.hotRouteOptions, ...this.coldRouteOptions]
  private allHotRoutes: Array<RouteValue> = ['Gateway', 'Marcola', 'MC', 'Short', 'Long', 'North', 'Will', 'hotPU']
  private allColdRoutes: Array<RouteValue> = ['Tu1', 'Tu2', 'Tu3', 'Thur1', 'Thur2', 'Thur3', 'coldPU']
  public selectedHotRoutes: Array<RouteValue> = ['Gateway', 'Marcola', 'MC', 'Short', 'Long', 'North', 'Will']
  public selectedColdRoutes: Array<RouteValue> = []
  public newAddress = ''
  public showWaitlisted = false

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
        for(let route of this.allRouteOptions) {
          for (let waitlistOption of ['current', 'waitlisted']) {
            // Get the stops for the route.
            let stops
            let sourceInfix = ''
            if (waitlistOption == 'current') {
              stops = this.getters[route.getter]
            } else {
              stops = this.getters[route.waitlistGetter]
              sourceInfix = 'Waitlist'
            }

            // Create an array of addresses for the route.
            let addresses = []
            for (let address of stops) {
              addresses.push({
                'type': 'Feature',
                'geometry': {
                  'type': 'Point',
                  'coordinates': [address.longitude, address.latitude]
                }
              })
            }

            // Add the addresses as a map source.
            this.map.addSource(route.value + sourceInfix + 'Routes', {
              'type': 'geojson',
              'data': {
                'type': 'FeatureCollection',
                'features': addresses
              }
            });
            
            // Add the addresses as a layer on the map.
            this.map.addLayer({
              'id': route.value + sourceInfix.toLowerCase() + '-routes',
              'type': 'circle',
              'source': route.value + sourceInfix + 'Routes',
              'paint': {
                'circle-radius': 6,
                'circle-color': route.color
              },
              'filter': ['==', '$type', 'Point']
            });
          }
        }
        this.updateMapVisibility()
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

  toggleAllHot() {
    if (this.allHot) {
      this.selectedHotRoutes = ['Gateway', 'Marcola', 'MC', 'Short', 'Long', 'North', 'Will', 'hotPU']
    } else {
      this.selectedHotRoutes = []
    }
    this.updateMapVisibility()
  }

  toggleAllCold() {
    if (this.allCold) {
      this.selectedColdRoutes = ['Tu1', 'Tu2', 'Tu3', 'Thur1', 'Thur2', 'Thur3', 'coldPU']
    } else {
      this.selectedColdRoutes = []
    }
    this.updateMapVisibility()
  }

  updateMapVisibility() {
    // Set route visibility and trigger the map to fit.
    for (let route of this.allRouteOptions) {
      for (let waitlistOption of ['current', 'waitlisted']) {
        // Returns true if the waitlist option for this route matches the currently selected show waitlisted option.
        const waitlistOptionMatchesShowWaitlisted = (waitlistOption == 'waitlisted') == this.showWaitlisted
        let sourceInfix = ''
        if (waitlistOption == 'waitlisted') {
          sourceInfix = 'waitlist'
        }
        if ([...this.selectedHotRoutes, ...this.selectedColdRoutes].includes(route.value) && waitlistOptionMatchesShowWaitlisted) {
          this.map.setLayoutProperty(route.value + sourceInfix + '-routes', 'visibility', 'visible')
        } else {
          this.map.setLayoutProperty(route.value + sourceInfix + '-routes', 'visibility', 'none')
        }
        this.allHot = this.selectedHotRoutes.length == this.allHotRoutes.length
        this.allCold = this.selectedColdRoutes.length == this.allColdRoutes.length
      }
    }
    this.fitMapToStops()
  }

  fitMapToStops() {
    // Fit the map to the bounds of the selected routes.
    const bounds = new mapboxgl.LngLatBounds()
    for (let route of this.allRouteOptions) {
      for (let waitlistOption of ['current', 'waitlisted']) {
        // Returns true if the waitlist option for this route matches the currently selected show waitlisted option.
        const waitlistOptionMatchesShowWaitlisted = (waitlistOption == 'waitlisted') == this.showWaitlisted
        if ([...this.selectedHotRoutes, ...this.selectedColdRoutes].includes(route.value) && waitlistOptionMatchesShowWaitlisted) {
          let stops
          if (waitlistOption == 'current') {
            stops = this.getters[route.getter]
          } else {
            stops = this.getters[route.waitlistGetter]
          }
          for (let stop of stops) {
            bounds.extend([stop.longitude, stop.latitude])
          }
        }
      }
    }
    this.map.fitBounds(bounds, {padding: 50})
  }

  printPage() {
    window.print()
  }

}
</script>

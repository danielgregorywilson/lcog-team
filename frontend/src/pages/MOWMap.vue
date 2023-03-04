<template>
  <q-layout view="lHh Lpr lFf">
    <q-page-container>
      <q-page class="q-mx-lg" id="page">
        <div id="page-title" class="text-h4 q-my-lg text-center">Meals on Wheels Delivery Routes</div>
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
          <div class="text-h6">Add a Stop</div>
          <div class="row q-gutter-md">
            <q-input v-model="newStopAddress" label="Address" class="col" id="new-stop-address">
              <template v-slot:prepend>
                <q-icon name="place" />
              </template>
            </q-input>
            <q-select v-model="newStopCity" :options="newStopCityOptions" label="City" id="new-stop-city" />
            <q-select v-model="newStopState" :options="newStopStateOptions" label="State" id="new-stop-state" />
            <q-input v-model="newStopZip" mask="#####" label="Zip" class="col" id="new-stop-zip" />
          </div>
          <q-btn color="primary" label="Check Address" class="q-mt-sm" @click="checkAddress" />
          {{ newStopLatitude }}, {{ newStopLongitude }}, {{ newStopRoute }}
        </div>
        <div id="route-stats" class="row q-gutter-md">
          <div v-for="route in allRoutes" :key="allRoutes.indexOf(route)">
            <div class="text-h6">{{ route }}</div>
            <div>Current: {{ routeStats[route].current }}</div>
            <div>Waitlisted: {{ routeStats[route].waitlisted }}</div>
            <div>Center: {{ routeStats[route].center }}</div>
            <div>Average Distance: {{ routeStats[route].averageDistance }}</div>
            <div>Max Distance: {{ routeStats[route].maxDistance }}</div>
          </div>
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

  // New Stop Form
  #new-stop-state {
    min-width: 29px;
  }

  .star-marker {
    background-image: url('../assets/star.png');
    background-size: cover;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    cursor: pointer;
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
import { Stop, VuexStoreGetters } from '../store/types'

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
  public allRoutes = [...this.allHotRoutes, ...this.allColdRoutes]
  public selectedHotRoutes: Array<RouteValue> = ['Gateway', 'Marcola', 'MC', 'Short', 'Long', 'North', 'Will']
  public selectedColdRoutes: Array<RouteValue> = []
  public newStopAddress = ''
  public newStopCity = 'Springfield'
  public newStopState = 'OR'
  public newStopZip = ''
  public newStopLatitude = -1
  public newStopLongitude = -1
  public newStopCityOptions = ['Dexter', 'Eugene', 'Leaburg', 'Lowell', 'Marcola', 'Springfield']
  public newStopStateOptions = ['OR']
  public newStopRoute = ''
  public showWaitlisted = false

  public routeStats = {
    'Gateway': {current: 0, waitlisted: 0, center: [0, 0], averageDistance: 0, maxDistance: 0},
    'Marcola': {current: 0, waitlisted: 0, center: [0, 0], averageDistance: 0, maxDistance: 0},
    'MC': {current: 0, waitlisted: 0, center: [0, 0], averageDistance: 0, maxDistance: 0},
    'Short': {current: 0, waitlisted: 0, center: [0, 0], averageDistance: 0, maxDistance: 0},
    'Long': {current: 0, waitlisted: 0, center: [0, 0], averageDistance: 0, maxDistance: 0},
    'North': {current: 0, waitlisted: 0, center: [0, 0], averageDistance: 0, maxDistance: 0},
    'Will': {current: 0, waitlisted: 0, center: [0, 0], averageDistance: 0, maxDistance: 0},
    'hotPU': {current: 0, waitlisted: 0, center: [0, 0], averageDistance: 0, maxDistance: 0},
    'Tu1': {current: 0, waitlisted: 0, center: [0, 0], averageDistance: 0, maxDistance: 0},
    'Tu2': {current: 0, waitlisted: 0, center: [0, 0], averageDistance: 0, maxDistance: 0},
    'Tu3': {current: 0, waitlisted: 0, center: [0, 0], averageDistance: 0, maxDistance: 0},
    'Thur1': {current: 0, waitlisted: 0, center: [0, 0], averageDistance: 0, maxDistance: 0},
    'Thur2': {current: 0, waitlisted: 0, center: [0, 0], averageDistance: 0, maxDistance: 0},
    'Thur3': {current: 0, waitlisted: 0, center: [0, 0], averageDistance: 0, maxDistance: 0},
    'coldPU': {current: 0, waitlisted: 0, center: [0, 0], averageDistance: 0, maxDistance: 0}
  }

  // Mapbox
  private accessToken = process.env.VUE_APP_MAP_ACCESS_TOKEN
  private map: mapboxgl.Map = {} as mapboxgl.Map
  private center = [-122.94329319107005, 44.08711374902461]
  private zoom = 10

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
            this.compileRouteAndAddToMap(route, waitlistOption)
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

  private compileRouteAndAddToMap(
    route: RouteOption,
    waitlistOption: 'current' | 'waitlisted',
    newStop?: Stop
  ) {
    // Get the stops for the route.
    let stops
    let routeNameInfix = ''
    if (waitlistOption == 'current') {
      stops = this.getters[route.getter]
    } else {
      stops = this.getters[route.waitlistGetter]
      routeNameInfix = 'Waitlist'
    }

    // TODO: Don't do this. Submit new stop and re-fetch
    if (newStop) {
      // Add the new stop to the stops array so that the map will resize to include it.
      stops.push(newStop)

      this.addPulsingDotToMap(newStop, route)
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
    this.map.addSource(route.value + routeNameInfix + 'Routes', {
      'type': 'geojson',
      'data': {
        'type': 'FeatureCollection',
        'features': addresses
      }
    });
    
    // Add the addresses as a layer on the map.
    this.map.addLayer({
      'id': route.value + routeNameInfix + 'Routes',
      'type': 'circle',
      'source': route.value + routeNameInfix + 'Routes',
      'paint': {
        'circle-radius': 6,
        'circle-color': route.color
      },
      'filter': ['==', '$type', 'Point']
    });
  }

  private calculateRouteStats() {
    for (let route of this.allRouteOptions) {
      // Calculate the number of stops on the route.
      let waitlistedStops = this.getters[route.waitlistGetter]
      this.routeStats[route.value].waitlisted = waitlistedStops.length
      let stops = this.getters[route.getter]
      this.routeStats[route.value].current = stops.length
       
      // Calculate the center of the route.
      let center = [0, 0]
      for (let stop of stops) {
        center[0] += stop.longitude
        center[1] += stop.latitude
      }
      center[0] /= stops.length
      center[1] /= stops.length

      // Calculate the average distance from the center.
      let averageDistance = 0
      for (let stop of stops) {
        averageDistance += this.calculateDistance(stop.latitude, stop.longitude, center[1], center[0])
      }
      averageDistance /= stops.length

      // Calculate the maximum distance from the center.
      let maxDistance = 0
      for (let stop of stops) {
        let distance = this.calculateDistance(stop.latitude, stop.longitude, center[1], center[0])
        if (distance > maxDistance) {
          maxDistance = distance
        }
      }

      // Store the stats for the route.
      this.routeStats[route.value].center = center
      this.routeStats[route.value].averageDistance = averageDistance
      this.routeStats[route.value].maxDistance = maxDistance
    }
  }

  private calculateDistance(lat1: number, lon1: number, lat2: number, lon2: number) {
    // Haversine formula
    const R = 6371e3; // metres
    const φ1 = lat1 * Math.PI/180; // φ, λ in radians
    const φ2 = lat2 * Math.PI/180;
    const Δφ = (lat2-lat1) * Math.PI/180;
    const Δλ = (lon2-lon1) * Math.PI/180;

    const a = Math.sin(Δφ/2) * Math.sin(Δφ/2) +
              Math.cos(φ1) * Math.cos(φ2) *
              Math.sin(Δλ/2) * Math.sin(Δλ/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));

    const d = R * c; // in metres
    return d
  }

  public toggleAllHot() {
    if (this.allHot) {
      this.selectedHotRoutes = ['Gateway', 'Marcola', 'MC', 'Short', 'Long', 'North', 'Will', 'hotPU']
    } else {
      this.selectedHotRoutes = []
    }
    this.updateMapVisibility()
  }

  public toggleAllCold() {
    if (this.allCold) {
      this.selectedColdRoutes = ['Tu1', 'Tu2', 'Tu3', 'Thur1', 'Thur2', 'Thur3', 'coldPU']
    } else {
      this.selectedColdRoutes = []
    }
    this.updateMapVisibility()
  }

  private updateMapVisibility() {
    // Set route visibility and trigger the map to fit.
    for (let route of this.allRouteOptions) {
      for (let waitlistOption of ['current', 'waitlisted']) {
        // Returns true if the waitlist option for this route matches the currently selected show waitlisted option.
        const waitlistOptionMatchesShowWaitlisted = (waitlistOption == 'waitlisted') == this.showWaitlisted
        let sourceInfix = ''
        if (waitlistOption == 'waitlisted') {
          sourceInfix = 'Waitlist'
        }
        if ([...this.selectedHotRoutes, ...this.selectedColdRoutes].includes(route.value) && waitlistOptionMatchesShowWaitlisted) {
          this.map.setLayoutProperty(route.value + sourceInfix + 'Routes', 'visibility', 'visible')
        } else {
          this.map.setLayoutProperty(route.value + sourceInfix + 'Routes', 'visibility', 'none')
        }
        this.allHot = this.selectedHotRoutes.length == this.allHotRoutes.length
        this.allCold = this.selectedColdRoutes.length == this.allColdRoutes.length
      }
    }
    this.fitMapToStops()
  }

  private fitMapToStops() {
    // Fit the map to the bounds of the selected routes.
    const bounds = new mapboxgl.LngLatBounds()
    if (this.selectedColdRoutes.length == 0 && this.selectedHotRoutes.length == 0) {
      // If no routes are selected, don't resize
      return
    }
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

  public printPage() {
    window.print()
  }

  public checkAddress() {
    this.$store.dispatch(
      'mealsModule/getAddressLatLong', {
        address: this.newStopAddress, city: this.newStopCity,
        state: this.newStopState, zip: this.newStopZip
      }
    )
      .then((response) => {
        this.newStopLatitude = response.data.lat
        this.newStopLongitude = response.data.long
        this.chooseStopRoute()
      })
  }

  private chooseStopRoute() {
    // TODO: Super simple. Consider things like the number of stops on a route and the distance from the center relative to other stops on the route.
    // Find the route with the center with the shortest distance from the new stop.
    let shortestDistance
    let shortestDistanceRoute
    for (let route of this.allRouteOptions) {
      let distance = this.calculateDistance(this.newStopLatitude, this.newStopLongitude, this.routeStats[route.value].center[1], this.routeStats[route.value].center[0])
      if (shortestDistance == undefined || distance < shortestDistance) {
        shortestDistance = distance
        shortestDistanceRoute = route
      }
    }
    if (shortestDistanceRoute) {
      this.newStopRoute = shortestDistanceRoute?.value
      this.addNewStopToMap()
      this.calculateRouteStats()
      this.fitMapToStops()
    }
  }

  private addNewStopToMap() {
    // Add the new stop to the route
   
    // const route = this.allRouteOptions.find(route => route.value == this.newStopRoute)
    const route = this.allRouteOptions.find(route => route.value == this.newStopRoute)
    if (!route) {
      return
    }
    
    // Remove the old route.
    const routeName = this.newStopRoute + 'Routes'
    this.map.removeLayer(routeName)
    this.map.removeSource(routeName)
   
    // Add the new stop to the route.
    const newStop = {
      first_name: this.newStopFirstName, last_name: this.newStopLastName, address: this.newStopAddress,
      city: this.newStopCity, zip: this.newStopZip, latitude: this.newStopLatitude, longitude: this.newStopLongitude,
      meal_type: this.newStopMealType, waitlist: this.newStopWaitlist, phone: this.newStopPhone,
      phoneNotes: this.newPhoneNotes, notes: this.newStopNotes, route: this.newStopRoute, new: true
    }
    this.compileRouteAndAddToMap(route, 'current', newStop)
  }

  addPulsingDotToMap(newStop: Stop, route: RouteOption) {
    const geojson = {
      type: 'FeatureCollection',
      features: [
        {
          type: 'Feature',
          geometry: {
            type: 'Point',
            coordinates: [newStop.longitude, newStop.latitude]
          },
          properties: {
            title: 'Mapbox',
            description: 'Washington, D.C.'
          }
        }
      ]
    };
    // Add marker to map with an HTML element.
    const el = document.createElement('div');
    el.className = 'star-marker';
    el.style.backgroundColor = route.color;
    new mapboxgl.Marker(el).setLngLat(geojson.features[0].geometry.coordinates).addTo(this.map);
  }

  mounted() {
    this.getMealStops()
      .then(() => {
        this.createMap()
        this.calculateRouteStats()
      })
  }

}
</script>

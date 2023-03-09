<template>
  <q-layout view="lHh Lpr lFf">
    <q-page-container>
      <q-page class="q-mx-lg" id="page">
        <div id="page-title" class="text-h4 q-my-lg text-center">Meals on Wheels Delivery Routes</div>
        <div class="row justify-around">
          <div class="q-mr-lg" id="map-controls">
            <div class="q-pa-md row">
              <div class="col">
                <q-checkbox v-model="allHot" label="All Hot" @update:model-value="toggleAllHot" class="all-toggle"></q-checkbox>
                <q-option-group
                  :options="hotRouteOptions"
                  type="checkbox"
                  v-model="selectedHotRoutes"
                  @update:model-value="updateMapVisibility"
                />
              </div>
              <div class="col">
                <q-checkbox v-model="allCold" label="All Cold" @update:model-value="toggleAllCold" class="all-toggle"></q-checkbox>
                <q-option-group
                  :options="coldRouteOptions"
                  type="checkbox"
                  v-model="selectedColdRoutes"
                  @update:model-value="updateMapVisibility"
                />
              </div>
            </div>
            <q-toggle v-model="showWaitlisted" label="Show Waitlisted" class="row" @update:model-value="updateMapVisibility" />
            <q-btn color="primary" label="Print selected" class="row q-mt-md" @click="printPage"/>
          </div>
          <div id="map"></div>
        </div>
        <div id="add-address-container" class="q-mt-md" v-if="canManageMOWStops()">
          <div class="text-h6 row items-center q-my-sm">
            <div class="q-mr-sm">Add a Stop</div>
            <q-btn round color="primary" :icon="showNewStopForm ? 'remove' : 'add'" @click="showNewStopForm = !showNewStopForm"/>
          </div>
          <div id="addStopForm" v-if="showNewStopForm">
            <div class="row q-gutter-md">
              <q-input v-model="newStopFirstName" label="First Name" id="new-stop-first-name" />
              <q-input v-model="newStopLastName" label="Last Name" id="new-stop-last-name" />
              <q-input v-model="newStopPhone" label="Phone" id="new-stop-phone" />
              <q-input v-model="newStopPhoneNotes" label="Phone Notes" id="new-stop-phone-notes" class="col" />
            </div>
            <div class="row q-gutter-md">
              <q-input v-model="newStopAddress" name="street-address" label="Address" class="col" id="new-stop-address">
                <template v-slot:prepend>
                  <q-icon name="place" />
                </template>
              </q-input>
              <q-select v-model="newStopCity" :options="newStopCityOptions" label="City" name="city" id="new-stop-city" />
              <q-select v-model="newStopState" :options="newStopStateOptions" label="State" id="new-stop-state" />
              <q-input v-model="newStopZip" mask="#####" name="postal-code" label="Zip" class="col" id="new-stop-zip" />
            </div>
            <div class="row q-gutter-md">
              <q-select v-model="newStopMealType" label="Meal Type" :options="newStopMealTypeOptions" id="new-stop-meal-type" />
              <!-- <q-checkbox v-model="newStopWaitlist" label="Waitlist" id="new-stop-waitlist" /> -->
              <q-input v-model="newStopNotes" label="Notes" id="new-stop-notes" class="col" />
            </div>
            <div class="row q-gutter-md items-center" v-if="showNewStopRoute">
              <q-select
                v-model="newStopRoute"
                label="Route"
                :options="newStopMealType == 'Hot' ? allHotRoutes : allColdRoutes"
                id="new-stop-route"
                @update:model-value="addNewStopToMap"
              />
              <q-checkbox v-model="newStopWaitlist" label="Waitlist" id="new-stop-waitlist" />
              <q-btn color="primary" label="Add Stop" class="q-mt-sm" :disabled="!showNewStopRoute" @click="addStopToRoute" />
            </div>
            <div class="row">
              <q-btn color="primary" label="Check Address" class="q-mt-sm" :disabled="!newStopAddress || !newStopZip || showNewStopRoute" @click="checkAddress" />
            </div>
          </div>
        </div>
        <div id="route-stats" style="display: none">
          <div>{{ newStopLatitude }}, {{ newStopLongitude }}, {{ newStopRoute }}</div>
          <div class="row q-gutter-md">
            <div v-for="route in allRoutes" :key="allRoutes.indexOf(route)">
              <div class="text-h6">{{ route }}</div>
              <div>Current: {{ routeStats[route].current }}</div>
              <div>Waitlisted: {{ routeStats[route].waitlisted }}</div>
              <div>Center: {{ routeStats[route].center }}</div>
              <div>Average Distance: {{ routeStats[route].averageDistance }}</div>
              <div>Max Distance: {{ routeStats[route].maxDistance }}</div>
            </div>
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
  #addStopForm {
    background-color: lightgray;
    padding: 10px 30px 30px 30px
  }

  #new-stop-state {
    min-width: 29px;
  }

  #new-stop-meal-type {
    min-width: 56px;
  }

  #new-stop-route {
    min-width: 56px;
  }

  .star-marker {
    background-image: url('../../assets/star.png');
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

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { Ref } from 'vue'
import { Feature, GeoJsonProperties, Geometry } from 'GeoJSON'
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import { useMealsStore } from '../../stores/meals'
import { Stop } from '../../types'

type RouteLabel = 'Gateway' | 'Marcola' | 'MC' | 'Short' | 'Long' | 'North' | 'Will' | 'Tu 1' | 'Tu 2' | 'Tu 3' | 'Thur 1' | 'Thur 2' | 'Thur 3' | 'PU'
type RouteValue = 'Gateway' | 'Marcola' | 'MC' | 'Short' | 'Long' | 'North' | 'Will' | 'hotPU' | 'Tu 1' | 'Tu 2' | 'Tu 3' | 'Thur 1' | 'Thur 2' | 'Thur 3' | 'coldPU'
type RouteColor = 'red' | 'orange' | 'yellow' | 'green' | 'blue' | 'indigo' | 'violet' | 'pink'
type RouteGetter = 
  'gatewayStops' | 'marcolaStops' | 'MCStops' | 'shortStops' | 'longStops' |
  'northStops' | 'willStops' | 'hotPUStops' | 'tu1Stops' | 'tu2Stops' |
  'tu3Stops' | 'thur1Stops' | 'thur2Stops' | 'thur3Stops' | 'coldPUStops'
type WaitlistRouteGetter =
  'gatewayWaitlistStops' | 'marcolaWaitlistStops' | 'MCWaitlistStops' | 'shortWaitlistStops' |
  'longWaitlistStops' | 'northWaitlistStops' | 'willWaitlistStops' | 'hotPUWaitlistStops' |
  'tu1WaitlistStops' | 'tu2WaitlistStops' | 'tu3WaitlistStops' | 'thur1WaitlistStops' |
  'thur2WaitlistStops' | 'thur3WaitlistStops' | 'coldPUWaitlistStops'

interface RouteOption {
  label: RouteLabel,
  value: RouteValue,
  color: RouteColor,
  getter: RouteGetter
  waitlistGetter: WaitlistRouteGetter
}

interface RouteStats {
  current: number,
  waitlisted: number,
  center: {lng: number, lat: number},
  averageDistance: number,
  maxDistance: number
}

interface RoutesStats {
  [key: string]: RouteStats
}

type WaitlistOption = 'current' | 'waitlisted'

const store = useMealsStore()

let allHot = ref(false)
let allCold = ref(false)

const waitlistOptions: Array<WaitlistOption> = ['current', 'waitlisted']

const hotRouteOptions: Array<RouteOption> = [
  { label: 'Gateway', value: 'Gateway', color: 'red', getter: 'gatewayStops', waitlistGetter: 'gatewayWaitlistStops'},
  { label: 'Marcola', value: 'Marcola', color: 'orange', getter: 'marcolaStops', waitlistGetter: 'marcolaWaitlistStops'},
  { label: 'MC', value: 'MC', color: 'yellow', getter: 'MCStops', waitlistGetter: 'MCWaitlistStops'},
  { label: 'Short', value: 'Short', color: 'green', getter: 'shortStops', waitlistGetter: 'shortWaitlistStops'},
  { label: 'Long', value: 'Long', color: 'blue', getter: 'longStops', waitlistGetter: 'longWaitlistStops'},
  { label: 'North', value: 'North', color: 'indigo', getter: 'northStops', waitlistGetter: 'northWaitlistStops'},
  { label: 'Will', value: 'Will', color: 'violet', getter: 'willStops', waitlistGetter: 'willWaitlistStops'},
  { label: 'PU', value: 'hotPU', color: 'pink', getter: 'hotPUStops', waitlistGetter: 'hotPUWaitlistStops'}
]
const coldRouteOptions: Array<RouteOption> = [
  { label: 'Tu 1', value: 'Tu 1', color: 'red', getter: 'tu1Stops', waitlistGetter: 'tu1WaitlistStops'},
  { label: 'Tu 2', value: 'Tu 2', color: 'orange', getter: 'tu2Stops', waitlistGetter: 'tu2WaitlistStops'},
  { label: 'Tu 3', value: 'Tu 3', color: 'yellow', getter: 'tu3Stops', waitlistGetter: 'tu3WaitlistStops'},
  { label: 'Thur 1', value: 'Thur 1', color: 'green', getter: 'thur1Stops', waitlistGetter: 'thur1WaitlistStops'},
  { label: 'Thur 2', value: 'Thur 2', color: 'blue', getter: 'thur2Stops', waitlistGetter: 'thur2WaitlistStops'},
  { label: 'Thur 3', value: 'Thur 3', color: 'violet', getter: 'thur3Stops', waitlistGetter: 'thur3WaitlistStops'},
  { label: 'PU', value: 'coldPU', color: 'pink', getter: 'coldPUStops', waitlistGetter: 'coldPUWaitlistStops'}
]
const allRouteOptions = [...hotRouteOptions, ...coldRouteOptions]
const allHotRoutes: Array<RouteValue> = ['Gateway', 'Marcola', 'MC', 'Short', 'Long', 'North', 'Will', 'hotPU']
const allColdRoutes: Array<RouteValue> = ['Tu 1', 'Tu 2', 'Tu 3', 'Thur 1', 'Thur 2', 'Thur 3', 'coldPU']
const allRoutes = [...allHotRoutes, ...allColdRoutes]
let selectedHotRoutes: Ref<Array<string>> = ref(['Gateway', 'Marcola', 'MC', 'Short', 'Long', 'North', 'Will']) // TODO: Use Array<RouteValue> instead of Array<string>
let selectedColdRoutes: Ref<Array<string>> = ref([])
let showWaitlisted = ref(false)

const newStopCityOptions = ['Dexter', 'Eugene', 'Leaburg', 'Lowell', 'Marcola', 'Springfield']
const newStopStateOptions = ['OR']
const newStopMealTypeOptions = [{label: 'Hot', value: 'hot'}, {label: 'Cold', value: 'cold'}]
let showNewStopForm = ref(false)
let showNewStopRoute = ref(false)
let newStopFirstName = ref('')
let newStopLastName = ref('')
let newStopAddress = ref('')
let newStopCity = ref('Springfield')
let newStopState = ref('OR')
let newStopZip = ref('')
let newStopPhone = ref('')
let newStopPhoneNotes = ref('')
let newStopNotes = ref('')
let newStopMealType: Ref<'Hot'> | Ref<'Cold'> = ref('Hot')
let newStopWaitlist = ref(true)
let newStopLongitude = ref(-1)
let newStopLatitude = ref(-1)
let newStopRoute: Ref<RouteValue> = ref('Gateway')

let routeStats: RoutesStats = {
  'Gateway': {current: 0, waitlisted: 0, center: { lng: 0, lat: 0 }, averageDistance: 0, maxDistance: 0},
  'Marcola': {current: 0, waitlisted: 0, center: { lng: 0, lat: 0 }, averageDistance: 0, maxDistance: 0},
  'MC': {current: 0, waitlisted: 0, center: { lng: 0, lat: 0 }, averageDistance: 0, maxDistance: 0},
  'Short': {current: 0, waitlisted: 0, center: { lng: 0, lat: 0 }, averageDistance: 0, maxDistance: 0},
  'Long': {current: 0, waitlisted: 0, center: { lng: 0, lat: 0 }, averageDistance: 0, maxDistance: 0},
  'North': {current: 0, waitlisted: 0, center: { lng: 0, lat: 0 }, averageDistance: 0, maxDistance: 0},
  'Will': {current: 0, waitlisted: 0, center: { lng: 0, lat: 0 }, averageDistance: 0, maxDistance: 0},
  'hotPU': {current: 0, waitlisted: 0, center: { lng: 0, lat: 0 }, averageDistance: 0, maxDistance: 0},
  'Tu 1': {current: 0, waitlisted: 0, center: { lng: 0, lat: 0 }, averageDistance: 0, maxDistance: 0},
  'Tu 2': {current: 0, waitlisted: 0, center: { lng: 0, lat: 0 }, averageDistance: 0, maxDistance: 0},
  'Tu 3': {current: 0, waitlisted: 0, center: { lng: 0, lat: 0 }, averageDistance: 0, maxDistance: 0},
  'Thur 1': {current: 0, waitlisted: 0, center: { lng: 0, lat: 0 }, averageDistance: 0, maxDistance: 0},
  'Thur 2': {current: 0, waitlisted: 0, center: { lng: 0, lat: 0 }, averageDistance: 0, maxDistance: 0},
  'Thur 3': {current: 0, waitlisted: 0, center: { lng: 0, lat: 0 }, averageDistance: 0, maxDistance: 0},
  'coldPU': {current: 0, waitlisted: 0, center: { lng: 0, lat: 0 }, averageDistance: 0, maxDistance: 0}
}

// Mapbox
// console.log(process.env)
// const accessToken = process.env.VUE_APP_MAP_ACCESS_TOKEN
const accessToken = 'pk.eyJ1IjoiZHdpbHNvbjExMjMiLCJhIjoiY2xlZzFhczhiMGRuczNybXFxNjE1Z3BraiJ9.M5nEPBjHW4AS_nCnrr5ZPA'
let map = {} as mapboxgl.Map
let center: mapboxgl.LngLatLike = [-122.94329319107005, 44.08711374902461]
let zoom = 10

function getMealStops() {
  return new Promise((resolve, reject) => {
    store.getMealStops()
      .then(() => {
        resolve('Got meal stops')
      })
      .catch((err) => {
        reject(err)
      })
  })
}

function createMap() {
  try {
    map = new mapboxgl.Map({
      accessToken: accessToken,
      container: 'map',
      style: 'mapbox://styles/mapbox/streets-v11',
      center: center,
      zoom: zoom
    })

    map.addControl(new mapboxgl.NavigationControl());
    map.addControl(new mapboxgl.FullscreenControl());

    map.on('load', () => {
      for(let route of allRouteOptions) {
        for (let waitlistOption of waitlistOptions) {
          compileRouteAndAddToMap(route, waitlistOption)
        }
      }
      updateMapVisibility()
    });

    // When panning the map, update the center coordinates
    map.on('dragend', () => {
      const mapCenter = map.getCenter()
      center = [mapCenter.lng, mapCenter.lat]
    });
    
  } catch (err) {
    console.log('Error rendering map:', err)
  }
}

function compileRouteAndAddToMap(
  route: RouteOption,
  waitlistOption: 'current' | 'waitlisted',
  newStop?: Stop
) {
  // Get the stops for the route.
  let stops
  let routeNameInfix = ''
  if (waitlistOption == 'current') {
    stops = store[route.getter]
  } else {
    stops = store[route.waitlistGetter]
    routeNameInfix = 'Waitlist'
  }

  // TODO: Don't do this. Submit new stop and re-fetch
  if (newStop) {
    // Add the new stop to the stops array so that the map will resize to include it.
    stops.push(newStop)

    addNewStopMarkerToMap(newStop, route)
  }

  // Create an array of addresses for the route.
  // let addresses = []
  let addresses = [] as Feature<Geometry, GeoJsonProperties>[]
  for (let address of stops) {
    addresses.push({
      'type': 'Feature',
      'geometry': {
        'type': 'Point',
        'coordinates': [address.longitude, address.latitude]
      },
      'properties': {}
    })
  }

  // Add the addresses as a map source.
  map.addSource(route.value + routeNameInfix + 'Routes', {
    'type': 'geojson',
    'data': {
      'type': 'FeatureCollection',
      'features': addresses,
    }
  });
  
  // Add the addresses as a layer on the map.
  map.addLayer({
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

function calculateRouteStats() {
  for (let route of allRouteOptions) {
    // Calculate the number of stops on the route.
    let waitlistedStops = store[route.waitlistGetter]
    routeStats[route.value].waitlisted = waitlistedStops.length
    let stops = store[route.getter]
    routeStats[route.value].current = stops.length
      
    // Calculate the center of the route.
    let center: mapboxgl.LngLatLike = {lng: 0, lat: 0}
    for (let stop of stops) {
      center.lng += stop.longitude
      center.lat += stop.latitude
    }
    center.lng /= stops.length
    center.lat /= stops.length

    // Calculate the average distance from the center.
    let averageDistance = 0
    for (let stop of stops) {
      averageDistance += calculateDistance(stop.latitude, stop.longitude, center.lat, center.lng)
    }
    averageDistance /= stops.length

    // Calculate the maximum distance from the center.
    let maxDistance = 0
    for (let stop of stops) {
      let distance = calculateDistance(stop.latitude, stop.longitude, center.lat, center.lng)
      if (distance > maxDistance) {
        maxDistance = distance
      }
    }

    // Store the stats for the route.
    routeStats[route.value].center = center
    routeStats[route.value].averageDistance = averageDistance
    routeStats[route.value].maxDistance = maxDistance
  }
}

function calculateDistance(lat1: number, lon1: number, lat2: number, lon2: number) {
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

function toggleAllHot() {
  if (allHot.value) {
    selectedHotRoutes.value = ['Gateway', 'Marcola', 'MC', 'Short', 'Long', 'North', 'Will', 'hotPU']
  } else {
    selectedHotRoutes.value = []
  }
  updateMapVisibility()
}

function toggleAllCold() {
  if (allCold.value) {
    selectedColdRoutes.value = ['Tu 1', 'Tu 2', 'Tu 3', 'Thur 1', 'Thur 2', 'Thur 3', 'coldPU']
  } else {
    selectedColdRoutes.value = []
  }
  updateMapVisibility()
}

function updateMapVisibility() {
  // Set route visibility and trigger the map to fit.
  for (let route of allRouteOptions) {
    for (let waitlistOption of ['current', 'waitlisted']) {
      // Returns true if the waitlist option for this route matches the currently selected show waitlisted option.
      const waitlistOptionMatchesShowWaitlisted = (waitlistOption == 'waitlisted') == showWaitlisted.value
      let sourceInfix = ''
      if (waitlistOption == 'waitlisted') {
        sourceInfix = 'Waitlist'
      }
      if ([...selectedHotRoutes.value, ...selectedColdRoutes.value].includes(route.value) && waitlistOptionMatchesShowWaitlisted) {
        map.setLayoutProperty(route.value + sourceInfix + 'Routes', 'visibility', 'visible')
      } else {
        map.setLayoutProperty(route.value + sourceInfix + 'Routes', 'visibility', 'none')
      }
      allHot.value = selectedHotRoutes.value.length == allHotRoutes.length
      allCold.value = selectedColdRoutes.value.length == allColdRoutes.length
    }
  }
  fitMapToStops()
}

function fitMapToStops() {
  // Fit the map to the bounds of the selected routes.
  const bounds = new mapboxgl.LngLatBounds()
  if (selectedColdRoutes.value.length == 0 && selectedHotRoutes.value.length == 0) {
    // If no routes are selected, don't resize
    return
  }
  for (let route of allRouteOptions) {
    for (let waitlistOption of ['current', 'waitlisted']) {
      // Returns true if the waitlist option for this route matches the currently selected show waitlisted option.
      const waitlistOptionMatchesShowWaitlisted = (waitlistOption == 'waitlisted') == showWaitlisted.value
      if ([...selectedHotRoutes.value, ...selectedColdRoutes.value].includes(route.value) && waitlistOptionMatchesShowWaitlisted) {
        let stops
        if (waitlistOption == 'current') {
          stops = store[route.getter]
        } else {
          stops = store[route.waitlistGetter]
        }
        for (let stop of stops) {
          bounds.extend([stop.longitude, stop.latitude])
        }
      }
    }
  }
  map.fitBounds(bounds, {padding: 50})
}

function printPage() {
  window.print()
}

function canManageMOWStops() {
  return true
  // return this.getters['userModule/canManageMOWStops']
}

function checkAddress() {
  store.getAddressLatLong(newStopAddress.value, newStopCity.value, newStopState.value, newStopZip.value)
    .then((response) => {
      newStopLatitude.value = response.data.lat
      newStopLongitude.value = response.data.long
      chooseStopRoute()
    })
}

function chooseStopRoute() {
  // TODO: Super simple. Consider things like the number of stops on a route and the distance from the center relative to other stops on the route.
  // Find the route with the center with the shortest distance from the new stop. About 18-20 addresses should be on each route
  let shortestDistance
  let shortestDistanceRoute
  const routeOptions = newStopMealType.value == 'Hot' ? hotRouteOptions : coldRouteOptions
  for (let route of routeOptions) {
    let distance = calculateDistance(newStopLatitude.value, newStopLongitude.value, routeStats[route.value].center.lat, routeStats[route.value].center.lng)
    if (shortestDistance == undefined || distance < shortestDistance) {
      shortestDistance = distance
      shortestDistanceRoute = route
    }
  }
  if (shortestDistanceRoute) {
    newStopRoute.value = shortestDistanceRoute.value
    addNewStopToMap()
    calculateRouteStats()
    fitMapToStops()
    showNewStopRoute.value = true
  }
}

function addNewStopToMap() {
  // Add the new stop to the route
  
  // const route = this.allRouteOptions.find(route => route.value == this.newStopRoute)
  const route = allRouteOptions.find(route => route.value == newStopRoute.value)
  if (!route) {
    return
  }

  // If the new route is not currently checked, check it.
  if (!selectedHotRoutes.value.includes(newStopRoute.value) && !selectedColdRoutes.value.includes(newStopRoute.value)) {
    if (allHotRoutes.includes(newStopRoute.value)) {
      selectedHotRoutes.value.push(newStopRoute.value)
    } else {
      selectedColdRoutes.value.push(newStopRoute.value)
    }
    updateMapVisibility()
  }
  
  // Remove the old route.
  const routeName = newStopRoute.value + 'Routes'
  map.removeLayer(routeName)
  map.removeSource(routeName)
  
  // Add the new stop to the route.
  const meal_type_lower = newStopMealType.value.toLowerCase() as 'hot' | 'cold'
  const newStop: Stop = {
    first_name: newStopFirstName.value, last_name: newStopLastName.value, address: newStopAddress.value,
    city: newStopCity.value, zip_code: parseInt(newStopZip.value), latitude: newStopLatitude.value,
    longitude: newStopLongitude.value, meal_type: meal_type_lower, waitlist: newStopWaitlist.value,
    phone: newStopPhone.value, phone_notes: newStopPhoneNotes.value, notes: newStopNotes.value,
    route_name: newStopRoute.value, new: true
  }
  compileRouteAndAddToMap(route, 'current', newStop)
}

function addNewStopMarkerToMap(newStop: Stop, route: RouteOption) {
  const geojson = {
    type: 'FeatureCollection',
    features: [
      {
        type: 'Feature',
        geometry: {
          type: 'Point',
          coordinates: [newStop.longitude, newStop.latitude] as [number, number]
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
  new mapboxgl.Marker(el).setLngLat(geojson.features[0].geometry.coordinates).addTo(map);
}

function addStopToRoute() {
  store.addMealStop({
    first_name: newStopFirstName.value, last_name: newStopLastName.value, address: newStopAddress.value,
    city: newStopCity.value, zip_code: newStopZip.value, meal_type: newStopMealType.value,
    waitlist: newStopWaitlist.value, phone: newStopPhone.value, phone_notes: newStopPhoneNotes.value,
    notes: newStopNotes.value, route_name: newStopRoute.value
  })
    .then(() => {
      initializeComponent()
    })
}

function initializeComponent() {
  showNewStopForm.value = false
  showNewStopRoute.value = false
  newStopFirstName.value = ''
  newStopLastName.value = ''
  newStopAddress.value = ''
  newStopCity.value = 'Springfield'
  newStopState.value = 'OR'
  newStopZip.value = ''
  newStopPhone.value = ''
  newStopPhoneNotes.value = ''
  newStopNotes.value = ''
  newStopMealType.value = 'Hot'
  newStopWaitlist.value = true
  getMealStops()
    .then(() => {
      createMap() // TODO: When redrawing the map, there is a warning about the map already existing.
      calculateRouteStats()
    })
}

function getCurrentUser(): void {
  return //TODO
  if (store.getters['authModule/isAuthenticated'] && !store.getters['userModule/isProfileLoaded']) { // eslint-disable-line @typescript-eslint/no-unsafe-member-access
    store.dispatch('userModule/userRequest')
      .catch(e => {
        console.error('Error getting user from store', e)
      })
  }
}

// lifecycle hooks
onMounted(() => {
  getCurrentUser()
  initializeComponent()
})
</script>


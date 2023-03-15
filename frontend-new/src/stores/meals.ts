import { defineStore } from 'pinia';
import { Stop } from 'src/types';
import axios from 'axios';

// TODO
// const apiURL = process.env.API_URL ? process.env.API_URL : 'https://api.team.lcog.org/'
const apiURL = 'http://localhost:8000/'

export const useMealsStore = defineStore('meals', {
  state: () => ({
    stops: [] as Stop[],
  }),

  getters: {
    // Current Stops
    gatewayStops: (state) => state.stops.filter((stop) => stop.route === 'Gateway' && stop.waitlist === false),
    marcolaStops: (state) => state.stops.filter((stop) => stop.route === 'Marcola' && stop.waitlist === false),
    MCStops: (state) => state.stops.filter((stop) => stop.route === 'MC' && stop.waitlist === false),
    shortStops: (state) => state.stops.filter((stop) => stop.route === 'Short' && stop.waitlist === false),
    longStops: (state) => state.stops.filter((stop) => stop.route === 'Long' && stop.waitlist === false),
    northStops: (state) => state.stops.filter((stop) => stop.route === 'North' && stop.waitlist === false),
    willStops: (state) => state.stops.filter((stop) => stop.route === 'Will' && stop.waitlist === false),
    hotPUStops: (state) => state.stops.filter((stop) => stop.route === 'PU' && stop.meal_type === 'hot' && stop.waitlist === false),
    tu1Stops: (state) => state.stops.filter((stop) => stop.route === 'Tu 1' && stop.waitlist === false),
    tu2Stops: (state) => state.stops.filter((stop) => stop.route === 'Tu 2' && stop.waitlist === false),
    tu3Stops: (state) => state.stops.filter((stop) => stop.route === 'Tu 3' && stop.waitlist === false),
    thur1Stops: (state) => state.stops.filter((stop) => stop.route === 'Thur 1' && stop.waitlist === false),
    thur2Stops: (state) => state.stops.filter((stop) => stop.route === 'Thur 2' && stop.waitlist === false),
    thur3Stops: (state) => state.stops.filter((stop) => stop.route === 'Thur 3' && stop.waitlist === false),
    coldPUStops: (state) => state.stops.filter((stop) => stop.route === 'PU' && stop.meal_type === 'cold' && stop.waitlist === false),
    // Waitlist Stops
    gatewayWaitlistStops: (state) => state.stops.filter((stop) => stop.route === 'Gateway' && stop.waitlist === true),
    marcolaWaitlistStops: (state) => state.stops.filter((stop) => stop.route === 'Marcola' && stop.waitlist === true),
    MCWaitlistStops: (state) => state.stops.filter((stop) => stop.route === 'MC' && stop.waitlist === true),
    shortWaitlistStops: (state) => state.stops.filter((stop) => stop.route === 'Short' && stop.waitlist === true),
    longWaitlistStops: (state) => state.stops.filter((stop) => stop.route === 'Long' && stop.waitlist === true),
    northWaitlistStops: (state) => state.stops.filter((stop) => stop.route === 'North' && stop.waitlist === true),
    willWaitlistStops: (state) => state.stops.filter((stop) => stop.route === 'Will' && stop.waitlist === true),
    hotPUWaitlistStops: (state) => state.stops.filter((stop) => stop.route === 'PU' && stop.meal_type === 'hot' && stop.waitlist === true),
    tu1WaitlistStops: (state) => state.stops.filter((stop) => stop.route === 'Tu 1' && stop.waitlist === true),
    tu2WaitlistStops: (state) => state.stops.filter((stop) => stop.route === 'Tu 2' && stop.waitlist === true),
    tu3WaitlistStops: (state) => state.stops.filter((stop) => stop.route === 'Tu 3' && stop.waitlist === true),
    thur1WaitlistStops: (state) => state.stops.filter((stop) => stop.route === 'Thur 1' && stop.waitlist === true),
    thur2WaitlistStops: (state) => state.stops.filter((stop) => stop.route === 'Thur 2' && stop.waitlist === true),
    thur3WaitlistStops: (state) => state.stops.filter((stop) => stop.route === 'Thur 3' && stop.waitlist === true),
    coldPUWaitlistStops: (state) => state.stops.filter((stop) => stop.route === 'PU' && stop.meal_type === 'cold' && stop.waitlist === true),
  },

  actions: {
    async getMealStops() {
      await axios({ url: `${ apiURL }api/v1/mealstop`, method: 'GET' })
        .then(resp => {
          this.stops = resp.data.results;
        })
        .catch(e => {
          console.error('Error getting meal stops', e)
        });
    },
    getAddressLatLong: (address: string, city: string, state: string, zip: string) => {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/address-lat-long/?address=${ address }&city=${ city }&state=${ state }&zip=${ zip }`, method: 'GET' })
        .then(resp => {
          resolve(resp);
        })
        .catch(e => {
          console.error('Error getting lat/long', e)
          reject(e)
        });
      })
    },
    addMealStop: (data: {
      first_name: string, last_name: string, address: string, city: string,
      zip_code: string, meal_type: string, waitlist: boolean, phone: string,
      phone_notes: string, notes: string, route_name: string
    }) => {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/mealstop`, method: 'POST', data: data })
        .then(resp => {
          resolve(resp);
        })
        .catch(e => {
          console.error('Error adding meal stop', e)
          reject(e)
        });
      })
    },
  }
});

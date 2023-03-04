import { ActionTree } from 'vuex';
import { StateInterface } from '../../index';
import { MealStateInterface } from './state';
import axios from 'axios';

const apiURL = process.env.API_URL ? process.env.API_URL : 'https://api.team.lcog.org/'

const actions: ActionTree<MealStateInterface, StateInterface> = {
  getMealStops: ({ commit }) => {
    return new Promise((resolve, reject) => {
      axios({ url: `${ apiURL }api/v1/mealstop`, method: 'GET' })
      .then(resp => {
        commit('setMealStops', resp);
        resolve(resp);
      })
      .catch(e => {
        console.error('Error getting meal stops', e)
        reject(e)
      });
    })
  },
  getAddressLatLong: ({ commit }, data: {address: string, city: string, state: string, zip: string}) => {
    return new Promise((resolve, reject) => {
      axios({ url: `${ apiURL }api/v1/address-lat-long/?address=${ data.address }&city=${ data.city }&state=${ data.state }&zip=${ data.zip }`, method: 'GET' })
      .then(resp => {
        resolve(resp);
      })
      .catch(e => {
        console.error('Error getting lat/long', e)
        reject(e)
      });
    })
  },
  authLogout: ({commit}) => {
    return new Promise((resolve) => {
      commit('authLogout')
      resolve('Successfully triggered logout')
    })
  }
};

export default actions;

import { ActionTree } from 'vuex'
import { StateInterface } from '../../index'
import { DeskReservationStateInterface } from '../../types'
import axios from 'axios'


function getApiUrl(): string {
  if (process.env.API_URL) {
    return process.env.API_URL
  } else {
    return ''
  }
}

const actions: ActionTree<DeskReservationStateInterface, StateInterface> = {
  getAllDesks: ({ commit }) => {
    return new Promise((resolve, reject) => {
      axios({ url: `${ getApiUrl() }api/v1/desk` })
        .then(resp => {
          commit('setAllDesks', resp)
          resolve(resp)
        })
        .catch(e => {
          console.error('Error getting all desks:', e)
          reject(e)
        })
    })
  },
  getAllDeskReservations: ({ commit }) => {
    return new Promise((resolve, reject) => {
      axios({ url: `${ getApiUrl() }api/v1/deskreservation` })
        .then(resp => {
          commit('setAllDeskReservations', resp)
          resolve(resp)
        })
        .catch(e => {
          console.error('Error getting all desk reservations:', e)
          reject(e)
        })
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

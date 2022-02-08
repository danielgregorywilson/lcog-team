import { Desk, DeskReservation } from 'src/store/types'
import Vue from 'vue'

import { MutationTree } from 'vuex'
import { DeskReservationStateInterface } from '../../types'


const mutation: MutationTree<DeskReservationStateInterface> = {
  setAllDesks: (state, resp: {data: Array<Desk>}) => {
    Vue.set(state, 'allDesks', resp.data)
  },
  setAllDeskReservations: (state, resp: {data: Array<DeskReservation>}) => {
    Vue.set(state, 'allDeskReservations', resp.data)
  },
  authLogout: (state) => {
    // Clean up state
    state.allDesks = { results: [] }
    state.allDeskReservations = { results: [] }
  }
};

export default mutation;

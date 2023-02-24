import Vue from 'vue'

import { MutationTree } from 'vuex'
import { blankStop, MealStateInterface } from './state'
import { Stop } from '../../types'


const mutation: MutationTree<MealStateInterface> = {
  setMeals: (state, resp: {data: Array<Stop>}) => {
    Vue.set(state, 'allWorkflows', resp.data)
  },
  authLogout: (state) => {
    // Clean up state
    state.stops = [blankStop]
  }
};

export default mutation;

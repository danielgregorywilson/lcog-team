import { PerformanceReviewRetrieve, ReviewNoteRetrieve, ViewedSecurityMessageRetrieve } from 'src/store/types'
import Vue from 'vue'

import { MutationTree } from 'vuex'
import { SecurityMessageStateInterface } from './state'


const mutation: MutationTree<SecurityMessageStateInterface> = {
  setViewedSecurityMessages: (state, resp: {data: Array<ViewedSecurityMessageRetrieve>}) => {
    Vue.set(state, 'viewedSecurityMessages', resp.data)
  },
  setViewedLatestSecurityMessage: (state, resp: {data: boolean}) => {
    Vue.set(state, 'viewedLatestSecurityMessage', resp.data)
  },
  authLogout: (state) => {
    // Clean up state
    state.viewedSecurityMessages = []
    state.viewedLatestSecurityMessage = false
  }
};

export default mutation;

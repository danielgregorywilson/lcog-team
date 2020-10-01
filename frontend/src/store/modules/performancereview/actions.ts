import { ActionTree } from 'vuex';
import { StateInterface } from '../../index';
import { PerformanceReviewStateInterface } from './state';
import axios from 'axios';
import { ReviewNoteCreate } from 'src/store/types';

const actions: ActionTree<PerformanceReviewStateInterface, StateInterface> = {
  getAllReviewNotes: ({ commit }) => {
    axios({ url: 'http://localhost:8000/api/v1/reviewnote' })
      .then(resp => {
        commit('setAllReviewNotes', resp);
      })
      .catch(e => {
        console.log(e)
      });
  },
  createReviewNote: ({ dispatch }, reviewNote: ReviewNoteCreate) => {
    axios({ url: 'http://localhost:8000/api/v1/reviewnote', data: reviewNote, method: 'POST' })
      .then(() => {
        dispatch('getAllReviewNotes')
          .catch(e => {
            console.log(e)
          })
      })
      .catch(e => {
        console.log(e)
      });
  }
};

export default actions;

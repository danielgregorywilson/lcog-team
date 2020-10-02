import { ActionTree } from 'vuex';
import { StateInterface } from '../../index';
import { PerformanceReviewStateInterface } from './state';
import axios from 'axios';
import { ReviewNoteCreate } from 'src/store/types';

const actions: ActionTree<PerformanceReviewStateInterface, StateInterface> = {
  getNextPerformanceReview: ({ commit }, data: {pk: number}) => {
    axios({ url: `http://localhost:8000/api/v1/employee/${data.pk}/employee_next_performance_review`})
      .then(resp => {
        commit('setNextPerformanceReview', resp)
      })
      .catch(e => {
        console.log(e)
      })
  },
  employeeMarkDiscussed: ({ commit }) => {
    commit('employeeMarkDiscussed')
  },
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
  },
  getAllPerformanceReviewsActionRequired: ({ commit }) => {
    axios({ url: 'http://localhost:8000/api/v1/performancereview?action_required=True' })
      .then(resp => {
        commit('setAllPerformanceReviewsActionRequired', resp);
      })
      .catch(e => {
        console.log(e)
      });
  },
  getAllPerformanceReviewsActionNotRequired: ({ commit }) => {
    axios({ url: 'http://localhost:8000/api/v1/performancereview?action_required=False' })
      .then(resp => {
        commit('setAllPerformanceReviewsActionNotRequired', resp);
      })
      .catch(e => {
        console.log(e)
      });
  },
};

export default actions;

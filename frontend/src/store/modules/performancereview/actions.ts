import { ActionTree } from 'vuex';
import { StateInterface } from '../../index';
import { PerformanceReviewStateInterface } from './state';
import axios from 'axios';
import { PerformanceReviewUpdate, ReviewNoteCreate } from 'src/store/types';

const actions: ActionTree<PerformanceReviewStateInterface, StateInterface> = {
  getNextPerformanceReview: ({ commit }, data: {pk: number}) => {
    axios({ url: `${ process.env.API_URL }api/v1/employee/${data.pk}/employee_next_performance_review`}) // eslint-disable-line @typescript-eslint/restrict-template-expressions
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
    axios({ url: `${ process.env.API_URL }api/v1/reviewnote` }) // eslint-disable-line @typescript-eslint/restrict-template-expressions
      .then(resp => {
        commit('setAllReviewNotes', resp);
      })
      .catch(e => {
        console.log(e)
      });
  },
  createReviewNote: ({ dispatch }, reviewNote: ReviewNoteCreate) => {
    axios({ url: `${ process.env.API_URL }api/v1/reviewnote`, data: reviewNote, method: 'POST' }) // eslint-disable-line @typescript-eslint/restrict-template-expressions
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
  // All performance reviews for your direct reports as well as their descendants
  getAllPerformanceReviews: ({ commit }, data: {isUpperManager: boolean}) => {
    let targetUrl: string
    if (data.isUpperManager) {
      targetUrl = `${ process.env.API_URL }api/v1/performancereview?upper_manager=true` // eslint-disable-line
    } else {
      targetUrl = `${ process.env.API_URL }api/v1/performancereview` // eslint-disable-line
    }
    return new Promise((resolve, reject) => {
      axios({ url: targetUrl })
      .then(resp => {
        commit('setAllPerformanceReviews', resp);
        resolve(resp);
      })
      .catch(e => {
        console.log(e)
        reject(e)
      });
    })
  },
  getAllPerformanceReviewsActionRequired: ({ commit }) => {
    axios({ url: `${ process.env.API_URL }api/v1/performancereview?action_required=True` }) // eslint-disable-line @typescript-eslint/restrict-template-expressions
      .then(resp => {
        commit('setAllPerformanceReviewsActionRequired', resp);
      })
      .catch(e => {
        console.log(e)
      });
  },
  getAllPerformanceReviewsActionNotRequired: ({ commit }) => {
    axios({ url: `${ process.env.API_URL }api/v1/performancereview?action_required=False` }) // eslint-disable-line @typescript-eslint/restrict-template-expressions
      .then(resp => {
        commit('setAllPerformanceReviewsActionNotRequired', resp);
      })
      .catch(e => {
        console.log(e)
      });
  },
  getAllUpperManagerPerformanceReviewsActionRequired: ({ commit }) => {
    axios({ url: `${ process.env.API_URL }api/v1/performancereview?upper_manager=True&action_required=True` }) // eslint-disable-line @typescript-eslint/restrict-template-expressions
      .then(resp => {
        commit('setAllUpperManagerPerformanceReviewsActionRequired', resp);
      })
      .catch(e => {
        console.log(e)
      });
  },
  getAllUpperManagerPerformanceReviewsActionNotRequired: ({ commit }) => {
    axios({ url: `${ process.env.API_URL }api/v1/performancereview?upper_manager=True&action_required=False` }) // eslint-disable-line @typescript-eslint/restrict-template-expressions
      .then(resp => {
        commit('setAllUpperManagerPerformanceReviewsActionNotRequired', resp);
      })
      .catch(e => {
        console.log(e)
      });
  },
  updatePerformanceReview: ({ dispatch }, performanceReview: PerformanceReviewUpdate) => {
    const token = localStorage.getItem('user-token')
    return new Promise((resolve, reject) => {
      axios({ url: `${ process.env.API_URL }api/v1/performancereview/${performanceReview.pk}`, data: performanceReview, method: 'PUT', headers: { 'Authorization': `Token ${ token }`} }) // eslint-disable-line
      .then(resp => {
        dispatch('getAllPerformanceReviews')
          .catch(e => {
            console.log(e)
          })
        resolve(resp);
      })
      .catch(e => {
        console.log(e)
        reject(e)
      });
    })
  },
};

export default actions;

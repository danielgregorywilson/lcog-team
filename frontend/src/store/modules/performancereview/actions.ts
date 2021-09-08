import { ActionTree } from 'vuex';
import { StateInterface } from '../../index';
import { PerformanceReviewStateInterface } from './state';
import axios from 'axios';
import { ReviewNoteCreate, SignatureCreate } from 'src/store/types';

const actions: ActionTree<PerformanceReviewStateInterface, StateInterface> = {
  getNextPerformanceReview: ({ commit }, data: {pk: number}) => {
    axios({ url: `${ process.env.API_URL }api/v1/employee/${data.pk}/employee_next_performance_review`}) // eslint-disable-line @typescript-eslint/restrict-template-expressions
      .then(resp => {
        commit('setNextPerformanceReview', resp)
      })
      .catch(e => {
        console.error('Error getting next PR:', e)
      })
  },
  getAllReviewNotes: ({ commit }) => {
    axios({ url: `${ process.env.API_URL }api/v1/reviewnote` }) // eslint-disable-line @typescript-eslint/restrict-template-expressions
      .then(resp => {
        commit('setAllReviewNotes', resp);
      })
      .catch(e => {
        console.error('Error getting all review notes:', e)
      });
  },
  createReviewNote: ({ dispatch }, reviewNote: ReviewNoteCreate) => {
    axios({ url: `${ process.env.API_URL }api/v1/reviewnote`, data: reviewNote, method: 'POST' }) // eslint-disable-line @typescript-eslint/restrict-template-expressions
      .then(() => {
        dispatch('getAllReviewNotes')
          .catch(e => {
            console.error('Error getting all review notes ater creating a review note:', e)
          })
      })
      .catch(e => {
        console.error('Error creating a review note:', e)
      });
  },
  createSignature: ({}, signature: SignatureCreate) => {
    axios({ url: `${ process.env.API_URL }api/v1/signature`, data: signature, method: 'POST' }) // eslint-disable-line @typescript-eslint/restrict-template-expressions
      .catch(e => {
        console.error('Error creating a signature:', e)
      });
  },
  getPerformanceReview: ({ commit }, data: {pk: number}) => {
    return new Promise((resolve, reject) => {
      axios({ url: `${ process.env.API_URL }api/v1/performancereview/${ data.pk }` })  // eslint-disable-line @typescript-eslint/restrict-template-expressions
      .then(resp => {
        commit('setPerformanceReview', resp);
        resolve(resp);
      })
      .catch(e => {
        console.error('Error getting performance review:', e)
        reject(e)
      });
    })
  },
  // All performance reviews for your direct reports as well as their descendants
  getAllPerformanceReviews: ({ commit }, data: {signature: boolean}) => {
    let targetUrl: string
    if (data.signature) {
      targetUrl = `${ process.env.API_URL }api/v1/performancereview?signature=true` // eslint-disable-line
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
        console.error('Error getting all performance reviews:', e)
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
        console.error('Error getting all performance reviews action required:', e)
      });
  },
  getAllPerformanceReviewsActionNotRequired: ({ commit }) => {
    axios({ url: `${ process.env.API_URL }api/v1/performancereview?action_required=False` }) // eslint-disable-line @typescript-eslint/restrict-template-expressions
      .then(resp => {
        commit('setAllPerformanceReviewsActionNotRequired', resp);
      })
      .catch(e => {
        console.error('Error setting all PRs action not required:', e)
      });
  },
  getAllSignaturePerformanceReviewsActionRequired: ({ commit }) => {
    axios({ url: `${ process.env.API_URL }api/v1/performancereview?signature=True&action_required=True` }) // eslint-disable-line @typescript-eslint/restrict-template-expressions
      .then(resp => {
        commit('setAllSignaturePerformanceReviewsActionRequired', resp);
      })
      .catch(e => {
        console.error('Error setting all signature PRs action required:', e)
      });
  },
  getAllSignaturePerformanceReviewsActionNotRequired: ({ commit }) => {
    axios({ url: `${ process.env.API_URL }api/v1/performancereview?signature=True&action_required=False` }) // eslint-disable-line @typescript-eslint/restrict-template-expressions
      .then(resp => {
        commit('setAllSignaturePerformanceReviewsActionNotRequired', resp);
      })
      .catch(e => {
        console.error('Error setting all signature PRs action not required:', e)
      });
  },
  // TODO: Still needed?
  // updatePerformanceReview: ({ dispatch }, performanceReview: PerformanceReviewUpdate) => {
  //   const token = localStorage.getItem('user-token')
  //   console.log('TODO:UPDATE')
  //   return new Promise((resolve, reject) => {
  //     debugger
  //     axios({ url: `${ process.env.API_URL }api/v1/performancereview/${performanceReview.pk}`, data: performanceReview, method: 'PUT', headers: { 'Authorization': `Token ${ token }`} }) // eslint-disable-line
  //     .then(resp => {
  //       dispatch('getAllPerformanceReviews')
  //         .catch(e => {
  //           console.error(e)
  //         })
  //       resolve(resp);
  //     })
  //     .catch(e => {
  //       console.error(e)
  //       reject(e)
  //     });
  //   })
  // },
  authLogout: ({commit}) => {
    return new Promise((resolve) => {
      commit('authLogout')
      resolve('Successfully triggered logout')
    })
  }
};

export default actions;

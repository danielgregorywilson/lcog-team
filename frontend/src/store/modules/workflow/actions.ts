import { ActionTree } from 'vuex';
import { StateInterface } from '../../index';
import { WorkflowStateInterface } from './state';
import axios from 'axios';

const apiURL = process.env.API_URL ? process.env.API_URL : 'https://api.team.lcog.org/'

const actions: ActionTree<WorkflowStateInterface, StateInterface> = {
  getCurrentWorkflowInstance: ({ commit }, data: {pk: number}) => {
    return new Promise((resolve, reject) => {
      axios({ url: `${ apiURL }api/v1/workflowinstance/${ data.pk }` })
        .then(resp => {
          commit('setCurrentWorkflowInstance', resp);
          resolve(resp)
        })
        .catch(e => {
          console.error('Error getting current workflow instance', e)
          reject(e)
        });
      })
  },

  completeStepInstance: ({dispatch}, data: {stepInstancePk: number, nextStepPk: number}) => {
    return new Promise((resolve, reject) => {
      axios({ url: `${ apiURL }api/v1/stepinstance/${ data.stepInstancePk }`, data, method: 'PATCH' })
        .then(resp => {
          resolve(resp)
        })  
        .catch(e => {
          console.error('Error completing current step instance', e)
          reject(e)
        });
    })
  }
};

export default actions;

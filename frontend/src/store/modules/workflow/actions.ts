import { ActionTree } from 'vuex';
import { StateInterface } from '../../index';
import { WorkflowStateInterface } from './state';
import axios from 'axios';

const apiURL = process.env.API_URL ? process.env.API_URL : 'https://api.team.lcog.org/'

const actions: ActionTree<WorkflowStateInterface, StateInterface> = {
  createNewEmployeeOnboarding: ({}) => {
    return new Promise((resolve, reject) => {
      axios({ url: `${ apiURL }api/v1/workflowinstance`, method: 'POST', data: {type: 'new_employee_onboarding'} })
        .then(resp => {
          resolve(resp)
        })
        .catch(e => {
          console.error(e)
          reject(e)
        });  
    })
  },
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
  // All workflows, optionally filtered to ongoing/completed
  getWorkflows: ({ commit }, data: {complete?: boolean, actionRequired?: boolean}) => {
    let targetUrl: string
    let mutation: string
    if (data == undefined) {
      targetUrl = `${ apiURL }api/v1/workflowinstance`
      mutation = 'setAllWorkflows'
    } else if (data.actionRequired !== undefined && data.actionRequired) {
      targetUrl = `${ apiURL }api/v1/workflowinstance?action_required=true`
      mutation = 'setWorkflowsActionRequired'
    } else {
      if (data.complete !== undefined) {
        if (data.complete) {
          targetUrl = `${ apiURL }api/v1/workflowinstance?complete=true`
          mutation = 'setWorkflowsComplete'
        } else {
          targetUrl = `${ apiURL }api/v1/workflowinstance?complete=false`
          mutation = 'setWorkflowsIncomplete'
        }
      } else {
        // Todo: All? Error?
      }
    }
    return new Promise((resolve, reject) => {
      axios({ url: targetUrl })
      .then(resp => {
        commit(mutation, resp);
        resolve(resp);
      })
      .catch(e => {
        console.error('Error getting workflows of type', mutation, e)
        reject(e)
      });
    })
  },
  completeStepInstance: ({}, data: {stepInstancePk: number, nextStepPk: number}) => {
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

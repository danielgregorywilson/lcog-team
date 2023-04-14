import axios from 'axios'
import { defineStore } from 'pinia';

import { apiURL, handlePromiseError } from 'src/stores/index'
import { EmployeeTransition, WorkflowInstance } from 'src/types'

export const useWorkflowsStore = defineStore('workflows', {
  state: () => ({
    currentWorkflowInstance: {} as WorkflowInstance,
    currentEmployeeTransition: {} as EmployeeTransition,
    workflowsActionRequired: [] as Array<WorkflowInstance>,
    workflowsComplete: [] as Array<WorkflowInstance>,
    workflowsIncomplete: [] as Array<WorkflowInstance>,
    allWorkflows: [] as Array<WorkflowInstance>,
  }),

  getters: {
    processInstanceCurrentStepPks: state => {
      const d: {[pk: number]: number} = {}
      if (!state.currentWorkflowInstance.pk) {
        return d
      }
      debugger
      state.currentWorkflowInstance.process_instances.forEach(pi => {
        if (pi.current_step_instance) {
          d[pi.pk] = pi.current_step_instance.pk  
        } else {
          d[pi.pk] = -1
        }
      })
      return d
    }
  },

  actions: {
    createNewEmployeeOnboarding(): Promise<WorkflowInstance> {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/workflowinstance`, method: 'POST', data: {type: 'new_employee_onboarding'} })
          .then(resp => {
            resolve(resp)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error creating new employee onboarding workflow instance', e)
          });  
      })
    },
    getCurrentWorkflowInstance(data: {pk: number}) {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/workflowinstance/${ data.pk }` })
          .then(resp => {
            debugger
            this.currentWorkflowInstance = resp.data.results
            resolve(resp)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error getting current workflow instance', e)
          });
        })
    },
    // All workflows, optionally filtered to ongoing/completed
    getWorkflows(data: {complete?: boolean, actionRequired?: boolean}) {
      let targetUrl: string
      let workflowType: 'allWorkflows' | 'workflowsActionRequired' | 'workflowsComplete' | 'workflowsIncomplete'
      if (data == undefined) {
        targetUrl = `${ apiURL }api/v1/workflowinstance`
        workflowType = 'allWorkflows'	
      } else if (data.actionRequired !== undefined && data.actionRequired) {
        targetUrl = `${ apiURL }api/v1/workflowinstance?action_required=true`
        workflowType = 'workflowsActionRequired'
      } else {
        if (data.complete !== undefined) {
          if (data.complete) {
            targetUrl = `${ apiURL }api/v1/workflowinstance?complete=true`
            workflowType = 'workflowsComplete'
          } else {
            targetUrl = `${ apiURL }api/v1/workflowinstance?complete=false`
            workflowType = 'workflowsIncomplete'
          }
        } else {
          // Todo: All? Error?
        }
      }
      return new Promise((resolve, reject) => {
        axios({ url: targetUrl })
        .then(resp => {
          this[workflowType] = resp.data.results
          resolve(resp);
        })
        .catch(e => {
          handlePromiseError(reject, `Error getting workflows of type ${ workflowType }`, e)
        });
      })
    },
    completeStepInstance(data: {stepInstancePk: number, nextStepPk: number}) {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/stepinstance/${ data.stepInstancePk }`, data, method: 'PATCH' })
          .then(resp => {
            resolve(resp)
          })  
          .catch(e => {
            handlePromiseError(reject, 'Error completing current step instance', e)
          });
      })
    },
    deleteWorkflowInstance(workflowInstancePk: string) {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/workflowinstance/${ workflowInstancePk }`, method: 'DELETE' })
          .then(resp => {
            resolve(resp)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error deleting workflow instance', e)
            reject(e)
          });
      })
    },
    authLogout() {
      return new Promise((resolve) => {
        this.$reset()
        resolve('Successfully triggered logout')
      })
    }
  }
});

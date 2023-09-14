import axios from 'axios'
import { defineStore } from 'pinia'

import { apiURL, handlePromiseError } from 'src/stores/index'
import { EmployeeTransition, EmployeeTransitionUpdate, WorkflowInstance } from 'src/types'

export const useWorkflowsStore = defineStore('workflows', {
  state: () => ({
    currentWorkflowInstance: {} as WorkflowInstance,
    workflowsIncomplete: [] as Array<WorkflowInstance>,
    workflowsComplete: [] as Array<WorkflowInstance>,
    workflowsArchived: [] as Array<WorkflowInstance>,
  }),

  getters: {
    currentEmployeeTransition(state): EmployeeTransition {
      return state.currentWorkflowInstance.transition || {} as EmployeeTransition
    },
    processInstanceCurrentStepPks: state => {
      const d: {[pk: number]: number} = {}
      if (!state.currentWorkflowInstance.pk) {
        return d
      }
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
        axios({ url: `${ apiURL }api/v1/workflowinstance`, method: 'POST', data: {type: 'employee_onboarding'} })
          .then(resp => {
            resolve(resp.data)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error creating new employee onboarding workflow instance', e)
          })
      })
    },
    createNewEmployeeReturning(): Promise<WorkflowInstance> {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/workflowinstance`, method: 'POST', data: {type: 'employee_returning'} })
          .then(resp => {
            resolve(resp.data)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error creating new employee returning workflow instance', e)
          })
      })
    },
    createNewEmployeeChanging(): Promise<WorkflowInstance> {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/workflowinstance`, method: 'POST', data: {type: 'employee_changing'} })
          .then(resp => {
            resolve(resp.data)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error creating new employee changing workflow instance', e)
          })
      })
    },
    createNewEmployeeExiting(): Promise<WorkflowInstance> {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/workflowinstance`, method: 'POST', data: {type: 'employee_exiting'} })
          .then(resp => {
            resolve(resp.data)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error creating new employee exiting workflow instance', e)
          })
      })
    },
    getCurrentWorkflowInstance(pk: string) {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/workflowinstance/${ pk }` })
          .then(resp => {
            this.currentWorkflowInstance = resp.data
            resolve(resp)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error getting current workflow instance', e)
          })
        })
    },
    // All workflow instances, optionally filtered to ongoing/completed
    getWorkflows(data: {archived: boolean, complete: boolean}) {
      let targetUrl: string
      let workflowType: 'workflowsComplete' | 'workflowsIncomplete' | 'workflowsArchived'
      if (data.archived) {
        targetUrl = `${ apiURL }api/v1/workflowinstance?simple=true&archived=true`
        workflowType = 'workflowsArchived'
      } else if (data.complete) {
        targetUrl = `${ apiURL }api/v1/workflowinstance?simple=true&archived=false&complete=true`
        workflowType = 'workflowsComplete'
      } else {
        targetUrl = `${ apiURL }api/v1/workflowinstance?simple=true&archived=false&complete=false`
        workflowType = 'workflowsIncomplete'
      }
      return new Promise((resolve, reject) => {
        axios({ url: targetUrl })
        .then(resp => {
          this[workflowType] = resp.data.results
          resolve(resp)
        })
        .catch(e => {
          handlePromiseError(reject, `Error getting workflows of type ${ workflowType }`, e)
        })
      })
    },
    completeStepInstance(stepInstancePk: number, nextStepPk?: number) {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/stepinstance/${ stepInstancePk }`, data: {action: 'complete', stepInstancePk, nextStepPk}, method: 'PATCH' })
          .then(resp => {
            resolve(resp)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error completing current step instance', e)
          })
      })
    },
    undoStepInstanceCompletion(stepInstancePk: number, nextStepInstancePk?: number) {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/stepinstance/${ stepInstancePk }`, data: {action: 'undo', stepInstancePk, nextStepInstancePk}, method: 'PATCH' })
          .then(resp => {
            resolve(resp)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error undoing current step instance completion', e)
          })
      })
    },
    updateEmployeeTransition(pk: string, data: EmployeeTransitionUpdate): Promise<EmployeeTransition> {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/employeetransition/${ pk }`, data, method: 'PUT' })
          .then(resp => {
            resolve(resp.data)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error updating employee transition', e)
          })
      })
    },
    sendGasPINNotificationEmail(pk: string, data: {
      senderName: string, senderEmail: string, transition_url: string
    }): Promise<boolean> {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/employeetransition/${ pk }/send_gas_pin_notification_email`, data, method: 'POST' })
          .then(() => {
            resolve(true)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error sending gas PIN notification email', e)
          })
      })
    },
    sendTransitionToEmailList(pk: string, data: {
      type: 'SDS'|'FI'|'HR'|'STN', update: boolean, extraMessage: string,
      senderName: string, senderEmail: string, transition_url: string
    }): Promise<boolean> {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/employeetransition/${ pk }/send_transition_to_email_list`, data, method: 'POST' })
          .then(() => {
            resolve(true)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error sending employee transition to email list', e)
          })
      })
    },
    archiveWorkflowInstance(workflowInstancePk: string) {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/workflowinstance/${ workflowInstancePk }`, data: {action: 'archive'}, method: 'PATCH' })
          .then(resp => {
            resolve(resp)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error archiving workflow instance', e)
          })
      })
    },
    restoreWorkflowInstance(workflowInstancePk: string) {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/workflowinstance/${ workflowInstancePk }`, data: {action: 'restore'}, method: 'PATCH' })
          .then(resp => {
            resolve(resp)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error restoring workflow instance', e)
          })
      })
    },
    completeWorkflowInstance(workflowInstancePk: string) {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/workflowinstance/${ workflowInstancePk }`, data: {action: 'complete'}, method: 'PATCH' })
          .then(resp => {
            resolve(resp)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error completing workflow instance', e)
          })
      })
    },
    reopenWorkflowInstance(workflowInstancePk: string) {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/workflowinstance/${ workflowInstancePk }`, data: {action: 'reopen'}, method: 'PATCH' })
          .then(resp => {
            resolve(resp)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error reopening workflow instance', e)
          })
      })
    },
    authLogout() {
      return new Promise((resolve) => {
        this.$reset()
        resolve('Successfully triggered logout')
      })
    }
  }
})

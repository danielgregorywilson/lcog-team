<template>
  <q-page class="q-pa-md" v-if="workflowInstanceLoaded()">
    <div class="row items-center q-mb-sm">
      <div class="text-h4 q-mr-md">{{ wfi().workflow.name }}</div>
      <div style="width: 100px;">
        <q-linear-progress rounded size="25px" :value="wfi().percent_complete/100" color="primary">
          <div class="absolute-full flex flex-center">
            <q-badge color="white" text-color="primary" :label="`${wfi().percent_complete}%`" />
          </div>
        </q-linear-progress>
      </div>
    </div>
    <q-btn-group push v-if="hasEmployeeTransition()">
      <q-btn push :color="isSelected('workflow-processes')" glossy label="Processes" :to="{name: 'workflow-processes', params: {pk: wfi().pk}}" />
      <q-btn push :color="isSelected('workflow-transition-form')" glossy label="Employee Transition Form" :to="{name: 'workflow-transition-form', params: {pk: wfi().pk}}" />
    </q-btn-group>
    <router-view :key="$route.path" />
  </q-page>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { onMounted, watch } from 'vue'

import useEventBus from 'src/eventBus'
import { handlePromiseError } from 'src/stores'
import { useUserStore } from 'src/stores/user'
import { useWorkflowsStore } from 'src/stores/workflows'
import { WorkflowInstance } from 'src/types'
import { getCurrentUser, getRoutePk } from 'src/utils'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const workflowsStore = useWorkflowsStore()
const bus = useEventBus()

function workflowInstanceLoaded() {
  return workflowsStore.currentWorkflowInstance.pk != null
}

function wfi(): WorkflowInstance {
  return workflowsStore.currentWorkflowInstance
}

function hasEmployeeTransition() {
  // TODO: If not, then just show the processes and no subnav
  return true
}

function isSelected(currentRouteName: string) {
  if (route.name == currentRouteName) {
    return 'primary'
  } else {
    return 'grey'
  }
}

function retrieveWorkflowInstance() {
  return new Promise((resolve, reject) => {
    const pk = getRoutePk(route)
    if (!pk) {
      handlePromiseError(reject, 'No pk found in route params', '')
      return
    }
    workflowsStore.getCurrentWorkflowInstance(pk)
    .then(() => {
      const wfInstance: WorkflowInstance = workflowsStore.currentWorkflowInstance
      if (!wfInstance) {
        console.log('Workflow instance does not seem to exist. Redirecting...')
        router.push('/')
          .catch(e => {
            console.error('Error navigating to dashboard upon not finding a matching Workflow Instance:', e)
            reject(e)
          })
        return
      }
      // Trigger ProcessInstanceDetail to get a new current step
      bus.emit('updateProcessInstances', Math.random())
      resolve('Got Workflow Instance')
    })
    .catch(e => {
      console.error('Error retrieving workflow instance', e)
      reject(e)
    })
  })
}

function userHasWorkflowRoles() {
  return userStore.getEmployeeProfile.workflow_roles.length > 0
}

onMounted(() => {
  getCurrentUser()
    .then(() => {
      if (!userHasWorkflowRoles()) {
        router.push({ name: 'dashboard' })
      } else {
        retrieveWorkflowInstance()
          .then(() => bus.emit('workflowInstanceRetrieved', Math.random()))
          .catch(e => {
            console.error('Error retrieving workflow instance:', e)
          })
      }
    })
    .catch(e => {
      // User not authenticated or an error occurred fetching the user
      console.error(e)
      router.push({ name: 'dashboard' })
    })
})

// We trigger updating the current step instance in WorkflowInstanceDetail when
// we complete a step and reload it.
watch(() => bus.bus.value.get('completedStep'), () => {
  retrieveWorkflowInstance()
    .then(() => bus.emit('workflowInstanceRetrieved', Math.random()))
    .catch(e => {
      console.error('Error retrieving workflow instance:', e)
    })
})
</script>

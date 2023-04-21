<template>
  <q-page class="q-pa-md" v-if="workflowInstanceLoaded()">
    <div class="text-h4 q-mb-sm">{{ currentWorkflowInstance().workflow.name }}</div>
    <q-btn-group push v-if="hasEmployeeTransition()">
      <q-btn push :color="isSelected('workflow-processes')" glossy label="Processes" :to="{name: 'workflow-processes', params: {pk: currentWorkflowInstance().pk}}" />
      <q-btn push :color="isSelected('workflow-transition-form')" glossy label="Employee Transition Form" :to="{name: 'workflow-transition-form', params: {pk: currentWorkflowInstance().pk}}" />
    </q-btn-group>
    <router-view :key="$route.path" />
  </q-page>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { onMounted, watch } from 'vue'

import useEventBus from 'src/eventBus'
import { handlePromiseError } from 'src/stores'
import { useWorkflowsStore } from 'src/stores/workflows'
import { WorkflowInstance } from 'src/types'
import { getRoutePk } from 'src/utils'

const route = useRoute()
const router = useRouter()
const workflowsStore = useWorkflowsStore()
const bus = useEventBus()

function workflowInstanceLoaded() {
  return workflowsStore.currentWorkflowInstance.pk != null
}

function currentWorkflowInstance(): WorkflowInstance {
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
      debugger
      console.error('Error retrieving workflow instance', e)
      reject(e)
    })
  })
}


onMounted(() => {
  retrieveWorkflowInstance()
    .then(() => bus.emit('workflowInstanceRetrieved', Math.random()))
    .catch(e => {
      console.error('Error retrieving workflow instance:', e)
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

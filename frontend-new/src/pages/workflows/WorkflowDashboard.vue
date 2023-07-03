<template>
  <div class="row items-center q-mb-sm">
    <q-avatar
      icon="person_add"
      color="primary"
      text-color="white"
      font-size="22px"
      class="q-mr-sm"
      size="md"
    />
    <div class="text-h5">Employees Onboarding</div>
  </div>
  <WorkflowTable
    :complete="false"
    type="new"
    :allowAddDelete="true"
    v-on:retrieve="retrieveWorkflows"
  />
  <div class="row items-center q-mb-sm q-mt-md">
    <q-avatar
      icon="hail"
      color="primary"
      text-color="white"
      font-size="22px"
      class="q-mr-sm"
      size="md"
    />
    <div class="text-h5">Employees Returning</div>
  </div>
  <WorkflowTable
    :complete="false"
    type="return"
    :allowAddDelete="true"
    v-on:retrieve="retrieveWorkflows"
  />
  <div class="row items-center q-mb-sm q-mt-md">
    <q-avatar
      icon="directions_bike"
      color="primary"
      text-color="white"
      font-size="22px"
      class="q-mr-sm"
      size="md"
    />
    <div class="text-h5">Employees Changing</div>
  </div>
  <WorkflowTable
    :complete="false"
    type="change"
    :allowAddDelete="true"
    v-on:retrieve="retrieveWorkflows()"
  />
  <div class="row items-center q-mb-sm q-mt-md">
    <q-avatar
      icon="person_remove"
      color="primary"
      text-color="white"
      font-size="22px"
      class="q-mr-sm"
      size="md"
    />
    <div class="text-h5">Employees Exiting</div>
  </div>
  <WorkflowTable
    :complete="false"
    type="exit"
    :allowAddDelete="true"
    v-on:retrieve="retrieveWorkflows"
  />
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

import WorkflowTable from 'src/components/workflows/WorkflowTable.vue'
import { useUserStore } from 'src/stores/user'
import { useWorkflowsStore } from 'src/stores/workflows'
import { getCurrentUser } from 'src/utils'

const router = useRouter()
const userStore = useUserStore()
const workflowsStore = useWorkflowsStore()

let workflowsLoaded = ref(false)

function userHasWorkflowRoles() {
  return userStore.getEmployeeProfile.workflow_roles.length > 0
}

function retrieveWorkflows(): void {
  workflowsStore.getWorkflows({complete: false})
    .then(() => {
      workflowsLoaded.value = true
    })  
    .catch(e => {
      console.error('Error retrieving incomplete workflows:', e)
    })
}

onMounted(() => {
  getCurrentUser()
    .then(() => {
      if (!userHasWorkflowRoles()) {
        router.push({ name: 'dashboard' })
      } else {
        retrieveWorkflows()
      }
    })
    .catch(e => {
      // User not authenticated or an error occurred fetching the user
      console.error(e)
      router.push({ name: 'dashboard' })
    })
})

</script>

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
  <WorkflowTable :complete="false" type="new"/>
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
  <WorkflowTable :complete="false" type="return"/>
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
  <WorkflowTable :complete="false" type="change"/>
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
  <WorkflowTable :complete="false" type="exit"/>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

import WorkflowTable from 'src/components/workflows/WorkflowTable.vue'
import { useUserStore } from 'src/stores/user'
import { getCurrentUser } from 'src/utils'

const router = useRouter()
const userStore = useUserStore()

function userHasWorkflowRoles() {
  return userStore.getEmployeeProfile.workflow_roles.length > 0
}

onMounted(() => {
  getCurrentUser()
    .then(() => {
      if (!userHasWorkflowRoles()) {
        router.push({ name: 'dashboard' })
      }
    })
    .catch(e => {
      // User not authenticated or an error occurred fetching the user
      console.error(e)
      router.push({ name: 'dashboard' })
    })
})

</script>

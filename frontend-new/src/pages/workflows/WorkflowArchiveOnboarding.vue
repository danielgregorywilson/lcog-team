<template>
  <div class="row items-center q-mb-md">
    <q-avatar
      icon="person_add"
      color="primary"
      text-color="white"
      font-size="32px"
      class="q-mr-sm"
    />
    <div class="text-h4">Employees Onboarding</div>
  </div>
  <!-- <div class="text-h6">Action Required</div>
  <workflow-table :actionRequired="true" />
  <div class="text-h6">All Incomplete</div>
  <workflow-table :complete="false" />
  <div class="text-h6">All Complete</div>
  <workflow-table :complete="true" /> -->
  <!-- <div class="text-h6">All</div> -->
  <WorkflowTable :complete="true" type="all" :noPagination="true" />
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

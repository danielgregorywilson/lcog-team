<template>
<q-layout view="lHh Lpr lFf">
  <q-page-container>
    <q-page>
      Test
    </q-page>
  </q-page-container>
</q-layout>
</template>

<style lang="scss">
</style>

<script setup lang="ts">
import { onMounted } from 'vue'

import { useTimeOffStore } from 'src/stores/timeoff'
import { useWorkflowsStore } from 'src/stores/workflows'

const timeOffStore = useTimeOffStore()
const workflowsStore = useWorkflowsStore()

onMounted(() => {
  // workflowsStore.getWorkflows({archived: false, complete: false})
  timeOffStore.getTeamTimeOffRequests()
})
</script>

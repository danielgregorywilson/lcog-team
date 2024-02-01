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

const timeOffStore = useTimeOffStore()

onMounted(() => {
  // workflowsStore.getWorkflows({archived: false, complete: false})
  timeOffStore.getTeamTimeOffRequests()
})
</script>

<template>
  <div class="q-pt-md">
    <div v-for="pi of currentWorkflowInstance().process_instances" :key="pi.pk">
      <div class="text-h5">{{pi.process.name}}</div>
      <ProcessInstanceDetail :pi="pi" />
    </div>
  </div>
</template>

<script setup lang="ts">
import ProcessInstanceDetail from 'src/components/workflows/ProcessInstanceDetail.vue'
import { WorkflowInstance } from 'src/types'

import { useWorkflowsStore } from 'src/stores/workflows'

const workflowsStore = useWorkflowsStore()

function currentWorkflowInstance(): WorkflowInstance {
  return workflowsStore.currentWorkflowInstance
}
</script>

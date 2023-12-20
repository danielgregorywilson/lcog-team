<template>
  <div class="q-pt-md">
    <div v-if="currentWorkflowInstance().process_instances.length === 0" class="text-h6 text-center q-pa-md">
      No processes have been started yet.	
    </div>
    <div v-for="pi of currentWorkflowInstance().process_instances" :key="pi.pk" class="q-mb-md">
      <div class="row items-center q-mb-sm">
        <div class="text-h5 q-mr-md">{{pi.process.name}}</div>
        <div style="width: 100px;">
          <q-linear-progress rounded size="25px" :value="pi.percent_complete/100" color="primary">
            <div class="absolute-full flex flex-center">
              <q-badge color="white" text-color="primary" :label="`${pi.percent_complete}%`" />
            </div>
          </q-linear-progress>
        </div>
      </div>
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

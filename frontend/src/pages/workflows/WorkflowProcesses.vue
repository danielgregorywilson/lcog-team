<template>
<div class="q-pt-md">
  <div v-for="pi of currentWorkflowInstance().process_instances" :key="pi.pk">
    <div class="text-h5">{{pi.process.name}}</div>
    <process-instance-detail :pi="pi" />
  </div>
</div>
</template>

<style scoped lang="scss">
</style>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import ProcessInstanceDetail from '../../components/workflows/ProcessInstanceDetail.vue'
import { VuexStoreGetters, WorkflowInstance } from '../../store/types'

@Component({
  components: { ProcessInstanceDetail }
})
export default class WorkflowProcesses extends Vue {
  private getters = this.$store.getters as VuexStoreGetters

  public currentStepInstance = -1;

  public currentWorkflowInstance(): WorkflowInstance {
    return this.getters['workflowModule/currentWorkflowInstance']
  }

}
</script>

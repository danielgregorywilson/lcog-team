<template>
  <q-page class="q-pa-md">
    <div class="text-h4">{{currentWorkflowInstance().workflow.name}}</div>
    <div v-for="pi of currentWorkflowInstance().process_instances">
      <div class="text-h5">{{pi.process.name}}</div>
      <process-instance-detail :pi="pi" @completed-step="retrieveWorkflowInstance"  />
    </div>
  </q-page>
</template>

<style scoped lang="scss">
</style>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { bus } from '../../App.vue'
import ProcessInstanceDetail from '../../components/workflows/ProcessInstanceDetail.vue'
import { VuexStoreGetters, WorkflowInstance } from '../../store/types'

@Component({
  components: { ProcessInstanceDetail }
})
export default class EIS extends Vue {
  private getters = this.$store.getters as VuexStoreGetters

  public currentStepInstance = -1;

  public currentWorkflowInstance(): WorkflowInstance {
    return this.getters['workflowModule/currentWorkflowInstance']
  }

  public retrieveWorkflowInstance() {
    return new Promise((resolve, reject) => {
      this.$store.dispatch('workflowModule/getCurrentWorkflowInstance', {pk: this.$route.params.pk})
      .then(() => {
        const wfInstance: WorkflowInstance = this.getters['workflowModule/currentWorkflowInstance'] // eslint-disable-line @typescript-eslint/no-unsafe-member-access
        if (!wfInstance) {
            console.log('Workflow instance does not seem to exist. Redirecting...')
            this.$router.push('/')
              .catch(e => {
                console.error('Error navigating to dashboard upon not finding a matching Workflow Instance:', e)
                reject(e)
              })
            return
          }
        if (!wfInstance.process_instances[0].completed_at) {
          this.currentStepInstance = wfInstance.process_instances[0].current_step_instance.pk
        } else {
          // Process Instance is complete
          this.currentStepInstance = -1
        }
        bus.$emit('updateProcessInstances') // Trigger ProcessInstanceDetail to get a new current step
        resolve('Got Workflow Instance')
      })
      .catch(e => {
        console.error('Error retrieving workflow instance', e)
        reject(e)
      })
    })
    
  }

  mounted() {
    this.retrieveWorkflowInstance()
      .catch(e => {
        console.error('Error retrieving workflow instance:', e)
      })
  }
}
</script>

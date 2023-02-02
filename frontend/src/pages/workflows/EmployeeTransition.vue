<template>
  <div class="q-pt-md">
    <div class="label-radio-triplet">
      <div class="text-bold" id="step-increase">Step Increase:</div>
      <q-radio v-model="type" val="N" />
      <div>New</div>
      <q-radio v-model="type" val="R" />
      <div>Return</div>
      <q-radio v-model="type" val="M" />
      <div>Change/Modify</div>
      <q-radio v-model="type" val="E" />
      <div>Exit</div>
    </div>

    {{currentEmployeeTransition()}}
  </div>
</template>

<style scoped lang="scss">
.label-radio-triplet {
    display: grid;
    justify-content: center;
    align-items: center;
    grid-template-columns: auto auto auto auto auto auto auto auto auto;
  }
</style>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { VuexStoreGetters, WorkflowInstance } from '../../store/types'

@Component
export default class EmployeeTransition extends Vue {
  private getters = this.$store.getters as VuexStoreGetters

  public currentEmployeeTransition(): EmployeeTransition {
    return this.getters['workflowModule/currentEmployeeTransition']
  }

  public type = ''

  public retrieveEmployeeTransition() {
    
    
    return new Promise((resolve, reject) => {
      this.$store.dispatch('workflowModule/getCurrentEmployeeTransition', {pk: this.$route.params.pk})
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
    this.retrieveEmployeeTransition()
      .catch(e => {
        console.error('Error retrieving workflow instance:', e)
      })
  }
}
</script>

<template>
  <q-page class="q-pa-md">
    <div class="text-h4">{{currentWorkflowInstance().workflow.name}}</div>
    <div v-for="pi of currentWorkflowInstance().process_instances">
      <div class="text-h5">{{pi.process.name}}</div>
      <process-instance-detail :pi="pi" @completed-step="retrieveWorkflowInstance"  />
    </div>
    <!-- <hr />
    <div class="text-h5" v-if="currentWorkflowInstance().process_instances.length">
      {{currentWorkflowInstance().process_instances[0].process.name}}
    </div>
    <div class="q-mt-sm">
      <q-stepper
        v-if="currentWorkflowInstance().process_instances.length"
        v-model="currentStepInstance"
        vertical
        color="primary"
        animated
      >
        <q-step
          v-for="instance of currentWorkflowInstance().process_instances[0].step_instances"
          :key="instance.pk"
          :name="instance.pk"
          :title="instance.step.name"
          icon="settings"
          :done="!!instance.completed_at"
        >
          <div>{{ instance.step.description }}</div>
          <q-stepper-navigation>
            <div v-if="instance.step.choices_prompt">
              {{instance.step.choices_prompt}}
              <q-btn
                v-for="choice of instance.step.next_step_choices"
                class="q-ml-sm"
                :key="choice.pk"
                @click="completeStep(instance.pk, choice.next_step_pk)"
                color="primary"
                :label="choice.choice_text"
              />
            </div>
            <div v-else>
              <q-btn @click="completeStep(instance.pk)" color="primary" label="Continue" />
            </div>
          </q-stepper-navigation>
        </q-step>
      </q-stepper>
    </div> -->
    
    <!-- <div class="q-mt-sm">
      <q-stepper
        v-model="step"
        vertical
        color="primary"
        animated
      >
        <q-step
          :name="1"
          title="Select campaign settings"
          icon="settings"
          :done="step > 1"
        >
          For each ad campaign that you create, you can control how much you're willing to
          spend on clicks and conversions, which networks and geographical locations you want
          your ads to show on, and more.

          <q-stepper-navigation>
            <q-btn @click="step = 2" color="primary" label="Continue" />
          </q-stepper-navigation>
        </q-step>

        <q-step
          :name="2"
          title="Create an ad group"
          caption="Optional"
          icon="create_new_folder"
          :done="step > 2"
        >
          An ad group contains one or more ads which target a shared set of keywords.

          <q-stepper-navigation>
            <q-btn @click="step = 4" color="primary" label="Continue" />
            <q-btn flat @click="step = 1" color="primary" label="Back" class="q-ml-sm" />
          </q-stepper-navigation>
        </q-step>

        <q-step
          :name="3"
          title="Ad template"
          icon="assignment"
          disable
        >
          This step won't show up because it is disabled.
        </q-step>

        <q-step
          :name="4"
          title="Create an ad"
          icon="add_comment"
        >
          Try out different ad text to see what brings in the most customers, and learn how to
          enhance your ads using features like ad extensions. If you run into any problems with
          your ads, find out how to tell if they're running and how to resolve approval issues.

          <q-stepper-navigation>
            <q-btn color="primary" label="Finish" />
            <q-btn flat @click="step = 2" color="primary" label="Back" class="q-ml-sm" />
          </q-stepper-navigation>
        </q-step>
      </q-stepper>
    </div> -->
  </q-page>
</template>

<style scoped lang="scss">
</style>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { bus } from '../../App.vue'
import ProcessInstanceDetail from '../../components/workflows/ProcessInstanceDetail.vue'
import { VuexStoreGetters, WorkflowInstanceRetrieve } from '../../store/types'

@Component({
  components: { ProcessInstanceDetail }
})
export default class EIS extends Vue {
  private getters = this.$store.getters as VuexStoreGetters

  private wfInstancePk = -1
  public currentStepInstance = -1;
  private workflowInstancePk = 46

  // private isManager() {
  //   return this.getters['userModule/getEmployeeProfile'].is_manager
  // }

  public currentWorkflowInstance(): WorkflowInstanceRetrieve {
    return this.getters['workflowModule/currentWorkflowInstance']
  }

  // private currentStepInstance(): number {
  //   return this.currentWorkflowInstance().process_instances[0].current_step_instance.pk
  // } 

  // private numUnacknowledgedManagedTimeOffRequests(): number {
  //   const tors = this.getters['timeOffModule/managedTimeOffRequests'].results
  //   if (tors) {
  //     return tors.filter(tor => tor.acknowledged == null).length
  //   } else {
  //     return 0
  //   }
  // }

  public retrieveWorkflowInstance() {
    return new Promise((resolve, reject) => {
      this.$store.dispatch('workflowModule/getCurrentWorkflowInstance', {pk: this.$route.params.pk})
      .then(() => {
        const wfInstance: WorkflowInstanceRetrieve = this.getters['workflowModule/currentWorkflowInstance'] // eslint-disable-line @typescript-eslint/no-unsafe-member-access
        if (!wfInstance) {
            console.log('Workflow instance does not seem to exist. Redirecting...')
            this.$router.push('/')
              .catch(e => {
                console.error('Error navigating to dashboard upon not finding a matching Workflow Instance:', e)
                reject(e)
              })
            return
          }
        this.wfInstancePk = wfInstance.pk
        if (!wfInstance.process_instances[0].completed_at) {
          this.currentStepInstance = wfInstance.process_instances[0].current_step_instance.pk
        } else {
          // Process Instance is complete
          this.currentStepInstance = -1
        }
        resolve('Got Workflow Instance')
      })
      .catch(e => {
        console.error('Error retrieving workflow instance', e)
        reject(e)
      })
    })
    
  }

  // public completeStep(stepInstancePk: number, nextStepPk?: number): void {
  //   this.$store.dispatch('workflowModule/completeStepInstance', { stepInstancePk, nextStepPk })
  //     .then(() => {
  //       this.retrieveWorkflowInstance()
  //         .catch(e => {
  //           console.error('Error retrieving workflow instance:', e)
  //         })
  //     })
  //     .catch(e => {
  //       console.error('Error retrieving workflow instance', e)
  //     })
  // }

  mounted() {
    this.retrieveWorkflowInstance()
      .catch(e => {
        console.error('Error retrieving workflow instance:', e)
      })
  }
}
</script>

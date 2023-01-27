<template>
  <div>
    <q-stepper
      v-model="currentStepInstance"
      header-nav
      vertical
      color="primary"
      animated
    >
      <q-step
        v-for="si of pi.step_instances"
        :key="si.pk"
        :name="si.pk"
        :title="si.step.name"
        icon="play_arrow"
        :active-icon="stepInstanceIsComplete(si) ? 'edit' : 'play_arrow'"
        :color="si.pk == currentStepInstance ? 'primary' : 'secondary'"
        :done="!!si.completed_at"
      >
        <div>{{ si.step.description }}</div>
        <div v-if="si.completed_at" class="text-secondary">Completed by {{ si.completed_by_name }} on {{ formatDate(si.completed_at, 'dddd, M/D/YY [at] HH:MM') }}</div>
        <q-stepper-navigation v-if="!stepInstanceIsComplete(si)">
          <div v-if="si.step.next_step">
            <q-btn
              :disable="!canCompleteStepInstance(si)"
              @click="completeStep(si.pk)"
              color="primary"
              label="Continue"
            />
          </div>
          <div v-else>
            {{si.step.choices_prompt}}
            <q-btn
              v-for="choice of si.step.next_step_choices"
              class="q-ml-sm"
              :key="choice.pk"
              @click="completeStep(si.pk, choice.next_step_pk)"
              color="primary"
              :label="choice.choice_text"
              :disable="!canCompleteStepInstance(si)"
            />
          </div>
        </q-stepper-navigation>
      </q-step>
    </q-stepper>
  </div>
</template>

<style scoped lang="scss">

</style>

<script lang="ts">
import { date } from 'quasar'
import { Component, Prop, Vue } from 'vue-property-decorator'
import { bus } from '../../App.vue'
import { ProcessInstance, StepInstance, VuexStoreGetters } from '../../store/types'
// import { readableDate } from '../../filters'

@Component
export default class ProcessInstanceDetail extends Vue {
  @Prop({required: true}) readonly pi!: ProcessInstance

  public formatDate = date.formatDate

  private getters = this.$store.getters as VuexStoreGetters

  public currentStepInstance = -1;

  public setCurrentStepInstance() {
    this.currentStepInstance = this.getters['workflowModule/processInstanceCurrentStepPks'][this.pi.pk]
  }

  public stepInstanceIsComplete(stepInstance: StepInstance): boolean {
    if (stepInstance.completed_at) {
      return true
    } else {
      return false
    }
  }

  public canCompleteStepInstance(stepInstance: StepInstance): boolean {
    if (stepInstance.completed_at) {
      return false
    }
    const step = stepInstance.step
    if (this.$store.getters['userModule/getEmployeeProfile'].is_all_workflows_admin) {
      // If they are an All-Workflows-Admin, allow completion
      return true
    } else if (step.workflow_role_pk) {
      // If they are an admin of the workflow, allow completion
      return this.$store.getters['userModule/getEmployeeProfile'].workflow_roles.indexOf(step.workflow_role_pk) != -1
    } else if (step.process_role_pk) {
      // If they are an admin of the process, allow completion
      return this.$store.getters['userModule/getEmployeeProfile'].workflow_roles.indexOf(step.process_role_pk) != -1
    } else if (step.role) {
      // If they are assigned to the step's role, allow completion
      return this.$store.getters['userModule/getEmployeeProfile'].workflow_roles.indexOf(step.role.pk) != -1
    } else {
      // TODO: What should happen if no role assigned? Only admins? Everyone? Require all steps to have roles?
      return true
    }
  }

  public completeStep(stepInstancePk: number, nextStepPk?: number): void {
    this.$store.dispatch('workflowModule/completeStepInstance', { stepInstancePk, nextStepPk })
      .then(() => {
        this.setCurrentStepInstance()
        this.$emit('completed-step')
      })
      .catch(e => {
        console.error('Error completing step instance', e)
      })
  }

  created() {
    // We trigger updating the current step instance in WorkflowInstanceDetail when we complete a step and reload it.
    bus.$on('updateProcessInstances', () => {
      this.setCurrentStepInstance()
    })
  }

  mounted() {
    this.setCurrentStepInstance()
  }

}
</script>
  
<template>
  <div>
    <q-stepper
      v-model="pi.current_step_instance.pk"
      vertical
      color="primary"
      animated
    >
      <q-step
        v-for="si of pi.step_instances"
        :key="si.pk"
        :name="si.pk"
        :title="si.step.name"
        icon="settings"
        :done="!!si.completed_at"
      >
        <div>{{ si.step.description }}</div>
        <q-stepper-navigation>
          <div v-if="si.step.choices_prompt">
            {{si.step.choices_prompt}}
            <q-btn
              v-for="choice of si.step.next_step_choices"
              class="q-ml-sm"
              :key="choice.pk"
              @click="completeStep(si.pk, choice.next_step_pk)"
              color="primary"
              :label="choice.choice_text"
              :disable="!canCompleteStep(si.step)"
            />
          </div>
          <div v-else>
            <q-btn
              :disable="!canCompleteStep(si.step)"
              @click="completeStep(si.pk)"
              color="primary"
              label="Continue"
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
import { Component, Prop, Vue } from 'vue-property-decorator'
import { ProcessInstance, Step } from '../../store/types'

@Component
export default class ProcessInstanceDetail extends Vue {
  @Prop({required: true}) readonly pi!: ProcessInstance
  
  // public currentStepInstance = -1;

  public canCompleteStep(step: Step): boolean {
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
        this.$emit('completed-step')
      })
      .catch(e => {
        console.error('Error completing step instance', e)
      })
  }
}
</script>
  
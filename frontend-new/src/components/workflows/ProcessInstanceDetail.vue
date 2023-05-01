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
        <StepAction v-for="action of si.step.optional_actions" :action="action" :key="action.pk" />
        <div v-if="si.completed_at" class="text-secondary">Completed by {{ si.completed_by_name }} on {{ formatDate(si.completed_at, 'dddd, M/D/YY [at] HH:MM') }}</div>
        <q-stepper-navigation v-if="!stepInstanceIsComplete(si)">
          <div v-if="si.step.next_step">
            <q-btn
              :disable="!canCompleteStepInstance(si)"
              @click="completeStep(si.pk)"
              color="primary"
              label="Mark as Complete"
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

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { date } from 'quasar'
import StepAction from 'src/components/workflows/StepAction.vue'
import { ProcessInstance, StepInstance } from 'src/types'

import useEventBus from 'src/eventBus'
import { useUserStore } from 'src/stores/user'
import { useWorkflowsStore } from 'src/stores/workflows'

const userStore = useUserStore()
const workflowsStore = useWorkflowsStore()
const bus = useEventBus()

const props = defineProps<{
  pi: ProcessInstance
}>()

const formatDate = date.formatDate

let currentStepInstance = ref(-1)

function setCurrentStepInstance() {
  currentStepInstance.value = workflowsStore.processInstanceCurrentStepPks[props.pi.pk]
}

function stepInstanceIsComplete(stepInstance: StepInstance): boolean {
  if (stepInstance.completed_at) {
    return true
  } else {
    return false
  }
}

function canCompleteStepInstance(stepInstance: StepInstance): boolean {
  if (stepInstance.completed_at) {
    return false
  }
  const step = stepInstance.step
  if (userStore.getEmployeeProfile.is_all_workflows_admin) {
    // If they are an All-Workflows-Admin, allow completion
    return true
  } else if (step.workflow_role_pk) {
    // If they are an admin of the workflow, allow completion
    return userStore.getEmployeeProfile.workflow_roles.indexOf(step.workflow_role_pk) != -1
  } else if (step.process_role_pk) {
    // If they are an admin of the process, allow completion
    return userStore.getEmployeeProfile.workflow_roles.indexOf(step.process_role_pk) != -1
  } else if (step.role) {
    // If they are assigned to the step's role, allow completion
    return userStore.getEmployeeProfile.workflow_roles.indexOf(step.role.pk) != -1
  } else {
    // TODO: What should happen if no role assigned? Only admins? Everyone? Require all steps to have roles?
    return true
  }
}

function completeStep(stepInstancePk: number, nextStepPk?: number): void {
  workflowsStore.completeStepInstance(stepInstancePk, nextStepPk)
    .then(() => {
      setCurrentStepInstance()
      bus.emit('completedStep', Math.random())
    })
    .catch(e => {
      console.error('Error completing step instance', e)
    })
}

// We trigger updating the current step instance in WorkflowInstanceDetail when
// we complete a step and reload it.
watch(() => bus.bus.value.get('updateProcessInstances'), () => {
  setCurrentStepInstance()
})

onMounted(() => {
  setCurrentStepInstance()
})
</script>

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
            />
          </div>
          <div v-else>
            <q-btn @click="completeStep(si.pk)" color="primary" label="Continue" />
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
import { ProcessInstance } from '../../store/types'

@Component
export default class ProcessInstanceDetail extends Vue {
  @Prop({required: true}) readonly pi!: ProcessInstance
  
  // public currentStepInstance = -1;

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
  
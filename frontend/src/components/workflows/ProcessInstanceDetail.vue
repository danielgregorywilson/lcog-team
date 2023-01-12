<template>
  <div>
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
  </div>
</template>

<style scoped>

</style>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

@Component
export default class ProcessInstanceDetail extends Vue {

}
</script>
  
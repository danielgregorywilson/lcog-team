<template>
<q-page class="q-pa-md">
  <div class="text-h4">{{currentWorkflowInstance().workflow.name}}</div>
  <q-btn-group push v-if="hasEmployeeTransition()">
    <q-btn push color="secondary" glossy label="Processes" :to="{name: 'workflow-processes', params: {pk: currentWorkflowInstance().pk}}" />
    <q-btn push color="primary" glossy label="Employee Transition Form" :to="{name: 'workflow-transition-form', params: {pk: currentWorkflowInstance().pk}}" />
  </q-btn-group>
  <router-view :key="$route.path" />
</q-page>
</template>

<style scoped lang="scss">
</style>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { bus } from '../../App.vue'
import { VuexStoreGetters, WorkflowInstance } from '../../store/types'

@Component
export default class WorkflowInstanceDetail extends Vue {
  private getters = this.$store.getters as VuexStoreGetters

  public currentWorkflowInstance(): WorkflowInstance {
    return this.getters['workflowModule/currentWorkflowInstance']
  }

  public hasEmployeeTransition() {
    // TODO
    return true
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
        bus.$emit('updateProcessInstances') // Trigger ProcessInstanceDetail to get a new current step
        resolve('Got Workflow Instance')
      })
      .catch(e => {
        console.error('Error retrieving workflow instance', e)
        reject(e)
      })
    })
  }

  created() {
    // We trigger updating the current step instance in WorkflowInstanceDetail when we complete a step and reload it.
    bus.$on('completedStep', () => {
      this.retrieveWorkflowInstance()
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

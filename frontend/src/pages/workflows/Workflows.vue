<template>
  <q-page class="q-pa-md">
    <div class="q-py-md" v-if="hasWorkflowRoles()">
      <div class="row items-center q-mb-md">
        <q-avatar icon="person_add" color="primary" text-color="white" font-size="32px" class="q-mr-sm" />
        <div class="text-h4">Employees Onboarding</div>
      </div>
      <!-- <div class="text-h6">Action Required</div>
      <workflow-table :actionRequired="true" />
      <div class="text-h6">All Incomplete</div>
      <workflow-table :complete="false" />
      <div class="text-h6">All Complete</div>
      <workflow-table :complete="true" /> -->
      <!-- <div class="text-h6">All</div> -->
      <workflow-table />
    </div>
    <!-- <div class="q-py-md" v-if="isManager()">
      <div class="row items-center q-mb-md">
        <q-avatar icon="person_remove" color="primary" text-color="white" font-size="32px" class="q-mr-sm" />
        <div class="text-h4">Employees Exiting</div>
      </div>
      <div class="text-h6">Action Required</div>
      <workflow-table :actionRequired="true" />
      <div class="text-h6">No Action Required</div>
      <workflow-table :actionRequired="false" />
    </div> -->
  </q-page>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import WorkflowTable from '../../components/WorkflowTable.vue';

@Component({
  components: { WorkflowTable, }
})
export default class Workflows extends Vue {
  private currentIndex = -1;
  private title = '';
  public hasWorkflowRoles() {
    return this.$store.getters['userModule/getEmployeeProfile'].workflow_roles.length
  }
};
</script>

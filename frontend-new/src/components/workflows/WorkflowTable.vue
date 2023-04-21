<template>
  <div class="q-py-sm">
    <q-table
      :rows="workflows()"
      :columns="columns"
      :grid="$q.screen.lt.md"
      :no-data-label="noDataLabel()"
      row-key="name"
    >
      <!-- Slots for header cells: Shrink the width when the screen is too small to see the whole table width -->
      <!-- <template v-slot:header-cell-employeeName="props">
        <th v-if="$q.screen.lt.lg" style="white-space: normal;">{{props.col.label}}</th>
        <th v-else>{{props.col.label}}</th>
      </template>
      <template v-slot:header-cell-daysUntilReview="props">
        <th v-if="$q.screen.lt.lg" style="white-space: normal;">{{props.col.label}}</th>
        <th v-else>{{props.col.label}}</th>
      </template> -->
      <!-- Slots for body cells: Show dates in a familiar format; make sure status can wrap, and display action buttons -->
      <template v-slot:body-cell-startedAt="props">
        <q-td key="startedAt" :props="props">
          {{ readableDate(props.row.started_at) }}
        </q-td>
      </template>
      <template v-slot:body-cell-transitionDate="props">
        <q-td key="transitionDate" :props="props">
          {{ readableDate(props.row.transition_date) }}
        </q-td>
      </template>
      <template v-slot:body-cell-percentComplete="props">
        <q-td key="percentComplete" :props="props">
          <q-linear-progress size="25px" :value="props.row.percent_complete/100" color="primary">
            <div class="absolute-full flex flex-center">
              <q-badge color="white" text-color="primary" :label="`${props.row.percent_complete}%`" />
            </div>
          </q-linear-progress>
      </q-td>
      </template>
      <template v-slot:body-cell-actions="props">
        <q-td key="actions" :props="props">
          <q-btn class="col" dense round flat color="grey" @click="editWorkflowInstance(props.row)" icon="play_arrow"></q-btn>
          <q-btn v-if="workflowHasTransition(props.row) && canViewTransition(props.row)" class="col" dense round flat color="grey" @click="editTransitionForm(props.row)" icon="assignment"></q-btn>
          <q-btn v-if="canDeleteWorkflowInstance(props.row)" class="col" dense round flat color="grey" @click="showDeleteDialog(props.row)" icon="delete"></q-btn>
        </q-td>
      </template>
      <!-- <template v-slot:body-cell-status="props">
        <q-td style="white-space: normal;" :props="props">{{ props.row.status }}</q-td>
      </template> -->
      <!-- <template v-slot:body-cell-actions="props">
        <q-td :props="props">
          <div class="row">
            <q-btn class="col edit-button" dense round flat color="grey" @click="editEvaluation(props)" icon="edit"></q-btn>
            <q-btn class="col print-button" dense round flat color="grey" @click="printEvaluation(props)" icon="print">
              <q-tooltip content-style="font-size: 16px">Print Performance Review Form</q-tooltip>
            </q-btn>
            <q-btn v-if="props.row.signed_position_description" class="col print-button" dense round flat color="grey" @click="printEvaluationPositionDescription(props)" icon="print">
              <q-tooltip content-style="font-size: 16px">Print Signed Position Description</q-tooltip>
            </q-btn>
          </div>
        </q-td>
      </template> -->
      <!-- For grid mode, we need to specify everything in order for our action buttons to render -->
      <template v-slot:item="props">
        <div class="q-pa-xs col-xs-12 col-sm-6 col-md-4 col-lg-3 grid-style-transition">
          <q-card class="q-py-sm">
            <q-list dense>
              <q-item v-for="col in props.cols" :key="col.name">
                <div class="q-table__grid-item-row">
                  <div class="q-table__grid-item-title">{{ col.label }}</div>
                  <div class="q-table__grid-item-value" v-if="col.label != 'Actions'">
                    {{ col.value }}
                  </div>
                  <div class="q-table__grid-item-value row q-gutter-sm" v-else>
                    <q-btn class="col" dense round flat color="grey" @click="editWorkflowInstance(props.row)" icon="play_arrow"></q-btn>
                    <q-btn v-if="workflowHasTransition(props.row) && canViewTransition(props.row)" class="col" dense round flat color="grey" @click="editTransitionForm(props.row)" icon="assignment"></q-btn>
                    <q-btn v-if="canDeleteWorkflowInstance(props.row)" class="col" dense round flat color="grey" @click="showDeleteDialog(props.row)" icon="delete"></q-btn>
                  </div>
                </div>
              </q-item>
            </q-list>
          </q-card>
        </div>
      </template>
      <template v-slot:bottom-row>
        <q-tr @click="clickAddWorkflow('newEmployeeOnboarding')" class="cursor-pointer">
          <q-td colspan="100%">
            <q-icon name="add" size="md" class="q-pr-sm"/>New Position To Fill
          </q-td>
        </q-tr>
      </template>
    </q-table>

    <q-dialog v-model="deleteDialogVisible">
      <q-card>
        <q-card-section>
          <div class="row items-center">
            <q-avatar icon="insert_chart_outlined" color="primary" text-color="white" />
            <span class="q-ml-sm">Are you sure you want to delete this workflow?</span>
          </div>
          <div class="row justify-center text-center">Position: {{ deleteDialogPositionName }}</div>
          <div class="row justify-center text-center">{{ deleteDialogPercentComplete }}% Complete</div>
        </q-card-section>

        <q-card-actions class="row justify-around">
          <q-btn flat label="Cancel" color="primary" v-close-popup />
          <q-btn flat label="Yes, delete it" color="primary" @click="deleteRow()" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<style scoped>
.q-table tbody td.td-status {
    min-width: 135px;
    white-space: normal;
}
.q-table tbody td.wide-actions {
    min-width: 200px;
    white-space: normal;
}
</style>

<script setup lang="ts">
import { QTableProps, useQuasar } from 'quasar'
import { defineProps, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

import { WorkflowInstance } from 'src/types'

import { readableDate } from 'src/filters'
import { useUserStore } from 'src/stores/user'
import { useWorkflowsStore } from 'src/stores/workflows'

const quasar = useQuasar()
const router = useRouter()
const userStore = useUserStore()
const workflowsStore = useWorkflowsStore()

let deleteDialogVisible = ref(false)
let deleteDialogPositionName = ref('Not Set')
let deleteDialogPercentComplete = ref('0')
let rowPkToDelete = ref('')

const props = defineProps<{
  complete?: boolean,
  actionRequired?: boolean,
}>()

interface WorkflowColumn {
  name: string;
  required?: boolean;
  label: string;
  align?: string;
  field?: string;
  sortable?: boolean;
  style?: string;
  headerStyle?: string;
}

const columns: QTableProps['columns'] = [
  { name: 'position', label: 'Position', align: 'center', field: 'title' },
  { name: 'name', label: 'Name', align: 'center', field: 'employee_name' },
  { name: 'startedAt', align: 'center', label: 'Workflow Start Date', field: 'started_at', sortable: true },
  { name: 'transitionDate', align: 'center', label: 'Transition Date', field: 'transition_date', sortable: true },
  { name: 'percentComplete', align: 'center', label: '% Complete', field: 'percent_complete', sortable: true },
  { name: 'actions', label: 'Actions', align: 'center', field: null },
]

function workflows(): Array<WorkflowInstance> {
  if (props.actionRequired !== undefined && props.actionRequired) {
    return workflowsStore.workflowsActionRequired
  } else if (props.complete !== undefined) {
    if (props.complete) {
      return workflowsStore.workflowsComplete
    } else {
      return workflowsStore.workflowsIncomplete
    }
  } else {
    return workflowsStore.allWorkflows
  }
}

function noDataLabel(): string {
  if (props.actionRequired) {
    return 'Great work! All done here.'
  } else {
    return 'Nothing to show.'
  }
}

function retrieveWorkflows(): void {
  if (props.actionRequired) {
    workflowsStore.getWorkflows({actionRequired: true})
      .catch(e => {
        console.error('Error retrieving workflows with action required:', e)
      })
  } else if (props.complete == undefined) {
    workflowsStore.getWorkflows({})
      .catch(e => {
        console.error('Error retrieving all workflows:', e)
      })
  } else {
    if (props.complete) {
      workflowsStore.getWorkflows({complete: true})
        .catch(e => {
          console.error('Error retrieving complete workflows:', e)
        })
    } else {
      workflowsStore.getWorkflows({complete: false})
        .catch(e => {
          console.error('Error retrieving incomplete workflows:', e)
        })
    }
  }
}

function editWorkflowInstance(workflowInstance: WorkflowInstance): void {
  const rowPk = workflowInstance.pk.toString()
  router.push({name: 'workflow-processes', params: {pk: rowPk}})
    .catch(e => {
      console.error('Error navigating to workflow instance detail:', e)
    })
}

// TODO
function workflowHasTransition(): boolean {
  return true
}

// TODO
function canViewTransition(): boolean {
  return true
}

function editTransitionForm(workflowInstance: WorkflowInstance) {
  const rowPk = workflowInstance.pk.toString()
  router.push({name: 'workflow-transition-form', params: {pk: rowPk}} )
    .catch(e => {
      console.error('Error navigating to workflow transition form:', e)
    })
}

function canDeleteWorkflowInstance(workflowInstance: WorkflowInstance): boolean {
  if (workflowInstance.completed_at) {
    return false
  }
  if (userStore.getEmployeeProfile.is_all_workflows_admin) {
    // If they are an All-Workflows-Admin, allow delete
    return true
  } else if (workflowInstance.workflow.role) {
    // If they are an admin of the workflow, allow delete
    return userStore.getEmployeeProfile.workflow_roles.indexOf(workflowInstance.workflow.role) != -1
  } else {
    // TODO: What should happen if no role assigned? Only admins? Everyone? Require all steps to have roles?
    return false
  }
}

function showDeleteDialog(row: WorkflowInstance): void {
  rowPkToDelete.value = row.pk.toString()
  deleteDialogPositionName.value = row.title
  deleteDialogPercentComplete.value = row.percent_complete
  deleteDialogVisible.value = true;
}

function deleteRow(): void {
  workflowsStore.deleteWorkflowInstance(rowPkToDelete.value)
    .then(() => {
      quasar.notify('Deleted a workflow.')
      retrieveWorkflows()
    })
    .catch(e => {
      console.error('Error deleting workflow', e)
    })
}

// private editEvaluation(props: QuasarPerformanceReviewTableRowClickActionProps): void {
//   // this.$router.push(`pr/${ props.row.pk }`)
//   //   .catch(e => {
//   //     console.error('Error navigating to PR detail:', e)
//   //   })
// }

// private printEvaluation(props: QuasarPerformanceReviewTableRowClickActionProps): void {
//   // this.$router.push(`print/pr/${ props.row.pk }`)
//   //   .catch(e => {
//   //     console.error('Error printing PR:', e)
//   //   })
// }

// private printEvaluationPositionDescription(props: QuasarPerformanceReviewTableRowClickActionProps): void {
//   // window.location.href = props.row.signed_position_description
// }

function clickAddWorkflow(type: 'newEmployeeOnboarding' | 'newEmployeeOffboarding'): void {
  switch (type) {
    case 'newEmployeeOnboarding':
      workflowsStore.createNewEmployeeOnboarding()
        .then((response) => {
          router.push({name: 'workflow-transition-form', params: {pk: response.pk.toString()}})
            .catch(e => {
              console.error('Error navigating to new employee page', e)
            })
        })
        .catch(e => {
          console.error('Error creating a new employee onboarding workflow instance', e)
        })
      break
    case 'newEmployeeOffboarding':
      // TODO
      break
    default:
      break
  }
}

onMounted(() => {
  retrieveWorkflows()
})
</script>

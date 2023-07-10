<template>
  <div class="q-py-sm">
    <q-spinner-grid
        v-if="!workflowsLoaded"
        class="spinner q-mt-lg"
        color="primary"
        size="xl"
      />
    <q-table
      v-else
      :rows="workflows()"
      :columns="columns"
      :filter=tableFilter
      :filter-method=tableFilterMethod
      :grid="$q.screen.lt.md"
      no-data-label="Nothing to show"
      row-key="name"
      :rows-per-page-options="[0]"
    >
      <template v-slot:top-right>
        <q-input borderless dense clearable debounce="300" v-model="tableFilter" placeholder="Search">
          <template v-slot:prepend>
            <q-icon name="search">
              <q-tooltip>
                Type to search on Name, Description, Tag name, or Employee Name
              </q-tooltip>
            </q-icon>
          </template>
        </q-input>
      </template>
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
          <q-linear-progress rounded size="25px" :value="props.row.percent_complete/100" color="primary">
            <div class="absolute-full flex flex-center">
              <q-badge color="white" text-color="primary" :label="`${props.row.percent_complete}%`" />
            </div>
          </q-linear-progress>
      </q-td>
      </template>
      <template v-slot:body-cell-actions="props">
        <q-td key="actions" :props="props">
          <q-btn class="col" dense round flat color="grey" @click="editWorkflowInstance(props.row)" icon="play_arrow"></q-btn>
          <q-btn v-if="workflowHasTransition() && canViewTransition()" class="col" dense round flat color="grey" @click="editTransitionForm(props.row)" icon="assignment"></q-btn>
          <q-btn v-if="!archived && canDeleteWorkflowInstance(props.row)" class="col" dense round flat color="grey" @click="showArchiveDialog(props.row)" icon="delete"></q-btn>
          <q-btn v-if="archived && canDeleteWorkflowInstance(props.row)" class="col" dense round flat color="grey" @click="showArchiveDialog(props.row)" icon="restore_from_trash"></q-btn>
          <q-icon v-if="props.row.employee_action_required" color="orange" name="warning" size="md">
              <q-tooltip content-style="font-size: 16px">
                <div>Your action is required</div>
              </q-tooltip>
            </q-icon>
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
                  <div class="q-table__grid-item-value row q-gutter-sm" v-if="col.label == 'Actions'">
                    <q-btn class="col" dense round flat color="grey" @click="editWorkflowInstance(props.row)" icon="play_arrow"></q-btn>
                    <q-btn v-if="workflowHasTransition() && canViewTransition()" class="col" dense round flat color="grey" @click="editTransitionForm(props.row)" icon="assignment"></q-btn>
                    <q-btn v-if="!archived && canDeleteWorkflowInstance(props.row)" class="col" dense round flat color="grey" @click="showArchiveDialog(props.row)" icon="delete"></q-btn>
                    <q-btn v-if="archived && canDeleteWorkflowInstance(props.row)" class="col" dense round flat color="grey" @click="showArchiveDialog(props.row)" icon="restore_from_trash"></q-btn>
                    <q-icon v-if="props.row.employee_action_required" color="orange" name="warning" size="md">
                      <q-tooltip content-style="font-size: 16px">
                        <div>Your action is required</div>
                      </q-tooltip>
                    </q-icon>
                  </div>
                  <div class="q-table__grid-item-value" v-else-if="col.label.indexOf('Date') != -1">
                    {{ readableDate(col.value) }}
                  </div>
                  <div class="q-table__grid-item-value" v-else>
                    {{ col.value }}
                  </div>
                </div>
              </q-item>
            </q-list>
          </q-card>
        </div>
      </template>
      <template v-slot:bottom-row v-if="props.allowAddDelete">
        <q-tr @click="clickAddWorkflow()" class="cursor-pointer">
          <q-td colspan="100%">
            <q-icon name="add" size="md" class="q-pr-sm"/>New Workflow
          </q-td>
        </q-tr>
      </template>
    </q-table>

    <q-dialog v-model="deleteDialogVisible">
      <q-card>
        <q-card-section>
          <div class="row items-center">
            <q-avatar icon="insert_chart_outlined" color="primary" text-color="white" />
            <span class="q-ml-sm">Are you sure you want to <span v-if="!archived">delete</span><span v-else>restore</span> this workflow?</span>
          </div>
          <div class="row justify-center text-center">Position: {{ deleteDialogPositionName }}</div>
          <div class="row justify-center text-center">{{ deleteDialogPercentComplete }}% Complete</div>
        </q-card-section>

        <q-card-actions class="row justify-around">
          <q-btn flat label="Cancel" color="primary" v-close-popup />
          <q-btn v-if="!archived" flat label="Yes, delete it" color="primary" @click="deleteRow()" v-close-popup />
          <q-btn v-else flat label="Yes, restore it" color="primary" @click="restoreRow()" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<style lang="scss">
.q-table tbody td.td-status {
    min-width: 135px;
    white-space: normal;
}
.q-table tbody td.wide-actions {
    min-width: 200px;
    white-space: normal;
}
.q-table__bottom {
  display: none !important;
}
</style>

<script setup lang="ts">
import { QTableProps, useQuasar } from 'quasar'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import { WorkflowInstanceSimple } from 'src/types'

import { readableDate } from 'src/filters'
import { useUserStore } from 'src/stores/user'
import { useWorkflowsStore } from 'src/stores/workflows'

const quasar = useQuasar()
const router = useRouter()
const userStore = useUserStore()
const workflowsStore = useWorkflowsStore()

let workflowsLoaded = ref(true)

let deleteDialogVisible = ref(false)
let deleteDialogPositionName = ref('Not Set')
let deleteDialogPercentComplete = ref(0)
let rowPkToArchive = ref('')

const props = defineProps<{
  archived: boolean,
  complete: boolean,
  type: 'all' | 'new' | 'return' | 'change' | 'exit'
  allowAddDelete: boolean,
  // TODO: Move action required into the table as a column
  // actionRequired?: boolean,
}>()

const emit = defineEmits<{
  (e: 'retrieve'): void
}>()

const columns: QTableProps['columns'] = [
  { name: 'position', label: 'Position', align: 'center', field: 'title_name' },
  { name: 'name', label: 'Name', align: 'center', field: 'employee_name' },
  { name: 'startedAt', align: 'center', label: 'Workflow Start Date', field: 'started_at', sortable: true },
  { name: 'transitionDate', align: 'center', label: 'Transition Date', field: 'transition_date', sortable: true },
  { name: 'percentComplete', align: 'center', label: '% Complete', field: 'percent_complete', sortable: true },
  { name: 'actions', label: 'Actions', align: 'center', field: '' },
]

let tableFilter = ref('')

function tableFilterMethod(rows: readonly any[], term: string) {
  const tableRows = rows as WorkflowInstanceSimple[]
  const searchTerm = term ? term.toLowerCase() : ''
  const filteredRows = tableRows.filter(
    (row) => {
      if (searchTerm == '') {
          // If no search term, return all rows
          return true
      } else {
          const matchCriteria: Array<boolean> = []
          // Filter by name
          if (row.employee_name) {
            const nameMatches = row.employee_name.toLowerCase().includes(searchTerm)
            matchCriteria.push(nameMatches)
          }
          // Filter by position
          if (row.title_name) {
            const positionMatches = row.title_name.toLowerCase().includes(searchTerm)
            matchCriteria.push(positionMatches)
          }
          if (matchCriteria.some(c => !!c)) {
              return true
          }
          // Assume row doesn't match
          return false
      }
    })
  return filteredRows
}

function workflows(): Array<WorkflowInstanceSimple> {
  let workflows: Array<WorkflowInstanceSimple> = []
  if (props.archived) {
    workflows = workflowsStore.workflowsArchived
  } else if (props.complete) {
    workflows = workflowsStore.workflowsComplete
  } else {
    workflows = workflowsStore.workflowsIncomplete
  }
  return workflows.filter(
    (row) => {
      if (props.type == 'all') {
        return true
      } else {
        const matchCriteria: Array<boolean> = []
        // Filter by workflow type
        if (props.type == 'new') {
          const typeMatches = row.transition_type == 'New'
          matchCriteria.push(typeMatches)
        } else if (props.type == 'return') {
          const typeMatches = row.transition_type == 'Return'
          matchCriteria.push(typeMatches)
        } else if (props.type == 'change') {
          const typeMatches = row.transition_type == 'Change/Modify'
          matchCriteria.push(typeMatches)
        } else if (props.type == 'exit') {
          const typeMatches = row.transition_type == 'Exit'
          matchCriteria.push(typeMatches)
        }
        if (matchCriteria.some(c => !!c)) {
          return true
        }
        // Assume row doesn't match
        return false
      }
    }
  )
}

function editWorkflowInstance(workflowInstance: WorkflowInstanceSimple): void {
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

function editTransitionForm(workflowInstance: WorkflowInstanceSimple) {
  const rowPk = workflowInstance.pk.toString()
  router.push({name: 'workflow-transition-form', params: {pk: rowPk}} )
    .catch(e => {
      console.error('Error navigating to workflow transition form:', e)
    })
}

function canDeleteWorkflowInstance(workflowInstance: WorkflowInstanceSimple): boolean {
  if (workflowInstance.completed_at) {
    return false
  }
  if (userStore.getEmployeeProfile.is_all_workflows_admin) {
    // If they are an All-Workflows-Admin, allow delete
    return true
  } else if (workflowInstance.workflow_role_pk) {
    // If they are an admin of the workflow, allow delete
    return userStore.getEmployeeProfile.workflow_roles.indexOf(workflowInstance.workflow_role_pk) != -1
  } else {
    // TODO: What should happen if no role assigned? Only admins? Everyone? Require all steps to have roles?
    return false
  }
}

function showArchiveDialog(row: WorkflowInstanceSimple): void {
  rowPkToArchive.value = row.pk.toString()
  deleteDialogPositionName.value = row.title_name
  deleteDialogPercentComplete.value = row.percent_complete
  deleteDialogVisible.value = true
}

function deleteRow(): void {
  workflowsStore.archiveWorkflowInstance(rowPkToArchive.value)
    .then(() => {
      quasar.notify('Deleted a workflow.')
      emit('retrieve')
    })
    .catch(e => {
      console.error('Error deleting workflow', e)
    })
}

function restoreRow(): void {
  workflowsStore.restoreWorkflowInstance(rowPkToArchive.value)
    .then(() => {
      quasar.notify('Restored a workflow.')
      emit('retrieve')
    })
    .catch(e => {
      console.error('Error restoring workflow', e)
    })
}

function clickAddWorkflow(): void {
  switch (props.type) {
    case 'all':
    case 'new':
      workflowsStore.createNewEmployeeOnboarding()
        .then((wfi) => {
          navigateToWorkflowTransitionForm(wfi.pk)
        })
        .catch(e => {
          console.error('Error creating a new employee onboarding workflow instance', e)
        })
      break
    case 'return':
      workflowsStore.createNewEmployeeReturning()
        .then((wfi) => {
          navigateToWorkflowTransitionForm(wfi.pk)
        })
        .catch(e => {
          console.error('Error creating a new employee onboarding workflow instance', e)
        })
      break
    case 'change':
      workflowsStore.createNewEmployeeChanging()
        .then((wfi) => {
          navigateToWorkflowTransitionForm(wfi.pk)
        })
        .catch(e => {
          console.error('Error creating a new employee onboarding workflow instance', e)
        })
      break
    case 'exit':
      workflowsStore.createNewEmployeeExiting()
        .then((wfi) => {
          navigateToWorkflowTransitionForm(wfi.pk)
        })
        .catch(e => {
          console.error('Error creating a new employee onboarding workflow instance', e)
        })
      break
    default:
      break
  }

  function navigateToWorkflowTransitionForm(pk: number): void {
    router.push({name: 'workflow-transition-form', params: {pk: pk.toString()}})
      .catch(e => {
        console.error('Error navigating to workflow transition form:', e)
      })
  }
}
</script>

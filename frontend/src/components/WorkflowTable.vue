<template>
  <div class="q-py-sm">
    <q-table
      :data="workflows()"
      :columns="columns()"
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
          {{ props.row.started_at | readableDate }}
        </q-td>
      </template>
      <template v-slot:body-cell-transitionDate="props">
        <q-td key="transitionDate" :props="props">
          {{ props.row.transition_date | readableDate }}
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

<script lang="ts">
import { Notify } from 'quasar'
import { Component, Prop, Vue } from 'vue-property-decorator'
import WorkflowInstanceDataService from '../services/WorkflowInstanceDataService';
import { WorkflowInstance } from '../store/types'
import '../filters'

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

@Component
export default class WorkflowTable extends Vue {
  @Prop() readonly complete!: boolean
  @Prop() readonly actionRequired!: boolean
  public workflows(): Array<WorkflowInstance> {
    if (this.actionRequired !== undefined && this.actionRequired) {
      return this.$store.getters['workflowModule/workflowsActionRequired'].results // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-return
    } else if (this.complete !== undefined) {
      if (this.complete) {
        return this.$store.getters['workflowModule/workflowsComplete'].results // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-return
      } else {
        return this.$store.getters['workflowModule/workflowsIncomplete'].results // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-return
      }
    } else {
      return this.$store.getters['workflowModule/allWorkflows'].results // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-return
    }
  }
  public columns(): Array<WorkflowColumn> {
    return [
      { name: 'position', label: 'Position', align: 'center', field: 'title' },
      { name: 'name', label: 'Name', align: 'center', field: 'employee_name' },
      { name: 'startedAt', align: 'center', label: 'Workflow Start Date', field: 'started_at', sortable: true },
      { name: 'transitionDate', align: 'center', label: 'Transition Date', field: 'transition_date', sortable: true },
      { name: 'percentComplete', align: 'center', label: '% Complete', field: 'percent_complete', sortable: true },
      { name: 'actions', label: 'Actions', align: 'center' },
    ]
  }

  public noDataLabel(): string {
    if (this.actionRequired) {
      return 'Great work! All done here.'
    } else {
      return 'Nothing to show.'
    }
  }

  public deleteDialogVisible = false
  private deleteDialogPositionName = 'Not Set'
  private deleteDialogPercentComplete = '0'
  private rowPkToDelete = ''

  private retrieveWorkflows(): void {
    if (this.actionRequired) {
      this.$store.dispatch('workflowModule/getWorkflows', {actionRequired: true})
        .catch(e => {
          console.error('Error retrieving workflows with action required:', e)
        })
    } else if (this.complete == undefined) {
      this.$store.dispatch('workflowModule/getWorkflows')
        .catch(e => {
          console.error('Error retrieving all workflows:', e)
        })
    } else {
      if (this.complete) {
        this.$store.dispatch('workflowModule/getWorkflows', {complete: true})
          .catch(e => {
            console.error('Error retrieving complete workflows:', e)
          })
      } else {
        this.$store.dispatch('workflowModule/getWorkflows', {complete: false})
          .catch(e => {
            console.error('Error retrieving incomplete workflows:', e)
          })
      }
    }
  }

  public editWorkflowInstance(workflowInstance: WorkflowInstance): void {
    const rowPk = workflowInstance.pk.toString()
    this.$router.push({name: 'workflow-processes', params: {pk: rowPk}})
      .catch(e => {
        console.error('Error navigating to workflow instance detail:', e)
      })
  }

  public workflowHasTransition(workflowInstance: WorkflowInstance): boolean {
    return true
  }

  public canViewTransition(workflowInstance: WorkflowInstance): boolean {
    return true
  }

  public editTransitionForm(workflowInstance: WorkflowInstance) {
    const rowPk = workflowInstance.pk.toString()
    this.$router.push({name: 'workflow-transition-form', params: {pk: rowPk}} )
      .catch(e => {
        console.error('Error navigating to workflow transition form:', e)
      })
  }

  public canDeleteWorkflowInstance(workflowInstance: WorkflowInstance): boolean {
    if (workflowInstance.completed_at) {
      return false
    }
    if (this.$store.getters['userModule/getEmployeeProfile'].is_all_workflows_admin) {
      // If they are an All-Workflows-Admin, allow delete
      return true
    } else if (workflowInstance.workflow.role) {
      // If they are an admin of the workflow, allow delete
      return this.$store.getters['userModule/getEmployeeProfile'].workflow_roles.indexOf(workflowInstance.workflow.role) != -1
    } else {
      // TODO: What should happen if no role assigned? Only admins? Everyone? Require all steps to have roles?
      return false
    }
  }

  public showDeleteDialog(row: WorkflowInstance): void {
    this.rowPkToDelete = row.pk.toString()
    this.deleteDialogPositionName = row.title
    this.deleteDialogPercentComplete = row.percent_complete
    this.deleteDialogVisible = true;
  }

  public deleteRow(): void {
    WorkflowInstanceDataService.delete(this.rowPkToDelete)
      .then(() => {
        Notify.create('Deleted a workflow.')
        this.retrieveWorkflows()
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

  public clickAddWorkflow(type: 'newEmployeeOnboarding' | 'newEmployeeOffboarding'): void {
    switch (type) {
      case 'newEmployeeOnboarding':
        this.$store.dispatch('workflowModule/createNewEmployeeOnboarding')
          .then((workflowInstance) => {
            this.$router.push({name: 'workflow-transition-form', params: {pk: workflowInstance.data.pk}})
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

  mounted() {
    this.retrieveWorkflows();
  }
}
</script>

<template>
  <div class="q-py-sm">
    <q-table
      :rows="performanceReviews()"
      :columns="columns()"
      :dense="$q.screen.lt.lg"
      :grid="$q.screen.lt.md"
      :no-data-label="noDataLabel()"
      row-key="name"
    >
      <!-- Slots for body cells: Show dates in a familiar format; make sure
        status can wrap, and display action buttons -->
      <template v-slot:body-cell-performancePeriod="props">
        <q-td key="performancePeriod" :props="props">
          {{ readableDate(props.row.period_start_date) }} -
          {{ readableDate(props.row.period_end_date) }}
        </q-td>
      </template>
      <template v-slot:body-cell-status="props">
        <q-td style="white-space: normal;" :props="props">
          {{ props.row.status }}
        </q-td>
      </template>
      <template v-slot:body-cell-actions="props">
        <q-td :props="props">
          <div class="row">
            <q-btn
              class="col edit-button"
              dense
              round
              flat
              color="grey"
              @click="editEvaluation(props)"
              icon="edit"
            />
            <q-btn
              class="col print-button"
              dense
              round
              flat
              color="grey"
              @click="printEvaluation(props)"
              icon="print"
            >
              <q-tooltip content-style="font-size: 16px">
                Print Performance Review Form
              </q-tooltip>
            </q-btn>
            <q-btn
              v-if="props.row.signed_position_description"
              class="col print-button"
              dense
              round
              flat
              color="grey"
              @click="printEvaluationPositionDescription(props)"
              icon="print"
            >
              <q-tooltip content-style="font-size: 16px">
                Print Signed Position Description
              </q-tooltip>
            </q-btn>
          </div>
        </q-td>
      </template>
      <!-- For grid mode, we need to specify everything in order for our action
        buttons to render -->
      <template v-slot:item="props">
        <div
          class="q-pa-xs col-xs-12 col-sm-6 col-md-4 col-lg-3
            grid-style-transition"
        >
          <q-card class="q-py-sm">
            <q-list dense>
              <q-item v-for="col in props.cols" :key="col.name">
                <div class="q-table__grid-item-row">
                  <div class="q-table__grid-item-title">{{ col.label }}</div>
                  <div
                    class="q-table__grid-item-value"
                    v-if="col.label != 'Actions'"
                  >
                    {{ col.value }}
                  </div>
                  <div class="q-table__grid-item-value row q-gutter-sm" v-else>
                    <q-btn
                      class="col edit-button"
                      dense
                      round
                      flat
                      color="grey"
                      @click="editEvaluation(props)"
                      icon="edit"
                    />
                    <q-btn
                      class="col print-button"
                      dense
                      round
                      flat
                      color="grey"
                      @click="printEvaluation(props)"
                      icon="print"
                    >
                      <q-tooltip content-style="font-size: 16px">
                        Print Performance Review Form
                      </q-tooltip>
                    </q-btn>
                    <q-btn
                      v-if="props.row.signed_position_description"
                      class="col print-button"
                      dense
                      round
                      flat
                      color="grey"
                      @click="printEvaluationPositionDescription(props)"
                      icon="print"
                    >
                      <q-tooltip content-style="font-size: 16px">
                        Print Signed Position Description
                      </q-tooltip>
                    </q-btn>
                  </div>
                </div>
              </q-item>
            </q-list>
          </q-card>
        </div>
      </template>
    </q-table>
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
</style>

<script setup lang="ts">
import { QTable, QTableProps } from 'quasar'
import { onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'

import useEventBus from 'src/eventBus'
import { readableDate } from 'src/filters'
import { usePerformanceReviewStore } from 'src/stores/performancereview'
import { PerformanceReviewRetrieve } from 'src/types'

interface QuasarPerformanceReviewTableRowClickActionProps {
  evt: MouseEvent;
  row: PerformanceReviewRetrieve;
}

const props = defineProps<{
  signature?: boolean,
  actionRequired: boolean
}>()

const router = useRouter()
const { bus } = useEventBus()
const performanceReviewStore = usePerformanceReviewStore()

function performanceReviews(): Array<PerformanceReviewRetrieve> {
  let prs = []
  if (props.signature) {
    if (props.actionRequired) {
      prs = performanceReviewStore.allSignaturePerformanceReviewsActionRequired
      // return this.$store.getters['performanceReviewModule/allSignaturePerformanceReviewsActionRequired'].results // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-return
    } else {
      prs = performanceReviewStore.allSignaturePerformanceReviewsActionNotRequired
      // return this.$store.getters['performanceReviewModule/allSignaturePerformanceReviewsActionNotRequired'].results // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-return
    }
  } else {
    if (props.actionRequired) {
      prs = performanceReviewStore.allPerformanceReviewsActionRequired
      // return this.$store.getters['performanceReviewModule/allPerformanceReviewsActionRequired'].results // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-return
    } else {
      prs = performanceReviewStore.allPerformanceReviewsActionNotRequired
      // return this.$store.getters['performanceReviewModule/allPerformanceReviewsActionNotRequired'].results // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-return
    }
  }
  return prs.sort((a, b) => {
    return a.days_until_review - b.days_until_review
  })
}

function columns(): QTableProps['columns'] {
  if (props.signature) {
    return [
      { name: 'employeeName', label: 'Employee', align: 'center', field: 'employee_name', sortable: true },
      { name: 'managerName', label: 'Manager', align: 'center', field: 'manager_name', sortable: true },
      { name: 'performancePeriod', align: 'center', label: 'Performance Period', field: 'performance_period' },
      { name: 'daysUntilReview', align: 'center', label: 'Days Until Review', field: 'days_until_review', sortable: true },
      { name: 'status', align: 'center', label: 'Status', field: 'status', sortable: true },
      { name: 'actions', label: 'Actions', align: 'around', },
    ]
  } else {
    return [
      { name: 'employeeName', label: 'Employee', align: 'center', field: 'employee_name', sortable: true },
      { name: 'performancePeriod', align: 'center', label: 'Performance Period', field: 'performance_period' },
      { name: 'daysUntilReview', align: 'center', label: 'Days Until Review', field: 'days_until_review', sortable: true },
      { name: 'status', align: 'center', label: 'Status', field: 'status', sortable: true },
      { name: 'actions', label: 'Actions', align: 'around', },
    ]
  }
}

function noDataLabel(): string {
  if (props.actionRequired) {
    return 'Great work! All done here.'
  } else {
    return 'Nothing to show.'
  }
}

function retrievePerformanceReviews(): void {
  if (props.signature) {
    if (props.actionRequired) {
      performanceReviewStore.getAllSignaturePerformanceReviewsActionRequired()
        .catch(e => {
          console.error(
            'Error retrieving getAllSignaturePerformanceReviewsActionRequired:',
            e
          )
        })
    } else {
      performanceReviewStore.getAllSignaturePerformanceReviewsActionNotRequired()
        .catch(e => {
          console.error(
            'Error retrieving getAllSignaturePerformanceReviewsActionNotRequired:',
            e
          )
        })
    }
  } else {
    if (props.actionRequired) {
      performanceReviewStore.getAllPerformanceReviewsActionRequired()
        .catch(e => {
          console.error(
            'Error retrieving getAllPerformanceReviewsActionRequired:', e
          )
        })
    } else {
      performanceReviewStore.getAllPerformanceReviewsActionNotRequired()
        .catch(e => {
          console.error(
            'Error retrieving getAllPerformanceReviewsActionNotRequired:', e
          )
        })
    }
  }
}

function editEvaluation(props: QuasarPerformanceReviewTableRowClickActionProps): void {
  router.push(`pr/${ props.row.pk }`)
    .catch(e => {
      console.error('Error navigating to PR detail:', e)
    })
}

function printEvaluation(props: QuasarPerformanceReviewTableRowClickActionProps): void {
  router.push(`print/pr/${ props.row.pk }`)
    .catch(e => {
      console.error('Error printing PR:', e)
    })
}

function printEvaluationPositionDescription(props: QuasarPerformanceReviewTableRowClickActionProps): void {
  window.location.href = props.row.signed_position_description
}

watch(() => bus.value.get('updateTeleworkApplicationTables'), () => {
  retrievePerformanceReviews()
})

onMounted(() => {
  retrievePerformanceReviews();
})

</script>

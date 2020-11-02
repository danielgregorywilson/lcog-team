<template>
  <div class="q-py-sm">
    <q-table
      :data="performanceReviews()"
      :columns="columns()"
      :dense="$q.screen.lt.lg"
      :grid="$q.screen.lt.md"
      :no-data-label="noDataLabel()"
      row-key="name"
    >
      <!-- Slots for header cells: Shrink the width when the screen is too small to see the whole table width -->
      <template v-slot:header-cell-employeeName="props">
        <th v-if="$q.screen.lt.lg" style="white-space: normal;">{{props.col.label}}</th>
        <th v-else>{{props.col.label}}</th>
      </template>
      <template v-slot:header-cell-daysUntilReview="props">
        <th v-if="$q.screen.lt.lg" style="white-space: normal;">{{props.col.label}}</th>
        <th v-else>{{props.col.label}}</th>
      </template>
      <!-- Slots for body cells: Show dates in a familiar format; make sure status can wrap, and display action buttons -->
      <template v-slot:body-cell-dateOfReview="props">
        <q-td key="dateOfReview" :props="props">
          {{ props.row.date_of_review | readableDate }}
        </q-td>
      </template>
      <template v-slot:body-cell-status="props">
        <q-td style="white-space: normal;" :props="props">{{ props.row.status }}</q-td>
      </template>
      <template v-slot:body-cell-actions="props">
        <q-td :props="props">
          <div class="row">
            <q-btn class="col" dense round flat color="grey" @click="editEvaluation(props)" icon="edit"></q-btn>
          </div>
        </q-td>
      </template>
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
                    <q-btn class="col" dense round flat color="grey" @click="editEvaluation(props)" icon="edit"></q-btn>
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
import { Component, Prop, Vue } from 'vue-property-decorator'
import { ReviewNoteRetrieve } from '../store/types'
import { bus } from '../App.vue'
import { PerformanceReviewRetrieve } from '../store/types'
import '../filters'

interface EvaluationColumn {
  name: string;
  required?: boolean;
  label: string;
  align?: string;
  field?: string;
  sortable?: boolean;
  style?: string;
  headerStyle?: string;
}

interface QuasarPerformanceReviewTableRowClickActionProps {
  evt: MouseEvent;
  row: PerformanceReviewRetrieve;
}

@Component
export default class PerformanceReviewTable extends Vue {
  @Prop() readonly upperManager!: boolean
  @Prop({required: true}) readonly actionRequired!: boolean
  private performanceReviews(): Array<ReviewNoteRetrieve> {
    if (this.upperManager) {
      if (this.actionRequired) {
        return this.$store.getters['performanceReviewModule/allUpperManagerPerformanceReviewsActionRequired'].results // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-return
      } else {
        return this.$store.getters['performanceReviewModule/allUpperManagerPerformanceReviewsActionNotRequired'].results // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-return
      }
    } else {
      if (this.actionRequired) {
        return this.$store.getters['performanceReviewModule/allPerformanceReviewsActionRequired'].results // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-return
      } else {
        return this.$store.getters['performanceReviewModule/allPerformanceReviewsActionNotRequired'].results // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-return
      }
    }
  }
  private columns(): Array<EvaluationColumn> {
    if (this.upperManager) {
      return [
        { name: 'employeeName', label: 'Employee Name', align: 'center', field: 'employee_name', sortable: true },
        { name: 'managerName', label: 'Manager Name', align: 'center', field: 'manager_name', sortable: true },
        { name: 'dateOfReview', align: 'center', label: 'Date of Review', field: 'date_of_review', sortable: true },
        { name: 'daysUntilReview', align: 'center', label: 'Days Until Review', field: 'days_until_review', sortable: true },
        { name: 'status', align: 'center', label: 'Status', field: 'status' },
        { name: 'actions', label: 'Actions', align: 'around', },
      ]
    } else {
      return [
        { name: 'employeeName', label: 'Employee Name', align: 'center', field: 'employee_name', sortable: true },
        { name: 'dateOfReview', align: 'center', label: 'Date of Review', field: 'date_of_review', sortable: true },
        { name: 'daysUntilReview', align: 'center', label: 'Days Until Review', field: 'days_until_review', sortable: true },
        { name: 'status', align: 'center', label: 'Status', field: 'status' },
        { name: 'actions', label: 'Actions', align: 'around', },
      ]
    }
  }

  private noDataLabel(): string {
    if (this.actionRequired) {
      return 'Great work! All done here.'
    } else {
      return 'Nothing to show.'
    }
  }

  private retrievePerformanceReviews(): void {
    if (this.upperManager) {
      if (this.actionRequired) {
        this.$store.dispatch('performanceReviewModule/getAllUpperManagerPerformanceReviewsActionRequired')
        .catch(e => {
          console.log(e)
        })
      } else {
        this.$store.dispatch('performanceReviewModule/getAllUpperManagerPerformanceReviewsActionNotRequired')
        .catch(e => {
          console.log(e)
        })
      }
    } else {
      if (this.actionRequired) {
        this.$store.dispatch('performanceReviewModule/getAllPerformanceReviewsActionRequired')
        .catch(e => {
          console.log(e)
        })
      } else {
        this.$store.dispatch('performanceReviewModule/getAllPerformanceReviewsActionNotRequired')
        .catch(e => {
          console.log(e)
        })
      }
    }
  }

  private editEvaluation(props: QuasarPerformanceReviewTableRowClickActionProps): void {
    this.$router.push(`pr/${ props.row.pk }`)
      .catch(e => {
        console.log(e)
      })
  }

  created() {
    bus.$on('updatePerformanceReviewTables', (data: string) => { // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-call
      console.log(data)
      this.retrievePerformanceReviews()
    })
  }

  mounted() {
    this.retrievePerformanceReviews();
    // TODO: Was only loading them once, but we need to update them if changes have occurred
    // if (this.performanceReviews() == undefined) {
    //   this.retrievePerformanceReviews();
    // }
  }
}
</script>

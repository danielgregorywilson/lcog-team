<template>
  <div class="q-py-sm">
    <q-table
      :data="performanceReviews()"
      :columns="columns"
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
      <template v-slot:header-cell-dateOfDiscussion="props">
        <th v-if="$q.screen.lt.lg" style="white-space: normal;">{{props.col.label}}</th>
        <th v-else>{{props.col.label}}</th>
      </template>
      <template v-slot:header-cell-discussionTookPlace="props">
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
      <template v-slot:body-cell-dateOfDiscussion="props">
        <q-td key="dateOfDiscussion" :props="props" >
          {{ props.row.date_of_discussion | readableDate }}
        </q-td>
      </template>
      <template v-slot:body-cell-actions="props">
        <q-td :props="props" :class="{ 'wide-actions' : props.row.discussion_took_place == 'No'}">
          <div class="row">
            <q-btn class="col" dense round flat color="grey" @click="editEvaluation(props)" icon="edit"></q-btn>
            <q-btn class="col" v-if="props.row.discussion_took_place=='No'" color="white" text-color="black" label="Mark as Discussed" @click="managerMarkDiscussed(props)" />
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
                    <q-btn class="col" v-if="props.row.discussion_took_place=='No'" color="white" text-color="black" label="Mark as Discussed" @click="managerMarkDiscussed(props)" />
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
import { AxiosPerformanceReviewManagerMarkDiscussedServerResponse, ReviewNoteRetrieve } from '../store/types'
import { bus } from '../App.vue'
import PerformanceReviewDataService from '../services/PerformanceReviewDataService';
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

interface QuasarEvaluationTableRowClickActionProps {
  evt: MouseEvent;
  row: PerformanceReviewRetrieve;
}

@Component
export default class EvaluationTable extends Vue {
  @Prop({required: true}) readonly actionRequired!: boolean
  private performanceReviews(): Array<ReviewNoteRetrieve> {
    if (this.actionRequired) {
      return this.$store.getters['performanceReviewModule/allPerformanceReviewsActionRequired'].results // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-return
    } else {
      return this.$store.getters['performanceReviewModule/allPerformanceReviewsActionNotRequired'].results // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-return
    }
  }
  private columns: Array<EvaluationColumn> = [
    { name: 'employeeName', required: true, label: 'Employee Name', align: 'center', field: 'employee_name', sortable: true },
    { name: 'dateOfReview', align: 'center', label: 'Date of Review', field: 'date_of_review', sortable: true },
    { name: 'daysUntilReview', align: 'center', label: 'Days Until Review', field: 'days_until_review', sortable: true },
    { name: 'status', align: 'center', label: 'Status', field: 'status' },
    { name: 'dateOfDiscussion', align: 'center', label: 'Date of Discussion', field: 'date_of_discussion' },
    { name: 'discussionTookPlace', align: 'center', label: 'Discussion took place', field: 'discussion_took_place' },
    { name: 'actions', label: 'Actions', align: 'around', },
  ]

  private noDataLabel(): string {
    if (this.actionRequired) {
      return "Great work! All done here."
    } else {
      return "Nothing to show."
    }
  }

  private retrievePerformanceReviews(): void {
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

  private editEvaluation(props: QuasarEvaluationTableRowClickActionProps): void {
    this.$router.push(`pr/${ props.row.pk }`)
      .catch(e => {
        console.log(e)
      })
  }

  private managerMarkDiscussed(props: QuasarEvaluationTableRowClickActionProps): void {
    PerformanceReviewDataService.managerMarkDiscussed(props.row.pk)
      .then((response: AxiosPerformanceReviewManagerMarkDiscussedServerResponse) => {
        console.log(response.data.status)
        bus.$emit('updateEvaluationTables', 'updated table') // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-call
      })
      .catch(e => {
        console.log(e)
      })
  }

  created() {
    bus.$on('updateEvaluationTables', (data: string) => { // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-call
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

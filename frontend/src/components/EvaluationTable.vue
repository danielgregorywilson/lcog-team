<template>
  <div class="q-py-sm">
    <q-table
      :data="performanceReviews"
      :columns="columns"
      row-key="name"
    >
      <template v-slot:body-cell-dateOfReview="props">
        <q-td key="dateOfReview" :props="props">
          {{ new Date(props.row.date_of_review).toLocaleDateString() }}
        </q-td>
      </template>
      <template v-slot:body-cell-status="props">
        <q-td key="status" :props="props">
          {{ props.row.status }}
        </q-td>
      </template>
      <template v-slot:body-cell-dateOfDiscussion="props">
        <q-td key="dateOfDiscussion" :props="props" >
          {{ new Date(props.row.date_of_discussion).toLocaleDateString('en-us') + new Date(props.row.date_of_discussion).getTimezoneOffset() * 60000 }}
          <!-- {{ new Date(props.row.date_of_discussion).getTimezoneOffset() }} -->
        </q-td>
      </template>
      <template v-slot:body-cell-actions="props">
        <q-td :props="props">
          <q-btn dense round flat color="grey" @click="editEvaluation(props)" icon="edit"></q-btn>
        </q-td>
      </template>
    </q-table>
  </div>
</template>

<style scoped>
.q-table tbody td {
    min-width: 135px;
    white-space: normal;
}
</style>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'

import { AxiosPerformanceReviewRetrieveManyServerResponse } from '../store/types'

import PerformanceReviewDataService from '../services/PerformanceReviewDataService';

import { PerformanceReviewRetrieve } from '../store/types'

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
  private performanceReviews: Array<PerformanceReviewRetrieve> = []
  private columns: Array<EvaluationColumn> = [
    { name: 'employeeName', required: true, label: 'Employee Name', align: 'left', field: 'employee_name', sortable: true },
    { name: 'dateOfReview', align: 'center', label: 'Date of Review', field: 'date_of_review', sortable: true },
    { name: 'daysUntilReview', label: 'Days Until Review', field: 'days_until_review', sortable: true },
    { name: 'status', label: 'Status', field: 'status' },
    { name: 'dateOfDiscussion', label: 'Date of Discussion', field: 'date_of_discussion' },
    { name: 'discussionTookPlace', label: 'Discussion took place', field: 'discussion_took_place' },
    { name: 'actions', label: 'Actions' },
  ]
  public retrievePerformanceReviews(): void {
    if (this.actionRequired) {
      PerformanceReviewDataService.getAllManagerUpcomingActionRequired()
        .then((response: AxiosPerformanceReviewRetrieveManyServerResponse) => {
          this.performanceReviews = response.data.results;
        })
        .catch(e => {
          console.log(e);
        });
    } else {
      PerformanceReviewDataService.getAllManagerUpcomingNoActionRequired()
        .then((response: AxiosPerformanceReviewRetrieveManyServerResponse) => {
          this.performanceReviews = response.data.results;
        })
        .catch(e => {
          console.log(e);
        });
    }
  }

  private editEvaluation(props: QuasarEvaluationTableRowClickActionProps): void {
    this.$router.push(`pr/${ props.row.pk }`)
      .catch(e => {
        console.log(e)
      })
  }

  mounted() {
    this.retrievePerformanceReviews();
  }
}
</script>

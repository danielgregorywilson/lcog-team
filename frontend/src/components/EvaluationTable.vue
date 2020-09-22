<template>
  <div class="q-py-sm">
    <q-table
      :data="performanceReviews"
      :columns="columns"
      row-key="name"
      @row-click="onRowClick"
    >
    </q-table>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'

import PerformanceReviewDataService from '../services/PerformanceReviewDataService';

import { PerformanceReview } from '../store/types'

interface EvaluationColumn {
  name: string,
  required?: boolean,
  label: string,
  align?: string,
  field?: string,
  sortable?: boolean
}

@Component
export default class EvaluationTable extends Vue {
  @Prop({required: true}) readonly actionRequired!: boolean
  private performanceReviews: Array<PerformanceReview> = []
  private columns: Array<EvaluationColumn> = [
    { name: 'employeeName', required: true, label: 'Employee Name', align: 'left', field: 'employee_name', sortable: true },
    { name: 'dateOfReview', align: 'center', label: 'Date of Review', field: 'date_of_review', sortable: true },
    { name: 'daysUntilReview', label: 'Days Until Review', field: 'days_until_review', sortable: true },
    { name: 'status', label: 'Status', field: 'status' },
    { name: 'dateOfDiscussion', label: 'Date of Discussion', field: 'date_of_discussion' },
    { name: 'discussionTookPlace', label: 'Discussion took place', field: 'discussion_took_place' }
  ]
  public retrievePerformanceReviews(): void {
    if (this.actionRequired) {
      PerformanceReviewDataService.getAllManagerUpcomingActionRequired()
        .then(response => {
          this.performanceReviews = response.data.results; // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-assignment
        })
        .catch(e => {
          console.log(e);
        });
    } else {
      PerformanceReviewDataService.getAllManagerUpcomingNoActionRequired()
        .then(response => {
          this.performanceReviews = response.data.results; // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-assignment
        })
        .catch(e => {
          console.log(e);
        });
    }
  }
  public onRowClick(evt: MouseEvent, row: PerformanceReview): void {
    this.$router.push(`pr/${ row.pk }`)
      .catch(e => {
        console.log(e)
      })
  }
  mounted() {
    this.retrievePerformanceReviews();
  }
}
</script>

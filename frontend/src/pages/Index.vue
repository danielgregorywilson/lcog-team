<template>
  <q-page class="q-pa-md">
    <div class="q-py-md">
      <div class="text-h4">Your Next Review</div>
      <div class="text-body1">You do not have a scheduled upcoming review</div>
    </div>
    <div class="q-py-md">
      <div class="text-h4">Review Notes</div>
      <review-note-table />
    </div>
    <div class="q-py-md">
      <div class="text-h4">Current Evaluations (For Managers)</div>
      <div class="text-h6">Action Required</div>
        <q-table
            :data="prsActionRequired"
            :columns="evaluations_columns"
            row-key="name"
          />
      <div class="text-h6">No Action Required</div>
        <q-table
            :data="prsNoActionRequired"
            :columns="evaluations_columns"
            row-key="name"
          />
    </div>
  </q-page>
</template>

<script lang="ts">
import { defineComponent } from '@vue/composition-api';

import ExampleComponent from '../components/CompositionComponent.vue';
import ReviewNoteTable from '../components/ReviewNoteTable.vue';

import PerformanceReviewDataService from '../services/PerformanceReviewDataService';

import { PerformanceReview } from '../store/types';


interface EvaluationColumn {
  name: string,
  required?: boolean,
  label: string,
  align?: string,
  field: string,
  sortable?: boolean
}

interface ComponentData {
  prsActionRequired: Array<PerformanceReview>
  prsNoActionRequired: Array<PerformanceReview>
  currentIndex: number
  title: string
  evaluations_columns: Array<EvaluationColumn>
}

export default defineComponent({
  name: 'PageIndex',
  components: { ExampleComponent, ReviewNoteTable },
  data(): ComponentData {
    return {
      prsActionRequired: [],
      prsNoActionRequired: [],
      currentIndex: -1,
      title: '',
      evaluations_columns: [
        {
          name: 'employeeName',
          required: true,
          label: 'Employee Name',
          align: 'left',
          field: 'employee_name',
          sortable: true
        },
        { name: 'dateOfReview', align: 'center', label: 'Date of Review', field: 'date_of_review', sortable: true },
        { name: 'daysUntilReview', label: 'Days Until Review', field: 'days_until_review', sortable: true },
        { name: 'status', label: 'Status', field: 'status' },
        { name: 'dateOfDiscussion', label: 'Date of Discussion', field: 'date_of_discussion' },
        { name: 'discussionTookPlace', label: 'Discussion took place', field: 'discussion_took_place' }
      ],
    };
  },
  computed: {

  },
  methods: {
    retrievePerformanceReviews() {
      PerformanceReviewDataService.getAllManagerUpcomingActionRequired()
        .then(response => {
          this.prsActionRequired = response.data.results; // eslint-disable-line @typescript-eslint/no-unsafe-member-access
        })
        .catch(e => {
          console.log(e);
        });
      PerformanceReviewDataService.getAllManagerUpcomingNoActionRequired()
        .then(response => {
          this.prsNoActionRequired = response.data.results; // eslint-disable-line @typescript-eslint/no-unsafe-member-access
        })
        .catch(e => {
          console.log(e);
        });
    },
  },
  mounted() {
    this.retrievePerformanceReviews();
  },
  setup() {
    return {  };
  }
});
</script>

<template>
  <q-page class="q-pa-md">
    <div class="q-py-md">
      <div class="text-h4">Your Next Review</div>
      <div class="text-body1">You do not have a scheduled upcoming review</div>
    </div>
    <div class="q-py-md">
      <div class="text-h4">Review Notes</div>
      <div class="q-py-sm">
        <q-table
          :data="reviewNotes.results"
          :columns="reviewNotesColumns"
          row-key="name"
        />
      </div>
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

import PerformanceReviewDataService from '../services/PerformanceReviewDataService';
import ReveiwNoteService from '../services/ReviewNoteDataService';


export default defineComponent({
  name: 'PageIndex',
  components: { ExampleComponent },
  data() {
    return {
      reviewNotes: [],
      prsActionRequired: [],
      prsNoActionRequired: [],
      currentIndex: -1,
      title: '',
      reviewNotesColumns: [
        {
          name: 'employeeName',
          required: true,
          label: 'Employee Name',
          align: 'left',
          field: 'employee_name',
          sortable: true
        },
        { name: 'date', label: 'Date', field: 'date', sortable: true },
        { name: 'delete', label: 'Delete?' },
      ],
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
      ReveiwNoteService.getAll()
        .then(response => {
          this.reviewNotes = response.data;
          console.log(response.data);
        })
        .catch(e => {
          console.log(e);
        });
      PerformanceReviewDataService.getAllManagerUpcomingActionRequired()
        .then(response => {
          this.prsActionRequired = response.data.results;
        })
        .catch(e => {
          console.log(e);
        });
      PerformanceReviewDataService.getAllManagerUpcomingNoActionRequired()
        .then(response => {
          this.prsNoActionRequired = response.data.results;
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

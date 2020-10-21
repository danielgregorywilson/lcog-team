<template>
  <q-page class="q-pa-md">
    <div class="q-py-md" v-if="isManager()">
      <div class="row items-center q-mb-md">
        <q-avatar icon="insert_chart_outlined" color="primary" text-color="white" font-size="32px" class="q-mr-sm" />
        <div class="text-h4">Review Notes</div>
      </div>
      <review-note-table />
    </div>
    <div class="q-py-md" v-if="isManager()">
      <div class="row items-center q-mb-md">
        <q-avatar icon="assignment_ind" color="primary" text-color="white" font-size="32px" class="q-mr-sm" />
        <div class="text-h4">Current Reviews (For Managers)</div>
      </div>
      <div class="text-h6">Action Required</div>
        <performance-review-table :actionRequired="true" />
      <div class="text-h6">No Action Required</div>
        <performance-review-table :actionRequired="false" />
    </div>
  </q-page>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import ReviewNoteTable from '../components/ReviewNoteTable.vue';
import PerformanceReviewTable from '../components/PerformanceReviewTable.vue';

@Component({
  components: { PerformanceReviewTable, ReviewNoteTable }
})
export default class PerformanceReviews extends Vue {
  private currentIndex = -1;
  private title = '';
  private isManager() {
    return this.$store.getters['userModule/getEmployeeProfile'].is_manager // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-return
  }
};
</script>

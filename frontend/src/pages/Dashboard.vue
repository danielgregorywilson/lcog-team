<template>
  <q-page class="q-pa-md">
    <div class="q-py-md">
      <div class="text-h4">Your Next Review</div>
      <div v-if="getNextReview()">
        <div>Your Next Review is scheduled for {{ getNextReview().period_end_date | readableDate }}</div>
        <div>Current Status: {{ getNextReview().status }}</div>
        <div v-if="getNextReview().evaluation">
          <div>Your manager manager has written an evaluation:</div>
          <div>{{ getNextReview().evaluation }}</div>
          <div v-if="getNextReview().employee_marked_discussed">You have marked this evaluation as discussed</div>
          <div v-else>
            <div>Evaluation is currently not marked as discussed</div>
            <q-btn @click="employeeMarkDiscussed">Mark as discussed</q-btn>
          </div>
        </div>
      </div>
      <div v-else>
        <div class="text-body1">You do not have a scheduled upcoming review</div>
      </div>
    </div>
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
    <div class="q-py-md" v-if="isUpperManager()">
      <div class="row items-center q-mb-md">
        <q-avatar icon="assignment_ind" color="primary" text-color="white" font-size="32px" class="q-mr-sm" />
        <div class="text-h4">All Current Reviews (For Upper Managers)</div>
      </div>
      <div class="text-h6">Action Required</div>
        <performance-review-table :upperManager="true" :actionRequired="true" />
      <div class="text-h6">No Action Required</div>
        <performance-review-table :upperManager="true" :actionRequired="false" />
    </div>
  </q-page>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import ReviewNoteTable from '../components/ReviewNoteTable.vue';
import PerformanceReviewTable from '../components/PerformanceReviewTable.vue';
import PerformanceReviewDataService from '../services/PerformanceReviewDataService'
import { AxiosPerformanceReviewManagerMarkDiscussedServerResponse, PerformanceReviewRetrieve } from '../store/types'

@Component({
  components: { PerformanceReviewTable, ReviewNoteTable }
})
export default class Dashboard extends Vue {
  private currentIndex = -1
  private title = ''
  private nextReviewDate?: Date
  private isManager(): boolean {
    return this.$store.getters['userModule/getEmployeeProfile'].is_manager // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-return
  }

  private isUpperManager(): boolean {
    return this.$store.getters['userModule/getEmployeeProfile'].is_upper_manager // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-return
  }

  private getNextReview(): PerformanceReviewRetrieve {
    return this.$store.getters['performanceReviewModule/nextPerformanceReview'] // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-return
  }

  private employeeMarkDiscussed(): void {
    PerformanceReviewDataService.employeeMarkDiscussed(this.getNextReview().pk)
      .then((response: AxiosPerformanceReviewManagerMarkDiscussedServerResponse) => {
        console.log(response.data.status)
        this.$store.dispatch('performanceReviewModule/employeeMarkDiscussed')
          .catch(e => {
            console.log(e)
          })
      })
      .catch(e => {
        console.log(e)
      })
  }
};
</script>

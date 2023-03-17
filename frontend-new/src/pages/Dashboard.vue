<template>
  <q-page class="q-pa-md" v-if="isAuthenticated()">
    <q-spinner-grid
      v-if="!isProfileLoaded()"
      class="spinner"
      color="primary"
      size="xl"
    />
    <div class="q-py-md">
      <div class="text-h4 q-mb-md">Your Next Review</div>
      <div v-if="getNextReview().employee_pk">
        <div class="q-mb-sm">Current Performance Period: {{ readableDate(getNextReview().period_start_date) }} - {{ readableDate(getNextReview().period_end_date) }}</div>
        <div v-if="nextReviewNeedsEvaluation()">Your manager has not yet completed their evaluation.</div>
        <div v-if="!nextReviewNeedsEvaluation() && !userSignedNextEvaluation()">
          <div>Your manager has completed their evaluation and it is ready for your review.</div>
          <q-btn @click="viewReview(getNextReview().pk)">View and Sign Evaluation</q-btn>
        </div>
        <q-btn v-if="!nextReviewNeedsEvaluation() && userSignedNextEvaluation()" @click="viewReview(getNextReview().pk)">View Evaluation</q-btn>

      </div>
      <div v-else>
        <div class="text-body1">You do not have a scheduled upcoming review</div>
      </div>
    </div>
    <div class="q-py-md" v-if="isManager()">
      <div class="row items-center q-mb-md">
        <q-avatar icon="insert_chart_outlined" color="primary" text-color="white" font-size="32px" class="q-mr-sm" />
        <div class="text-h4">Review Notes</div>
        <q-icon name="help" color="primary" size="xs" style="top: -10px;" >
          <q-tooltip content-style="font-size: 16px">
            Make a note about an employee to reference when completing their evaluation
          </q-tooltip>
        </q-icon>
      </div>
      <!-- <review-note-table /> -->
    </div>
    <div class="q-py-md" v-if="isManager()">
      <div class="row items-center q-mb-md">
        <q-avatar icon="assignment_ind" color="primary" text-color="white" font-size="32px" class="q-mr-sm" />
        <div class="text-h4">Reviews for your Direct Reports</div>
      </div>
      <div class="text-h6">Action Required</div>
        <!-- <performance-review-table :actionRequired="true" /> -->
      <div class="text-h6">No Action Required</div>
        <!-- <performance-review-table :actionRequired="false" /> -->
    </div>
    <div class="q-py-md" v-if="isUpperManager() || isTheHRManager() || isTheExecutiveDirector()">
      <div class="row items-center q-mb-md">
        <q-avatar icon="assignment_turned_in" color="primary" text-color="white" font-size="32px" class="q-mr-sm" />
        <div class="text-h4">Reviews to Sign</div>
      </div>
      <div class="text-h6">Signature Required</div>
        <!-- <performance-review-table :signature="true" :actionRequired="true" /> -->
      <div class="text-h6">Signed</div>
        <!-- <performance-review-table :signature="true" :actionRequired="false" /> -->
    </div>
    <div class="q-py-md" v-if="isManager()">
      <div class="row items-center q-mb-md">
        <q-avatar icon="assignment_ind" color="primary" text-color="white" font-size="32px" class="q-mr-sm" />
        <div class="text-h4">Telework Applications from your Direct Reports</div>
      </div>
      <div class="text-h6">Signature Required</div>
        <!-- <telework-application-table :signature="true" /> -->
      <div class="text-h6">Signed</div>
        <!-- <telework-application-table :signature="false" /> -->
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { readableDate } from 'src/filters'
import { PerformanceReviewRetrieve } from 'src/types'
import { useAuthStore } from 'src/stores/auth';
import { useUserStore } from 'src/stores/user';

const router = useRouter()
const authStore = useAuthStore()
const userStore = useUserStore()

function isAuthenticated(): boolean {
  return authStore.isAuthenticated
}

function isProfileLoaded(): boolean {
  return userStore.isProfileLoaded
}

function isManager(): boolean {
  return userStore.getEmployeeProfile.is_manager
}

function isUpperManager(): boolean {
  return userStore.getEmployeeProfile.is_upper_manager
}

function isTheHRManager(): boolean {
  return userStore.getEmployeeProfile.is_hr_manager
}

function isTheExecutiveDirector(): boolean {
  return userStore.getEmployeeProfile.is_executive_director
}

function getNextReview(): PerformanceReviewRetrieve {
  return {} as PerformanceReviewRetrieve
  // TODO
  // return this.$store.getters['performanceReviewModule/nextPerformanceReview']
}

function nextReviewNeedsEvaluation(): boolean {
  return getNextReview().status == 'Needs evaluation'
}

function userSignedNextEvaluation(): boolean {
  return false
  // TODO
  // Return if there is a date for the employee's signature on the review
  // if (this.getNextReview().all_required_signatures) {
  //   return !!this.getNextReview().all_required_signatures[0][2]
  // } else {
  //   return false
  // }
}

    
function viewReview(pk: number): void {
  router.push(`pr/${ pk }`)
    .catch(e => {
      console.error('Error navigating to PR detail', e)
    })
}

</script>

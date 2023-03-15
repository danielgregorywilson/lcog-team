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

<script lang="ts">
import { defineComponent } from 'vue'
import { readableDate } from 'src/filters'
import { PerformanceReviewRetrieve } from 'src/types'


function isAuthenticated(): boolean {
  // TODO
  return true
  // return this.$store.getters['authModule/isAuthenticated'] // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-return
}

function isProfileLoaded(): boolean {
  return true
  // return this.$store.getters['userModule/isProfileLoaded'] // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-return
}

function isManager(): boolean {
  return true
  // return this.$store.getters['userModule/getEmployeeProfile'].is_manager // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-return
}

function isUpperManager(): boolean {
  return true
  // return this.$store.getters['userModule/getEmployeeProfile'].is_upper_manager // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-return
}

function isTheHRManager(): boolean {
  return true
  // return this.$store.getters['userModule/getEmployeeProfile'].is_hr_manager // eslint-disable-line
}

function isTheExecutiveDirector(): boolean {
  return true
  // return this.$store.getters['userModule/getEmployeeProfile'].is_executive_director // eslint-disable-line
}

function getNextReview(): PerformanceReviewRetrieve {
  return true
  // return this.$store.getters['performanceReviewModule/nextPerformanceReview'] // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-return
}

function nextReviewNeedsEvaluation(): boolean {
  return true
  // return this.getNextReview().status == 'Needs evaluation'
}

function userSignedNextEvaluation(): boolean {
  return false
  // Return if there is a date for the employee's signature on the review
  // if (this.getNextReview().all_required_signatures) {
  //   return !!this.getNextReview().all_required_signatures[0][2]
  // } else {
  //   return false
  // }
}


export default defineComponent({
  // name: 'PageName'

  methods: {
    userSignedNextEvaluation(): boolean {
      return false
      // Return if there is a date for the employee's signature on the review
      // if (this.getNextReview().all_required_signatures) {
      //   return !!this.getNextReview().all_required_signatures[0][2]
      // } else {
      //   return false
      // }
    },
    
    viewReview(pk: number): void {
      this.$router.push(`pr/${ pk }`)
        .catch(e => {
          console.error('Error navigating to PR detail', e)
        })
    }
  },

  setup () {
    return {
      getNextReview, isAuthenticated, isManager, isProfileLoaded,
      isTheExecutiveDirector, isTheHRManager, isUpperManager,
      nextReviewNeedsEvaluation, readableDate
    };
  },
})
</script>

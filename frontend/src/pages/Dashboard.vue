<template>
  <q-page class="q-pa-md" v-if="isAuthenticated()">
    <q-spinner-grid
      v-if="!isProfileLoaded()"
      class="spinner"
      color="primary"
      size="xl"
    />
    <div v-else class="row">
      <div class="q-py-md">
        <div class="text-h4 q-mb-md">Workflows Needing Action</div>
        <WorkflowTable
          :archived="false"
          :complete="false"
          type="all"
          :allowAddDelete="false"
          :workflowsLoaded="workflowsLoaded"
          filterActionRequired
        />
      </div>
    </div>

    <!-- <div class="q-py-md">
      <div class="text-h4 q-mb-md">Your Next Review</div>
      <div v-if="nextReview().employee_pk">
        <div class="q-mb-sm">
          Current Performance Period:
          {{ readableDate(nextReview().period_start_date) }} -
          {{ readableDate(nextReview().period_end_date) }}
        </div>
        <div v-if="nextReviewNeedsEvaluation()">
          Your manager has not yet completed their evaluation.
        </div>
        <div v-if="!nextReviewNeedsEvaluation() && !userSignedNextEvaluation()">
          <div>
            Your manager has completed their evaluation and it is ready for your
            review.
          </div>
          <q-btn @click="viewReview(nextReview().pk)" class="q-mt-sm">
            View and Sign Evaluation
          </q-btn>
        </div>
        <q-btn
          v-if="!nextReviewNeedsEvaluation() && userSignedNextEvaluation()"
          @click="viewReview(nextReview().pk)"
        >
          View Evaluation
        </q-btn>

      </div>
      <div v-else>
        <div class="text-body1">
          You do not have a scheduled upcoming review
        </div>
      </div>
    </div>
    <div class="q-py-md" v-if="isManager()">
      <div class="row items-center q-mb-md">
        <q-avatar
          icon="assignment_ind"
          color="primary"
          text-color="white"
          font-size="32px"
          class="q-mr-sm"
        />
        <div class="text-h4">Reviews for your Direct Reports</div>
      </div>
      <div class="text-h6">Action Required</div>
        <PerformanceReviewTable
          :actionRequired="true"
          :pk="userStore.getEmployeeProfile.employee_pk"
        />
      <div class="text-h6">No Action Required</div>
        <PerformanceReviewTable
          :actionRequired="false"
          :pk="userStore.getEmployeeProfile.employee_pk"
        />
    </div>
    <div
      class="q-py-md"
      v-if="isUpperManager() || isTheHRManager() || isTheExecutiveDirector()"
    >
      <div class="row items-center q-mb-md">
        <q-avatar
          icon="assignment_turned_in"
          color="primary"
          text-color="white"
          font-size="32px"
          class="q-mr-sm"
        />
        <div class="text-h4">Reviews to Sign</div>
      </div>
      <div class="text-h6">Signature Required</div>
        <PerformanceReviewTable
          :signature="true"
          :actionRequired="true"
          :pk="userStore.getEmployeeProfile.employee_pk"
        />
      <div class="text-h6">Signed</div>
        <PerformanceReviewTable
          :signature="true"
          :actionRequired="false"
          :pk="userStore.getEmployeeProfile.employee_pk"
        />
    </div> -->
  </q-page>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
// import { useRouter } from 'vue-router'

// import PerformanceReviewTable from 'src/components/PerformanceReviewTable.vue'
import WorkflowTable from 'src/components/workflows/WorkflowTable.vue'
import useEventBus from 'src/eventBus'
// import { readableDate } from 'src/filters'
import { useAuthStore } from 'src/stores/auth'
import { usePerformanceReviewStore } from 'src/stores/performancereview'
import { useUserStore } from 'src/stores/user'
import { useWorkflowsStore } from 'src/stores/workflows'
// import { PerformanceReviewRetrieve } from 'src/types'

// const router = useRouter()
const { bus } = useEventBus()
const authStore = useAuthStore()
const userStore = useUserStore()
const performanceReviewStore = usePerformanceReviewStore()
const workflowsStore = useWorkflowsStore()

let workflowsLoaded = ref(false)

function isAuthenticated(): boolean {
  return authStore.isAuthenticated
}

function isProfileLoaded(): boolean {
  return userStore.isProfileLoaded
}

// function isManager(): boolean {
//   return userStore.getEmployeeProfile.is_manager
// }

// function isUpperManager(): boolean {
//   return userStore.getEmployeeProfile.is_upper_manager
// }

// function isTheHRManager(): boolean {
//   return userStore.getEmployeeProfile.is_hr_manager
// }

// function isTheExecutiveDirector(): boolean {
//   return userStore.getEmployeeProfile.is_executive_director
// }

// function nextReview(): PerformanceReviewRetrieve {
//   // return {} as PerformanceReviewRetrieve
//   // TODO
//   return performanceReviewStore.nextPerformanceReview
//   // return this.$store.getters['performanceReviewModule/nextPerformanceReview']
// }

// function nextReviewNeedsEvaluation(): boolean {
//   return nextReview().status == 'Needs evaluation'
// }

// function userSignedNextEvaluation(): boolean {
//   return false
//   // TODO
//   // Return if there is a date for the employee's signature on the review
//   // if (this.getNextReview().all_required_signatures) {
//   //   return !!this.getNextReview().all_required_signatures[0][2]
//   // } else {
//   //   return false
//   // }
// }


// function viewReview(pk: number): void {
//   router.push(`pr/${ pk }`)
//     .catch(e => {
//       console.error('Error navigating to PR detail', e)
//     })
// }

function retrieveWorkflows(): void {
  workflowsStore.getWorkflows({archived: false, complete: false})
    .then(() => {
      workflowsLoaded.value = true
    })  
    .catch(e => {
      console.error('Error retrieving workflows:', e)
    })
}

onMounted(() => {
  retrieveWorkflows()
})

watch(() => bus.value.get('gotUserProfile'), () => {
  performanceReviewStore.getNextPerformanceReview(
    userStore.getEmployeeProfile.employee_pk
  )
    .catch(e => {
      console.error('Error retrieving next performance review:', e)
    })
})

</script>

<template>
  <q-page padding>
    <div class="q-py-md" v-if="isManager()">
      <div class="row items-center q-mb-md">
        <q-avatar icon="insert_chart_outlined" color="primary" text-color="white" font-size="32px" class="q-mr-sm" />
        <div class="text-h4">Review Notes</div>
      </div>
      <ReviewNoteTable />
    </div>
    <div class="q-py-md" v-if="isManager()">
      <div class="row items-center q-mb-md">
        <q-avatar icon="assignment_ind" color="primary" text-color="white" font-size="32px" class="q-mr-sm" />
        <div class="text-h4">Current Reviews (For Managers)</div>
      </div>
      <div class="text-h6">Action Required</div>
        <PerformanceReviewTable :actionRequired="true" />
      <div class="text-h6">No Action Required</div>
        <PerformanceReviewTable :actionRequired="false" />
    </div>
    <div class="q-py-md" v-if="isUpperManager() || isTheHRManager() || isTheExecutiveDirector()">
      <div class="row items-center q-mb-md">
        <q-avatar icon="assignment_turned_in" color="primary" text-color="white" font-size="32px" class="q-mr-sm" />
        <div class="text-h4">Reviews to Sign</div>
      </div>
      <div class="text-h6">Signature Required</div>
        <PerformanceReviewTable :signature="true" :actionRequired="true" />
      <div class="text-h6">Signed</div>
        <PerformanceReviewTable :signature="true" :actionRequired="false" />
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue'

import { useUserStore } from 'src/stores/user'
import PerformanceReviewTable from 'src/components/PerformanceReviewTable.vue'
import ReviewNoteTable from 'src/components/ReviewNoteTable.vue'


const userStore = useUserStore()

let currentIndex = ref(-1)
let title = ref('')

function isManager() {
    return userStore.getEmployeeProfile.is_manager
}

function isUpperManager() {
  return userStore.getEmployeeProfile.is_upper_manager
}

function isTheHRManager(): boolean {
  return userStore.getEmployeeProfile.is_hr_manager
}

function isTheExecutiveDirector(): boolean {
  return userStore.getEmployeeProfile.is_executive_director
}


</script>

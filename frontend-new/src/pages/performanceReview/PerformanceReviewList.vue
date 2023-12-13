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
        <!-- <performance-review-table :actionRequired="true" /> -->
      <div class="text-h6">No Action Required</div>
        <!-- <performance-review-table :actionRequired="false" /> -->
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue'

import { useUserStore } from 'src/stores/user'
import ReviewNoteTable from 'src/components/ReviewNoteTable.vue'


const userStore = useUserStore()

let currentIndex = ref(-1)
let title = ref('')

function isManager() {
    return userStore.getEmployeeProfile.is_manager
}


</script>

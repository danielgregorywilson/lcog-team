<template>
  <div class="row">
    <q-btn-group push>
      <q-btn
        name="reviews-incomplete-button"
        push
        color="primary"
        glossy
        label="Active"
        :to="{ name: 'reviews-dashboard' }"
      />
      <q-btn
        name="reviews-complete-button"
        push
        color="secondary"
        glossy
        label="Complete"
        :to="{ name: 'reviews-complete' }"
      />
    </q-btn-group>
  </div>
  <div class="row items-center justify-between">
    <div class="text-h5">Complete Reviews</div>
    <!-- <div>Only the 100 most recently completed reviews are shown.</div> -->
  </div>
  <ReviewTable
    :managerPk="userStore.getEmployeeProfile.employee_pk"
    :complete="true"
  />
  <!-- TODO: For now we just have one complete page/table -->
  <!-- <router-view /> -->
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import ReviewTable from 'src/components/ReviewTable.vue'
import { useUserStore } from 'src/stores/user'
import { useWorkflowsStore } from 'src/stores/workflows'
// import { getCurrentUser } from 'src/utils'

// const router = useRouter()
const userStore = useUserStore()
// const workflowsStore = useWorkflowsStore()

// let workflowsLoaded = ref(false)

</script>

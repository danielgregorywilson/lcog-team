<template>
  <q-page class="q-pa-md">
    <div class="text-h4 q-mb-md">Employee Profile</div>
    <div class="q-mb-md">
      <div class="text-h5 q-mb-sm">Basic Info</div>
      <div>Legal Name: {{ employeeLegalName() }}</div>
      <div>Display Name: {{ employeeName() }}</div>
    </div>
    <div>
      <div class="text-h5 q-mb-sm">Performance Reviews</div>
      <PerformanceReviewTable :employee="true" :pk=pk() />
    </div>
  </q-page>
</template>

<style scoped lang="scss">

</style>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRoute } from 'vue-router';

import PerformanceReviewTable from 'src/components/PerformanceReviewTable.vue'
import { useUserStore } from 'src/stores/user'
import { usePeopleStore } from 'src/stores/people'
import { EmployeeRetrieve } from 'src/types'

const peopleStore = usePeopleStore()
const userStore = useUserStore()
const route = useRoute()

function pk(): number {
  if (typeof route.params.pk == 'string') {
    return parseInt(route.params.pk)
  } else {
    return parseInt(route.params.pk[0])
  }
}

function employeeName(): string {
  return peopleStore.simpleEmployeeDetail.name
}

function employeeLegalName(): string {
  return peopleStore.simpleEmployeeDetail.legal_name
}

function retrieveProfile(): Promise<EmployeeRetrieve> {
  return new Promise((resolve, reject) => {

    peopleStore.getSimpleEmployeeDetail({pk: pk()})
      .then((employee) => {
        resolve(employee)
      })
      .catch((error) => {
        reject(error)
      })
  })
}

onMounted(() => { 
  retrieveProfile()
})
</script>

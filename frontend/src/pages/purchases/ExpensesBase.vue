<template>
<q-page class="q-pa-md">
  <div class="text-h4">Credit Card Expenses</div>
  <div class="q-my-md">
    <q-btn-group rounded>
      <q-btn
        v-if="isExpenseManager()"
        :to="{ name: 'submit-expenses' }"
        unelevated
        rounded
        color="primary"
        icon="book"
        :label="$q.screen.xs ? 'Submit' : 'Submit Expenses'"
      />
      <q-btn
        v-if="isExpenseApprover()"
        :to="{ name: 'approve-expenses' }"
        unelevated
        rounded
        color="primary"
        icon="bookmark_added"
        :label="$q.screen.xs ? 'Approve' : 'Approve Expenses'"
      >
        <q-badge v-if="numExpenseGLsToApprove()" rounded color="red" floating>
          {{ numExpenseGLsToApprove() }}
        </q-badge>
      </q-btn>
      <q-btn
        v-if="isDirector()"
        :to="{ name: 'director-approve-expenses' }"
        unelevated
        rounded
        color="primary"
        icon="library_add_check"
        label="Director Approve"
      >
        <q-badge
          v-if="numExpensesDirectorToApprove()"
          rounded
          color="red"
          floating
        >
          {{ numExpensesDirectorToApprove() }}
        </q-badge>
      </q-btn>
      <q-btn
        v-if="isFiscal()"
        :to="{ name: 'fiscal-approve-expenses' }"
        unelevated
        rounded
        color="primary"
        icon="library_add_check"
        label="Fiscal Approve"
      >
        <q-badge
          v-if="numExpensesFiscalToApprove()"
          rounded
          color="red"
          floating
        >
          {{ numExpensesFiscalToApprove() }}
        </q-badge>
      </q-btn>
    </q-btn-group>  
  </div>
  <div class="q-gutter-md">
    <q-btn @click="setThisMonth()">This Month</q-btn>
    <q-btn-group>
      <q-btn color="secondary" icon="west" @click="monthBackward()"/>
      <q-btn color="secondary" icon="east" @click="monthForward()"/>
    </q-btn-group>
  </div>
  <div>
    <router-view
      :monthDisplay="monthDisplay()"
      :dayInt="new Date().getDate()"
      :monthInt="firstOfSelectedMonth.getMonth() + 1"
      :yearInt="firstOfSelectedMonth.getFullYear()"
    ></router-view>
  </div>
</q-page>
</template>

<style scoped lang="scss"></style>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { usePurchaseStore } from 'src/stores/purchase'
import { useUserStore } from 'src/stores/user'

const purchaseStore = usePurchaseStore()
const userStore = useUserStore()

let firstOfThisMonth = ref(new Date())
let firstOfSelectedMonth = ref(new Date())

function isExpenseManager() {
  return userStore.isExpenseManager
}

function isExpenseApprover() {
  return userStore.isExpenseApprover
}

function isDirector() {
  return userStore.isDivisionDirector
}

function isFiscal() {
  return userStore.isFiscal
}

function monthDisplay(): string {
  const m = firstOfSelectedMonth.value.toLocaleDateString(
    'en-us', { month: 'long' }
  )
  const y = firstOfSelectedMonth.value.getFullYear()
  return `${m} ${y}`
}

function setDates() {
  let theFirst = new Date()
  theFirst.setDate(1)
  theFirst.setHours(0,0,0,0)
  firstOfThisMonth.value = theFirst
  firstOfSelectedMonth.value = theFirst
}

function setThisMonth() {
  firstOfSelectedMonth.value = firstOfThisMonth.value
}

function monthBackward() {
  const m = firstOfSelectedMonth.value.getMonth()
  const y = firstOfSelectedMonth.value.getFullYear()
  firstOfSelectedMonth.value = m === 0
    ? new Date(y - 1, 11, 1)
    : new Date(y, m - 1, 1)
}

function monthForward() {
  const m = firstOfSelectedMonth.value.getMonth()
  const y = firstOfSelectedMonth.value.getFullYear()
  firstOfSelectedMonth.value = m === 11
    ? new Date(y + 1, 0, 1)
    : new Date(y, m + 1, 1)
}

function numExpenseGLsToApprove(): number {
  return purchaseStore.numExpenseGLsToApprove
}

function numExpensesDirectorToApprove(): number {
  return purchaseStore.numExpensesDirectorToApprove
}

function numExpensesFiscalToApprove(): number {
  return purchaseStore.numExpensesFiscalToApprove
}

onMounted(() => {
  setDates()
})

</script>

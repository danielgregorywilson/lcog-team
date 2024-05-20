<template>
  <q-page class="q-pa-md">
    <div class="text-h4">Credit Card Expenses</div>
    <div class="q-my-md">
      <q-btn-group rounded>
        <q-btn v-if="isExpenseManager()" :to="{ name: 'submit-expenses' }" unelevated rounded color="primary" icon="book" :label="$q.screen.xs ? 'Submit' : 'Submit Expenses'" />
        <q-btn v-if="isExpenseApprover()" :to="{ name: 'approve-expenses' }" unelevated rounded color="primary" icon="bookmark_added" :label="$q.screen.xs ? 'Approve' : 'Approve Expenses'">
          <q-badge v-if="numExpensesToApprove()" rounded color="red" floating>{{ numExpensesToApprove() }}</q-badge>
        </q-btn>
        <q-btn v-if="isFiscal()" :to="{ name: 'fiscal-approve' }" unelevated rounded color="primary" icon="library_add_check" label="Fiscal Approve">
          <q-badge v-if="numExpensesToApprove()" rounded color="red" floating>{{ numExpensesToApprove() }}</q-badge>
        </q-btn>
      </q-btn-group>  
    </div>
    <div v-if="route.name != 'approve-expenses'" class="q-gutter-md">
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
        :monthInt="firstOfSelectedMonth.getMonth()"
        :yearInt="firstOfSelectedMonth.getFullYear()"
      ></router-view>
    </div>
  </q-page>
  </template>

  <style scoped lang="scss"></style>

  <script setup lang="ts">
  import { onMounted, ref } from 'vue'
  import { useRoute } from 'vue-router'
  import { useUserStore } from 'src/stores/user'

  const route = useRoute()
  const userStore = useUserStore()

  let firstOfThisMonth = ref(new Date())
  let firstOfSelectedMonth = ref(new Date())

  function isExpenseManager() {
    return userStore.isExpenseManager
  }

  function isExpenseApprover() {
    return userStore.isExpenseApprover
  }

  function isFiscal() {
    return userStore.isFiscal
  }

  function monthDisplay(): string {
    return `${firstOfSelectedMonth.value.toLocaleDateString('en-us', { month: 'long' })} ${firstOfSelectedMonth.value.getFullYear()}`
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
    firstOfSelectedMonth.value = firstOfSelectedMonth.value.getMonth() === 0
      ? new Date(firstOfSelectedMonth.value.getFullYear() - 1, 11, 1)
      : new Date(firstOfSelectedMonth.value.getFullYear(), firstOfSelectedMonth.value.getMonth() - 1, 1)
  }

  function monthForward() {
    firstOfSelectedMonth.value = firstOfSelectedMonth.value.getMonth() === 11
      ? new Date(firstOfSelectedMonth.value.getFullYear() + 1, 0, 1)
      : new Date(firstOfSelectedMonth.value.getFullYear(), firstOfSelectedMonth.value.getMonth() + 1, 1)
  }

  function numExpensesToApprove(): number {
    return 0
    // const tors = managedTimeOffRequests()
    // if (tors) {
    //   return tors.filter(tor => tor.acknowledged == null).length
    // } else {
    //   return 0
    // }
  }

  onMounted(() => {
    setDates()
  })

  </script>

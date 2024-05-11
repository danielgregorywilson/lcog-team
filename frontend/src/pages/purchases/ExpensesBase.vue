<template>
  <q-page class="q-pa-md">
    <div class="text-h4">Credit Card Expenses</div>
    <div class="q-my-md">
      <q-btn-group rounded>
        <q-btn v-if="isExpenseManager()" :to="{ name: 'my-expenses' }" unelevated rounded color="primary" icon="calendar_today" :label="$q.screen.xs ? 'Requests' : 'My Requests'" />
        <q-btn v-if="isExpenseApprover()" :to="{ name: 'timeoff-manage-requests' }" unelevated rounded color="primary" icon="book" :label="$q.screen.xs ? 'Manage' : 'Manage Requests'">
          <q-badge v-if="numExpensesToApprove()" rounded color="red" floating>{{ numExpensesToApprove() }}</q-badge>
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
        :monthInt="firstOfSelectedMonth.getMonth()"
        :yearInt="firstOfSelectedMonth.getFullYear()"
      ></router-view>
    </div>
  </q-page>
  </template>

  <style scoped lang="scss"></style>

  <script setup lang="ts">
  import { onMounted, ref } from 'vue'
  import { useUserStore } from 'src/stores/user'

  const userStore = useUserStore()

  let firstOfThisMonth = ref(new Date())
  let firstOfSelectedMonth = ref(new Date())

  function isExpenseManager() {
    return userStore.isExpenseManager
  }

  function isExpenseApprover() {
    return userStore.isExpenseApprover
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

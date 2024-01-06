<template>
  <q-page class="q-pa-md">
    <p class="text-h5">Organization</p>
    <EmployeeTable />
    
    
  </q-page>
</template>

<style scoped lang="scss">
.q-input {
  width: 300px;
}

.success {
    color: green;
}
</style>

<script setup lang="ts">
import { onMounted, ref } from 'vue'

import { useUserStore } from 'src/stores/user'
import { usePeopleStore } from 'src/stores/people'
import { EmployeeRetrieve } from 'src/types'

import EmployeeTable from 'src/components/EmployeeTable.vue'

const peopleStore = usePeopleStore()
const userStore = useUserStore()

let employeePk = ref('')

let displayNameCurrentVal = ref('')
let displayName = ref('')

let emailOptOutAllCurrentVal = ref(false)
let emailOptOutAll = ref(false)
let emailOptOutTimeOffAllCurrentVal = ref(false)
let emailOptOutTimeOffAll = ref(false)
let emailOptOutTimeOffWeeklyCurrentVal = ref(false)
let emailOptOutTimeOffWeekly = ref(false)
let emailOptOutTimeOffDailyCurrentVal = ref(false)
let emailOptOutTimeOffDaily = ref(false)

let submitted = ref(false)

function retrieveProfile(): Promise<EmployeeRetrieve> {
  return new Promise((resolve, reject) => {
    // We cannot guarantee the user has arrived in vuex state immediately, so request it again here
    userStore.simpleUserRequest()
      .then((employee) => {
        employeePk.value = employee.pk.toString()
        // Now that we have the user's pk, get or create a Telework Application for that user
        displayName.value = employee.name
        displayNameCurrentVal.value = displayName.value
        emailOptOutAll.value = employee.email_opt_out_all
        emailOptOutAllCurrentVal.value = emailOptOutAll.value
        emailOptOutTimeOffAll.value = employee.email_opt_out_timeoff_all
        emailOptOutTimeOffAllCurrentVal.value = emailOptOutTimeOffAll.value
        emailOptOutTimeOffWeekly.value = employee.email_opt_out_timeoff_weekly
        emailOptOutTimeOffWeeklyCurrentVal.value = emailOptOutTimeOffWeekly.value
        emailOptOutTimeOffDaily.value = employee.email_opt_out_timeoff_daily
        emailOptOutTimeOffDailyCurrentVal.value = emailOptOutTimeOffDaily.value
      })
      .catch(e => {
        console.error('Error getting user from API:', e)
        reject(e)
      })
  })
}

function valuesAreChanged(): boolean { 
  if (
    displayName.value == displayNameCurrentVal.value &&
    emailOptOutAll.value == emailOptOutAllCurrentVal.value &&
    emailOptOutTimeOffAll.value == emailOptOutTimeOffAllCurrentVal.value &&
    emailOptOutTimeOffWeekly.value == emailOptOutTimeOffWeeklyCurrentVal.value &&
    emailOptOutTimeOffDaily.value == emailOptOutTimeOffDailyCurrentVal.value
  ) {
    return false
  } else {
    return true
  }
}

function submitProfileForm(): void {
  peopleStore.updatePartialEmployee(employeePk.value, {
    display_name: displayName.value,
    email_opt_out_all: emailOptOutAll.value,
    email_opt_out_timeoff_all: emailOptOutTimeOffAll.value,
    email_opt_out_timeoff_weekly: emailOptOutTimeOffWeekly.value,
    email_opt_out_timeoff_daily: emailOptOutTimeOffDaily.value
  })
    .then((p) => {
      displayNameCurrentVal.value = p.name
      emailOptOutAllCurrentVal.value = p.email_opt_out_all
      emailOptOutTimeOffAllCurrentVal.value = p.email_opt_out_timeoff_all
      emailOptOutTimeOffWeeklyCurrentVal.value = p.email_opt_out_timeoff_weekly
      emailOptOutTimeOffDailyCurrentVal.value = p.email_opt_out_timeoff_daily
      userStore.userRequest()
        .catch(e => {
          console.error('Error getting user from store', e)
        })
      submitted.value = true
      setTimeout(() => submitted.value = false, 3000)
    })
    .catch(e => {
      console.error('Error updating employee profile settings:', e)
    })
}

onMounted(() => { 
  retrieveProfile()
    .catch(e => {
      console.error('Error retrieving Employee profile from API:', e)
    })
})
</script>

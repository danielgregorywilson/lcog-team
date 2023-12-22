<template>
  <q-page class="q-pa-md">
    <p class="text-h5">Update Your Profile</p>
    <form>
      <!-- DISPLAY NAME -->
      <p class="row text-h6 q-mt-lg q-mb-none">Display Name</p>
      <div class="row items-center q-gutter-sm">
        <q-input v-model="displayName" />
      </div>
      
      <p class="row text-h6 q-mt-lg q-mb-none">Email Notifications</p>
      <!-- ALL EMAILS -->
      <p class="row q-mb-none text-bold">All</p>
      <div class="row items-center q-gutter-sm">
        <q-toggle
          v-model="emailOptOutAll"
          color="negative"
          checked-icon="clear"
          unchecked-icon="mail"
          :label="emailOptOutAll ? 'Opt out of all email notifications' : 'Receive email notifications'"
          class="text-bold"
        />
      </div>
      <hr/>
      <!-- TIMEOFF EMAILS -->
      <p class="row q-mb-none text-bold">Time Off</p>
      <div class="row items-center q-gutter-sm">
        <q-toggle
          v-model="emailOptOutTimeOffAll"
          color="negative"
          checked-icon="clear"
          unchecked-icon="mail"
          :label="emailOptOutTimeOffAll ? 'Opt out of all time off email notifications' : 'Receive time off email notifications'"
          class="text-bold"
          :disable="emailOptOutAll"
        />
      </div>
      <div class="row items-center q-gutter-sm">
        <q-toggle
          v-model="emailOptOutTimeOffWeekly"
          color="negative"
          checked-icon="clear"
          unchecked-icon="mail"
          :label="emailOptOutTimeOffWeekly ? 'Opt out of weekly time off email notifications' : 'Receive weekly time off email notifications'"
          :disable="emailOptOutAll || emailOptOutTimeOffAll"
        />
      </div>
      <div class="row items-center q-gutter-sm">
        <q-toggle
          v-model="emailOptOutTimeOffDaily"
          color="negative"
          checked-icon="clear"
          unchecked-icon="mail"
          :label="emailOptOutTimeOffDaily ? 'Opt out of daily time off email notifications' : 'Receive daily time off email notifications'"
          :disable="emailOptOutAll || emailOptOutTimeOffAll"
        />
      </div>
      <div class="row items-center q-gutter-sm q-mt-sm">
        <q-btn :disabled="!valuesAreChanged()" @click="submitProfileForm()">Submit</q-btn>
        <span class="success q-ml-sm q-mt-sm" :hidden="!submitted"><strong>Profile Updated.</strong></span>
      </div>
    </form>
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

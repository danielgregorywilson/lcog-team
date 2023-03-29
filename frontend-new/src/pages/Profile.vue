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
        <q-btn :disabled="submitted" @click="submitProfileForm()">Submit</q-btn>
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
import { AxiosEmployeeRetrieveOneServerResponse } from 'src/types'

const peopleStore = usePeopleStore()
const userStore = useUserStore()

let employeePk = ref('')
let displayName = ref('')

let emailOptOutAll = ref(false)
let emailOptOutTimeOffAll = ref(false)
let emailOptOutTimeOffWeekly = ref(false)
let emailOptOutTimeOffDaily = ref(false)

let submitted = ref(false)

function retrieveProfile(): Promise<AxiosEmployeeRetrieveOneServerResponse> {
  return new Promise((resolve, reject) => {
    // We cannot guarantee the user has arrived in vuex state immediately, so request it again here
    userStore.simpleUserRequest()
      .then((simpleUserresponse: AxiosEmployeeRetrieveOneServerResponse) => {
        // Now that we have the user's pk, get or create a Telework Application for that user
        displayName.value = simpleUserresponse.data.name
        employeePk.value = simpleUserresponse.data.pk.toString()
        emailOptOutAll.value = simpleUserresponse.data.email_opt_out_all
        emailOptOutTimeOffAll.value = simpleUserresponse.data.email_opt_out_timeoff_all
        emailOptOutTimeOffWeekly.value = simpleUserresponse.data.email_opt_out_timeoff_weekly
        emailOptOutTimeOffDaily.value = simpleUserresponse.data.email_opt_out_timeoff_daily
      })
      .catch(e => {
        console.error('Error getting user from API:', e)
        reject(e)
      })
  })
}

function submitProfileForm(): void {
  peopleStore.updatePartialEmployee(employeePk.value, {
    display_name: displayName.value,
    email_opt_out_all: emailOptOutAll.value,
    email_opt_out_timeoff_all: emailOptOutTimeOffAll.value,
    email_opt_out_timeoff_weekly: emailOptOutTimeOffWeekly.value,
    email_opt_out_timeoff_daily: emailOptOutTimeOffDaily.value
  })
    .then(() => {
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

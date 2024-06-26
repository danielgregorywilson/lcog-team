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

      <p class="row text-h6 q-mt-lg q-mb-none">Workflow Display Order</p>
      <q-markup-table style="max-width: 500px;">
        <thead>
          <tr>
            <th class="text-left">Workflow Type</th>
            <th>Display</th>
          </tr>
        </thead>
        <draggable 
          v-model="workflows" 
          tag="tbody"
          group="people" 
          @start="drag=true"
          @end="onEndDrag()"
          item-key="id">
          <template #item="{element}">
            <tr>
              <td class="text-left">{{ element.name }}</td>
              <td class="text-center"><q-checkbox v-model="element.display"/></td>
            </tr>
          </template>
        </draggable>
      </q-markup-table>

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
import { onMounted, Ref, ref } from 'vue'
import draggable from 'vuedraggable'

import { useUserStore } from 'src/stores/user'
import { usePeopleStore } from 'src/stores/people'
import { EmployeeRetrieve, WorkflowOption } from 'src/types'

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

let drag = ref(false)
let workflows: Ref<Array<WorkflowOption>> = ref([])
let workflowsCurrentVal: Ref<Array<WorkflowOption>> = ref([])

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
        workflows.value = employee.workflow_display_options
        workflowsCurrentVal.value = JSON.parse(JSON.stringify(workflows.value))
      })
      .catch(e => {
        console.error('Error getting user from API:', e)
        reject(e)
      })
  })
}

function workflowOptionsAreChanged(): boolean {
  if (workflows.value.length != workflowsCurrentVal.value.length) {
    return true
  }
  for (let i = 0; i < workflows.value.length; i++) {
    if (workflows.value[i].id != workflowsCurrentVal.value[i].id) {
      return true
    }
    if (workflows.value[i].name != workflowsCurrentVal.value[i].name) {
      return true
    }
    if (workflows.value[i].display != workflowsCurrentVal.value[i].display) {
      return true
    }
    if (workflows.value[i].order != workflowsCurrentVal.value[i].order) {
      return true
    }
  }
  return false
}

function valuesAreChanged(): boolean { 
  if (
    displayName.value == displayNameCurrentVal.value &&
    emailOptOutAll.value == emailOptOutAllCurrentVal.value &&
    emailOptOutTimeOffAll.value == emailOptOutTimeOffAllCurrentVal.value &&
    emailOptOutTimeOffWeekly.value == emailOptOutTimeOffWeeklyCurrentVal.value &&
    emailOptOutTimeOffDaily.value == emailOptOutTimeOffDailyCurrentVal.value &&
    !workflowOptionsAreChanged()
  ) {
    return false
  } else {
    return true
  }
}

function onEndDrag(): void {
  drag.value = false
  // updateServer(workflows)
}

function submitProfileForm(): void {
  peopleStore.updatePartialEmployee(employeePk.value, {
    display_name: displayName.value,
    email_opt_out_all: emailOptOutAll.value,
    email_opt_out_timeoff_all: emailOptOutTimeOffAll.value,
    email_opt_out_timeoff_weekly: emailOptOutTimeOffWeekly.value,
    email_opt_out_timeoff_daily: emailOptOutTimeOffDaily.value,
    workflow_display_options: workflows.value
  })
    .then((p) => {
      displayNameCurrentVal.value = p.name
      emailOptOutAllCurrentVal.value = p.email_opt_out_all
      emailOptOutTimeOffAllCurrentVal.value = p.email_opt_out_timeoff_all
      emailOptOutTimeOffWeeklyCurrentVal.value = p.email_opt_out_timeoff_weekly
      emailOptOutTimeOffDailyCurrentVal.value = p.email_opt_out_timeoff_daily
      workflows.value = JSON.parse(JSON.stringify(
        p.workflow_display_options
      ))
      workflowsCurrentVal.value = JSON.parse(JSON.stringify(
        p.workflow_display_options
      ))
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

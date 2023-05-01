<template>
  <div>
    <div class="q-gutter-md row">
      <q-date v-model="dates" range @input="dateChanged()"/>
      <div v-if="conflictingTimeOffRequests().length != 0">
        <q-icon color="orange" name="warning" size="xl" class="q-ml-sm" />
        <div>
          <div>One or more team members with shared responsibilities will be also be unavailable:</div>
          <ul>
            <li v-for="tor of conflictingTimeOffRequests()" :key="tor.pk">
              <router-link :to="{ name: 'employee-responsibilities', params: { pk: tor.employee_pk } }">{{ tor.employee_name }}</router-link>: {{ employee.responsibility_names[0] }}<span v-if="employee.responsibility_names.length > 1"> and {{ employee.responsibility_names.length - 1 }} more</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
    <q-input
        v-model="note"
        label="Public Note (visible to team members)"
        class="q-pb-md"
    />
    <q-input
      v-model="privateNote"
      label="Private Note (visible to manager only)"
      class="q-pb-md"
    />
    <q-btn color="white" text-color="black" label="Update" :disabled="!formIsFilled()" @click="updateTimeOffRequest()" />
  </div>
</template>

<script setup lang="ts">

import { onMounted, ref, Ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { getRoutePk } from 'src/utils'
import { TimeOffRequestDates, TimeOffRequestRetrieve } from 'src/types'
import { useTimeOffStore } from 'src/stores/timeoff'

const route = useRoute()
const router = useRouter()
const timeOffStore = useTimeOffStore()

const pk = getRoutePk(route)
let dates: Ref<TimeOffRequestDates> = ref({'from': '', 'to': ''})
let note = ref('')
let privateNote = ref('')

function formIsFilled(): boolean {
  if (!!dates.value) {
    return true
  } else {
    return false
  }
}

// TODO: Do a valuesAreChanged thing like with ReviewNoteDetail so we aren't always resetting acknowledgements unnecessarily

function conflictingTimeOffRequests(): Array<TimeOffRequestRetrieve> {
  return timeOffStore.conflictingTimeOffRequests
}

function dateChanged(): void {
  // Check if there are any coworkers out with shared responsibilities
  if (dates.value) {
    timeOffStore.getConflictingTimeOffRequests({ dates: dates.value })
      .catch(e => {
        console.error('Error getting conflicting responsibilities:', e)
      })
  }
}

function retrieveRequest(): void {
  if (!pk) {
    console.error('No pk provided to retrieve time off request')
    return
  }
  timeOffStore.getCurrentTimeOffRequest(pk)
    .then(() => {
      const tor = timeOffStore.currentTimeOffRequest
      const startDate: string = tor.start_date.toString().split('-').join('/')
      const endDate: string = tor.end_date.toString().split('-').join('/')
      if (startDate == endDate) {
        dates.value = startDate
      } else {
        dates.value = {'from': startDate, 'to': endDate}
      }
      note.value = tor.note
      privateNote.value = tor.private_note
    })
    .catch(e => {
      console.error('Error getting time off request:', e)
    })
}

function updateTimeOffRequest(): void {
  if (!pk) {
    console.error('No pk provided to update time off request')
    return
  }
  timeOffStore.updateTimeOffRequest({
    pk: pk,
    dates: dates.value,
    note: note.value,
    privateNote: privateNote.value
  })
    .then(() => {
      router.push({ name: 'timeoff-my-requests'})
        .catch(e => {
          console.error('Error navigating to My Requests page after creating time off request:', e)
        })
    })
    .catch(e => {
      console.error('Error updating time off request:', e)
    })
}

onMounted(() => {
  retrieveRequest()
})

</script>

<template>
  <div>
    <div class="q-gutter-md row">
      <q-date v-model="dates" range @update:model-value="dateChanged()"/>
      <div v-if="conflictingResponsibilities().length != 0">
        <q-icon color="orange" name="warning" size="xl" class="q-ml-sm" />
        <div>
          <div>
            One or more team members with shared responsibilities will also be
            unavailable:
          </div>
          <ul>
            <li v-for="tor of conflictingResponsibilities()" :key="tor.pk">
              <router-link
                :to="{ name: 'employee-responsibilities',
                params: { pk: tor.pk } }"
              >
                {{ tor.name }}
              </router-link>
              : 
              <span v-for="(name, idx) of tor.responsibility_names" :key="idx">
                <span v-if="idx==0">{{ name }}</span>
                <span v-else>, {{ name }}</span>
              </span>
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
    <q-btn
      color="white"
      text-color="black"
      label="Update"
      :disabled="!formIsFilled()"
      @click="updateTimeOffRequest()"
    />
  </div>
</template>

<script setup lang="ts">

import { onMounted, ref, Ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { getRoutePk } from 'src/utils'
import {
  EmployeeConflictingResponsibilities, TimeOffRequestDates
} from 'src/types'
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

// TODO: Do a valuesAreChanged thing like with ReviewNoteDetail so we aren't
// always resetting acknowledgements unnecessarily

function conflictingResponsibilities():
  Array<EmployeeConflictingResponsibilities>
{
  return timeOffStore.conflictingResponsibilities
}

function dateChanged(): void {
  // Check if there are any coworkers out with shared responsibilities
  if (dates.value) {
    timeOffStore.getConflictingResponsibilites({ dates: dates.value })
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
      dateChanged()
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
          console.error(
            'Error navigating to My Requests page after creating TOR:',
            e
          )
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

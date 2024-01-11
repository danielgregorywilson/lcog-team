<template>
  <q-page>
    <div class="q-px-md">
      <h4>Edit this Note</h4>
      <p>
        Notes are visible to you when completing an evalutation for the
        employee. They are not visible to anyone else.
      </p>
      <q-select
        v-model="employee" :options="options" label="Employee" class="q-pb-md"
      />
      <q-input
        input-class="review-note"
        v-model="note"
        label="Review Note"
        type="textarea"
        class="q-pb-md"
      />
      <q-btn
        color="white"
        id="review-note-update-button"
        text-color="black"
        label="Update"
        :disabled="!valuesAreChanged()"
        @click="updateReviewNote()"
      />
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { onMounted, ref, Ref } from 'vue'
import { useRoute } from 'vue-router'

import { usePeopleStore } from 'src/stores/people'
import { useUserStore } from 'src/stores/user'
import { usePerformanceReviewStore } from 'src/stores/performancereview'
import { getRoutePk } from 'src/utils'

interface EmployeeOption {
  label: string;
  pk: number;
}

const route = useRoute()
const peopleStore = usePeopleStore()
const performanceReviewStore = usePerformanceReviewStore()
const userStore = useUserStore()

const notePk = ref('')
let options = ref([]) as Ref<Array<EmployeeOption>>
let employee = ref({label: '', pk: -1}) as Ref<EmployeeOption>
let employeeCurrentVal = ref({label: '', pk: -1}) as Ref<EmployeeOption>
let note = ref('')
let noteCurrentVal = ref('')

function getOptions(): void {
  peopleStore.getDirectReports(userStore.getEmployeeProfile.employee_pk)
    .then((employees) => {
      options.value = employees.map(obj => {
        return {label: obj.name, pk: obj.pk}
      })
    })
    .catch(e => {
      console.error('Error getting direct reports:', e)
    })
}

function valuesAreChanged(): boolean {
  if (
    employee.value.pk == employeeCurrentVal.value.pk &&
      note.value == noteCurrentVal.value
  ) {
    return false
  } else {
    return true
  }
}

function updateReviewNote(): void {
  performanceReviewStore.updateReviewNote({
    pk: parseInt(notePk.value),
    employee_pk: employee.value.pk,
    note: note.value
  })
    .then((reviewNote) => {
      employeeCurrentVal.value = {
        label: reviewNote.employee_name, pk: reviewNote.employee_pk
      }
      noteCurrentVal.value = reviewNote.note
    })
}

function retrieveReviewNote(): void {
  const routePk = getRoutePk(route)
  if (routePk) {
    notePk.value = routePk
    performanceReviewStore.getReviewNote(routePk)
      .then((reviewNote) => {
        employee.value = {
          label: reviewNote.employee_name, pk: reviewNote.employee_pk
        }
        note.value = reviewNote.note
        employeeCurrentVal.value = employee.value
        noteCurrentVal.value = note.value
      })
  }
}

onMounted(() => {
  retrieveReviewNote();
  getOptions();
})
</script>

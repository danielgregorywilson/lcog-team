<template>
  <q-page>
    <div class="q-px-md">
      <h4>Add a New Note</h4>
      <p>
        Notes are visible to you when completing an evalutation for the
        employee. They are not visible to anyone else.
      </p>
      <q-select
        v-model="employee"
        :options="options"
        label="Employee"
        class="q-pb-md"
      />
      <q-input
        input-class="review-note"
        v-model="note"
        label="Review Note"
        type="textarea"
        class="q-pb-md"
      />
      <q-btn
        id="review-note-create-button"
        color="white"
        text-color="black"
        label="Create"
        :disabled="!formIsFilled()"
        @click="createReviewNote()"
      />
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { Notify } from 'quasar'
import { onMounted, ref, Ref, watch } from 'vue'
import { useRouter } from 'vue-router'

import useEventBus from 'src/eventBus'
import { usePeopleStore } from 'src/stores/people'
import { usePerformanceReviewStore } from 'src/stores/performancereview'
import { useUserStore } from 'src/stores/user'

interface EmployeeOption {
  label: string;
  pk: number;
}

const router = useRouter()
const { bus } = useEventBus()
const peopleStore = usePeopleStore()
const performanceReviewStore = usePerformanceReviewStore()
const userStore = useUserStore()

let options = ref([]) as Ref<Array<EmployeeOption>>
let employee = ref({label: '', pk: -1}) as Ref<EmployeeOption>
let note = ref('')

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

function formIsFilled(): boolean {
  if (!!employee.value.pk && !!note.value) {
    return true
  } else {
    return false
  }
}

function createReviewNote(): void {
  performanceReviewStore.createReviewNote({
    employee_pk: employee.value.pk,
    note: note.value,
  })
    .then(() => {
      router.push({ name: 'reviews' })
        .then(() => {
          Notify.create('Created a review note.')
        })
        .catch(e => {
          console.error(
            'Error navigating to dashboard after creating review note:', e
          )
        })
    })
    .catch(e => {
      console.error('Error creating review note:', e)
    })
}

watch(() => bus.value.get('gotUserProfile'), () => {
  getOptions()
})

onMounted(() => {
  if (userStore.isProfileLoaded) {
    getOptions()
  }
})
</script>

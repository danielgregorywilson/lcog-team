<template>
<q-select
  v-model="selectedEmployee"
  :options="employees()"
  option-value="pk"
  option-label="name"
  :label="label"
  use-input
  hide-selected
  fill-input
  input-debounce="500"
  @filter="filterFn"
  @update:model-value="emit('input', selectedEmployee)"
>
  <template v-slot:no-option>
    <q-item>
      <q-item-section class="text-grey">
        No results
      </q-item-section>
    </q-item>
  </template>
  <template v-if="selectedEmployee.name" v-slot:append>
    <q-icon name="cancel" @click.stop="clearEmployee()" class="cursor-pointer" />
  </template>
</q-select>
</template>

<script setup lang="ts">
import { onMounted, onUpdated, ref } from 'vue'

import { useUserStore } from 'src/stores/user'

const userStore = useUserStore()

const emptyEmployee = {name: '', pk: -1}

const props = defineProps<{
  label: string,
  employee: {name: string, pk: number},
}>()

const emit = defineEmits<{
  (e: 'clear'): void
  (e: 'input', arg: {name: string, pk: number}): void
}>()

let needle = ref('') // For filtering employee list
let selectedEmployee = ref(emptyEmployee)

function retrieveSimpleEmployeeList(): void {
  userStore.getSimpleEmployeeList()
    .catch(e => {
      console.error('Error retrieving simple employee list', e)
    })
}

function employees() {    
  const employees = userStore.simpleEmployeeList
  return employees.filter((employee) => {
    return employee.name.toLowerCase().indexOf(needle.value) != -1
  })
}

function filterFn (val: string, update: Function) { // eslint-disable-line @typescript-eslint/ban-types
  update(() => {
    needle.value = val.toLowerCase()
  })
}

function clearEmployee() {
  selectedEmployee.value = emptyEmployee
  emit('clear')
}

onMounted(() => {
  if (!employees().length) {
    retrieveSimpleEmployeeList()
  }
  selectedEmployee.value = props.employee
})

onUpdated(() => {
  selectedEmployee.value = props.employee
})
</script>

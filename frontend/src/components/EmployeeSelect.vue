<template>
<q-select
  v-model="selectedEmployee"
  :options="employees()"
  option-value="pk"
  :option-label="selectOptionLabel()"
  :label="label"
  :readonly = "readOnly"
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
  <template v-if="!readOnly && selectedEmployeeName()" v-slot:append>
    <q-icon
      name="cancel"
      @click.stop="clearEmployee()"
      class="cursor-pointer"
    />
  </template>
</q-select>
</template>

<script setup lang="ts">
import { onMounted, onUpdated, ref } from 'vue'

import { usePeopleStore } from 'src/stores/people'
import { emptyEmployee, SimpleEmployee } from 'src/types'

const peopleStore = usePeopleStore()

const props = defineProps<{
  label: string,
  employee?: SimpleEmployee,
  useLegalName: boolean
  readOnly: boolean
  employeeFilterFn?: (employee: SimpleEmployee) => boolean
}>()

const emit = defineEmits<{
  (e: 'clear'): void
  (e: 'input', arg: SimpleEmployee): void
}>()

let needle = ref('') // For filtering employee list
let selectedEmployee = ref(emptyEmployee)

function selectOptionLabel(): string {
  if (props.useLegalName) {
    return 'legal_name'
  } else {
    return 'name'
  }
}

function selectedEmployeeName(): string {
  if (props.useLegalName) {
    return selectedEmployee.value?.legal_name
  } else {
    return selectedEmployee.value?.name
  }
}

function retrieveSimpleEmployeeList(): void {
  peopleStore.getSimpleEmployeeList()
    .catch(e => {
      console.error('Error retrieving simple employee list', e)
    })
}

function employees() {    
  let employeesList = peopleStore.simpleEmployeeList
  if (props.employeeFilterFn) {
    employeesList = employeesList.filter(props.employeeFilterFn)
  }
  return employeesList.filter((employee) => {
    if (props.useLegalName) {
      return employee.legal_name.toLowerCase().indexOf(needle.value) != -1
    } else {
      return employee.name.toLowerCase().indexOf(needle.value) != -1
    }
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

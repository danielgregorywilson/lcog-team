<template>
  <div>
    <div>
      <q-btn-toggle
        :model-value="displayEmployeeSecondaryResponsibilities"
        class="q-mb-sm"
        no-caps
        rounded
        unelevated
        toggle-color="primary"
        color="white"
        text-color="primary"
        :options="[
          {label: 'Primary', value: false},
          {label: 'Secondary', value: true}
        ]"
        @click="toggleResponsibilityType()"
      />
    </div>

    <ResponsibilityTable
      v-if="!displayEmployeeSecondaryResponsibilities"
      :tableTitle="`Responsibilities for ${employeeName()}`"
      :tableRows="employeePrimaryResponsibilities()"
      :tableColumns="tableColumns"
    />
    <ResponsibilityTable
      v-if="displayEmployeeSecondaryResponsibilities"
      :tableTitle="`Secondary Responsibilities for ${employeeName()}`"
      :tableRows="employeeSecondaryResponsibilities()"
      :tableColumns="tableColumns"
    />
  </div>
</template>

<style lang="scss">
.q-table {
  .table-description {
    white-space: normal;
  }
  .table-link {
    white-space: normal;
  }
  .table-tags {
    white-space: normal;
  }
}

@media only screen and (max-width: 1600px) {
  .q-table td {
    white-space: normal;
  }
}
</style>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { QTableProps } from 'quasar'

import ResponsibilityTable from 'src/components/responsibilities/ResponsibilityTable.vue'
import { usePeopleStore } from 'src/stores/people'
import { useResponsibilityStore } from 'src/stores/responsibility'
import { Responsibility } from 'src/types'
import { getRoutePk } from 'src/utils'

const route = useRoute()
const router = useRouter()
const peopleStore = usePeopleStore()
const responsibilityStore = useResponsibilityStore()

function secondary() {
  const routeParts = route.path.split('/')
  return routeParts[routeParts.length - 1] === 'secondary'
}

function employeeName(): string {
  return peopleStore.simpleEmployeeDetail.name
}

let displayEmployeeSecondaryResponsibilities = ref(false)

const tableColumns: QTableProps['columns'] = [
  { name: 'name', required: true, label: 'Name', field: 'name', sortable: true, align: 'left' },
  { name: 'description', required: false, label: 'Description', field: 'description', sortable: false, align: 'left', classes: 'table-description', headerClasses: 'table-description' },
  { name: 'link', required: false, label: 'Link', field: 'link', sortable: false, align: 'left', classes: 'table-link', headerClasses: 'table-link' },
  { name: 'tags', required: false, label: 'Tags', field: 'tags', sortable: false, align: 'left', classes: 'table-tags', headerClasses: 'table-tags' },
  { name: 'primary_employee_name', label: 'Primary Employee', field: 'primary_employee_name', sortable: true },
  { name: 'secondary_employee_name', label: 'Secondary Employee', field: 'secondary_employee_name', sortable: true },
  { name: 'actions', label: 'Actions', field: null },
]

function toggleResponsibilityType(): void {
  let routeName
  if (secondary()) {
    routeName = 'employee-responsibilities'
  } else {
    routeName = 'employee-secondary-responsibilities'
  }
  router.push({ name: routeName, params: { pk: route.params.pk }})
    .catch(e => {
      console.error('Error navigating to employee\'s other responsibilities:', e)
    })
}

function retrieveEmployeeName(): void {
  const pk = getRoutePk(route)
  if (pk) {
    peopleStore.getSimpleEmployeeDetail({pk})
    .catch(e => {
      console.error('Error retrieving simple employee detail', e)
    })  
  }
}

function employeeResponsibilities(secondary=false): Array<Responsibility> {
  let allEmployeeResponsibilities
  if (secondary) {
    allEmployeeResponsibilities = responsibilityStore.employeeSecondaryResponsibilities
  } else {
    allEmployeeResponsibilities = responsibilityStore.employeePrimaryResponsibilities
  }
  const pk = getRoutePk(route)
  if (!pk) {
    return []
  }
  const thisEmployeeResponsibilities = allEmployeeResponsibilities.filter((list) => list.pk == parseInt(pk, 10))
  if (thisEmployeeResponsibilities.length && thisEmployeeResponsibilities[0].responsibilities) {
    return thisEmployeeResponsibilities[0].responsibilities
  } else {
    return []
  }
}

function employeePrimaryResponsibilities(): Array<Responsibility> {
  return employeeResponsibilities()
}

function employeeSecondaryResponsibilities(): Array<Responsibility> {
  return employeeResponsibilities(true)
}

function retrieveEmployeeResponsibilites(employeePk: string): void {
  responsibilityStore.getEmployeePrimaryResponsibilities({pk: employeePk})
    .catch(e => {
      console.error('Error retrieving employee responsibilities', e)
    })
}

function retrieveEmployeeSecondaryResponsibilites(employeePk: string): void {
  responsibilityStore.getEmployeeSecondaryResponsibilities({pk: employeePk})
    .catch(e => {
      console.error('Error retrieving employee secondary responsibilities', e)
    })
}

onMounted(() => {
  retrieveEmployeeName()
  if (secondary()) {
    displayEmployeeSecondaryResponsibilities.value = true 
  }
  const pk = getRoutePk(route)
  if (pk) {
    retrieveEmployeeResponsibilites(pk)
    retrieveEmployeeSecondaryResponsibilites(pk)
  }
})
</script>

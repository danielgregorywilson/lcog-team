<template>
  <div>
    <ResponsibilityTable
      tableTitle="Orphaned Responsibilities"
      :tableRows=orphanedResponsibilities()
      :tableColumns=tableColumns
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
import { onMounted } from 'vue'
import { QTableProps } from 'quasar'

import ResponsibilityTable from 'src/components/responsibilities/ResponsibilityTable.vue'
import { useResponsibilityStore } from 'src/stores/responsibility'
import { Responsibility } from 'src/types'

const responsibilityStore = useResponsibilityStore()

function orphanedResponsibilities(): Array<Responsibility> {
  return responsibilityStore.orphanedResponsibilities
}

const tableColumns: QTableProps["columns"] = [
  { name: 'name', required: true, label: 'Name', field: 'name', sortable: true, align: 'left' },
  { name: 'description', required: false, label: 'Description', field: 'description', sortable: false, align: 'left', classes: 'table-description', headerClasses: 'table-description' },
  { name: 'link', required: false, label: 'Link', field: 'link', sortable: false, align: 'left', classes: 'table-link', headerClasses: 'table-link' },
  { name: 'tags', required: false, label: 'Tags', field: 'tags', sortable: false, align: 'left', classes: 'table-tags', headerClasses: 'table-tags' },
  { name: 'primary_employee_name', label: 'Primary Employee', field: 'primary_employee_name', sortable: true },
  { name: 'secondary_employee_name', label: 'Secondary Employee', field: 'secondary_employee_name', sortable: true },
  { name: 'actions', label: 'Actions', field: null },
]

function retrieveOrphanedResponsibilites(): void {
  responsibilityStore.getOrphanedResponsibilities()
    .catch(e => {
      console.error('Error retrieving orphaned responsibilities', e)
    })
}

onMounted(() => {
  // TODO: Only fetch if doesn't exist, or needs update?
  retrieveOrphanedResponsibilites()
})
</script>

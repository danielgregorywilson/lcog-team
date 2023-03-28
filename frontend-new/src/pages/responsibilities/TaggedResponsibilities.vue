<template>
  <ResponsibilityTable
    :tableTitle="`${tagName()} Responsibilities`"
    :tableRows="tagResponsibilities()"
    :tableColumns="tableColumns"
  />
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { QTableProps } from 'quasar'

import ResponsibilityTable from 'src/components/responsibilities/ResponsibilityTable.vue'
import { useResponsibilityStore } from 'src/stores/responsibility'
import { getRoutePk } from 'src/utils'

const route = useRoute()
const responsibilityStore = useResponsibilityStore()


const tableColumns: QTableProps["columns"] = [
  { name: 'name', required: true, label: 'Name', field: 'name', sortable: true, align: 'left' },
  { name: 'description', required: false, label: 'Description', field: 'description', sortable: false, align: 'left' },
  { name: 'link', required: false, label: 'Link', field: 'link', sortable: false, align: 'left' },
  { name: 'tags', required: false, label: 'Tags', field: 'tags', sortable: false, align: 'left' },
  { name: 'primary_employee_name', label: 'Primary Employee', field: 'primary_employee_name', sortable: true },
  { name: 'secondary_employee_name', label: 'Secondary Employee', field: 'secondary_employee_name', sortable: true },
  { name: 'actions', label: 'Actions', field: null },
]

function tagName(): string {
  return responsibilityStore.tagWithResponsibilities.name
}

function retrieveTagWithResponsibilities(): void {
  const pk = getRoutePk(route)
  if (!pk) {
    return
  }
  responsibilityStore.getTagWithResponsibilities(pk)
    .catch(e => {
      console.error('Error retrieving tag data', e)
    })
}

function tagResponsibilities() {
  return responsibilityStore.tagWithResponsibilities.responsibilities || []
} 

onMounted(() => {
  retrieveTagWithResponsibilities()
})
</script>

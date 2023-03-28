<template>
  <q-table
    :title="`Tags`"
    :rows="allTags()"
    :columns="tableColumns"
    :pagination="initialTablePagination"
    :filter="tableFilter"
    :filter-method="tableFilterMethod"
    row-key="pk"
  >
    <template v-slot:top-right>
      <q-input borderless dense clearable debounce="300" v-model="tableFilter" placeholder="Search">
        <template v-slot:prepend>
          <q-icon name="search">
            <q-tooltip>
              Type to search on Name, Description, or Tag name
            </q-tooltip>
          </q-icon>
        </template>
      </q-input>
    </template>
    <template v-slot:body="props">
      <q-tr :props="props">
        <q-td key="name" :props="props">
          <q-chip clickable @click="navigateToTag(props.row.pk)" color="secondary" text-color="white">{{ props.row.name }}</q-chip>
        </q-td>
        <q-td key="actions" :props="props">
          <q-btn class="col edit-button" dense round flat color="grey" @click="showEditDialog(props.row)" icon="edit"></q-btn>
          <q-btn class="col delete-button" dense round flat color="grey" @click="showDeleteDialog(props.row)" icon="delete"></q-btn>
        </q-td>
      </q-tr>
    </template>
  </q-table>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { QTableProps } from 'quasar'

import useEventBus from 'src/eventBus';
import shared from 'src/pages/responsibilities/shared'
import { useResponsibilityStore } from 'src/stores/responsibility'
import { Responsibility, ResponsibilityTag } from 'src/types'

const router = useRouter()
const responsibilityStore = useResponsibilityStore()
const bus = useEventBus()

let tableFilter = ref('')

const tableColumns: QTableProps["columns"] = [
  { name: 'name', required: true, label: 'Name', field: 'name', sortable: true, align: 'left' },
  { name: 'actions', label: 'Actions', field: null }
]

const initialTablePagination = {
  rowsPerPage: 50
}

function allTags(): Array<ResponsibilityTag> {
  const allTags = responsibilityStore.allTags
  return allTags.results
}

function retrieveTags(): void {
  responsibilityStore.getAllTags()
    .catch(e => {
      console.error('Error retrieving tags', e)
    })
}

function tableFilterMethod(rows: Array<Responsibility>, term: string) {
  return shared.tableFilterMethod(rows, term, ['name',])
}

function navigateToTag(tagPk: string): void {
  router.push({ name: 'tagged-responsibilities', params: { pk: tagPk }})
    .catch(e => {
      console.error('Error navigating to tag detail:', e)
    })
}

function showEditDialog(row: Responsibility): void {
  bus.emit('emitOpenEditTagDialog', row) // eslint-disable-line @typescript-eslint/no-unsafe-call, @typescript-eslint/no-unsafe-member-access
}

function showDeleteDialog(row: Responsibility): void {
  bus.emit('emitOpenDeleteTagDialog', row) // eslint-disable-line @typescript-eslint/no-unsafe-call, @typescript-eslint/no-unsafe-member-access
}

onMounted(() => {
  retrieveTags()
})
</script>

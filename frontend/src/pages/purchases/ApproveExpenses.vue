<template>
<div class="q-mt-md">
  <div class="q-mt-md">
    <q-spinner-grid
      v-if="!expensesLoaded"
      class="spinner"
      color="primary"
      size="xl"
    />
    <q-table
      v-else
      flat bordered
      :title="tableTitleDisplay()"
      :rows="selectedMonthExpenses()"
      :columns="columns"
      row-key="name"
      binary-state-sort
      :pagination="pagination"
      class="expense-table"
    >
      <template v-slot:body-cell-purchaser="props">
        <q-td key="purchaser" :props="props">
          {{ props.row.purchaser.name }}
        </q-td>
      </template>
      <template v-slot:body-cell-date="props">
        <q-td key="date" :props="props">
          {{ readableDateNEW(props.row.date) }}
        </q-td>
      </template>
      <template v-slot:body-cell-gls="props">
        <q-td key="gls" :props="props">
          <div
            class="text-pre-wrap"
            v-for="gl in props.row.gls"
            :key="props.row.gls.indexOf(gl)"
          >
            {{ gl.gl }}: {{ gl.percent }}%
          </div>
        </q-td>
      </template>
      <template v-slot:body-cell-receipt="props">
        <q-td key="receipt" :props="props">
          <DocumentViewer
            v-if="props.row.receipt"
            :documentUrl="props.row.receipt"
          />
        </q-td>
      </template>
      <template v-slot:body-cell-approve="props">
        <q-td :props="props" class="row justify-center items-center">
          <q-btn 
            dense round color="red" icon="close"
            :outline="['submitted', 'approver_approved'].indexOf(props.row.status) > -1"
            :disable="!canApprove || props.row.status == 'approver_denied'"
            class="q-mr-sm"
            @click="approveExpense(props.row.pk, false)"
          />
          <q-btn
            dense round color="green" icon="check"
            :outline="['submitted', 'approver_denied'].indexOf(props.row.status) > -1"
            :disable="!canApprove || props.row.status == 'approver_approved'"
            @click="approveExpense(props.row.pk, true)"
          />
        </q-td>
      </template>
    </q-table>
  </div>
</div>
</template>

<style scoped lang="scss">

</style>

<script setup lang="ts">
import { onMounted, ref } from 'vue'

import DocumentViewer from 'src/components/DocumentViewer.vue'
import { readableDateNEW } from 'src/filters'
import { handlePromiseError } from 'src/stores'
import { usePurchaseStore } from 'src/stores/purchase'
import { Expense } from 'src/types'

const purchaseStore = usePurchaseStore()

const props = defineProps<{
  monthDisplay: string
  dayInt: number
  monthInt: number
  yearInt: number
}>()

let thisMonthLoaded = ref(false)
let allExpensesLoaded = ref(false)

let firstOfThisMonth = ref(new Date())
let firstOfSelectedMonth = ref(new Date())

const canApprove = ref(true)

const pagination = {
  rowsPerPage: '50'
}

const columns = [
  { 
    name: 'purchaser', field: 'purchaser', label: 'Purchaser', required: true,
    align: 'left', sortable: true
  },
  {
    name: 'name', field: 'name', label: 'Name', required: true, align: 'left',
    sortable: true
  },
  {
    name: 'date', field: 'date', label: 'Date', align: 'center', sortable: true
  },
  {
    name: 'job', field: 'job', label: 'Job #', align: 'center', sortable: true
  },
  {
    name: 'gls', field: 'gls', label: 'GL Codes', align: 'center',
    sortable: true, style: 'width: 10px'
  },
  { name: 'receipt', field: 'receipt', label: 'Receipt', align: 'center' },
  { name: 'approve', label: 'Approve?', field: 'approved', align: 'center' },
]

function viewingThisMonth() {
  return firstOfSelectedMonth.value.getTime() ===
    firstOfThisMonth.value.getTime()
}

function expensesLoaded() {
  return (viewingThisMonth() && thisMonthLoaded.value) ||
    allExpensesLoaded.value
}

function tableTitleDisplay(): string {
  return `${props.monthDisplay} - Expenses to Approve`
}

function selectedMonthExpenses(): Expense[] {
  const apiResults = purchaseStore.approvalExpenses
  let exps: Expense[] = []
  if (apiResults) {
    exps = apiResults.filter(exp => {
      let [y, m] = exp.date.split('-').map(s => parseInt(s))
      return m === props.monthInt && y === props.yearInt
    })
  }
  return exps
}

function retrieveThisMonthExpensesToApprove(): Promise<void> {
  return new Promise((resolve, reject) => {
    purchaseStore.getApprovalExpenses(props.yearInt, props.monthInt)
      .then(() => {
        thisMonthLoaded.value = true
        resolve()
      })
      .catch((error) => {
        handlePromiseError(reject, 'Error retrieving expenses', error)
        reject()
      })
  })
}

function retrieveAllExpensesToApprove(): Promise<void> {
  return new Promise((resolve, reject) => {
    purchaseStore.getApprovalExpenses()
      .then(() => {
        allExpensesLoaded.value = true
        resolve()
      })
      .catch((error) => {
        handlePromiseError(reject, 'Error retrieving expenses', error)
        reject()
      })
  })
}

function updateExpense(row: Expense) {
  purchaseStore.updateExpense(row)
    .catch((error) => {
      console.log('Error updating expense', error)
    })
}

function updateName(pk: number, val: string) {
  const exp = purchaseStore.myExpenses.find(exp => exp.pk === pk)
  if (exp) {
    exp.name = val
    updateExpense(exp)
  }
}

function approveExpense(pk: number, approved: boolean) {
  canApprove.value = false
  setTimeout(() => {
    canApprove.value = true
  }, 1500)
  purchaseStore.approveExpense(pk, approved)
    .then(() => {
      retrieveAllExpensesToApprove()
    })
    .catch((error) => {
      console.log('Error approving expense', error)
    })
}

function setDates() {
  let theFirst = new Date()
  theFirst.setDate(1)
  theFirst.setHours(0,0,0,0)
  firstOfThisMonth.value = theFirst
  firstOfSelectedMonth.value = theFirst
}

onMounted(() => {
  setDates()
  retrieveThisMonthExpensesToApprove().then(() => {
    retrieveAllExpensesToApprove()
  })
})

</script>

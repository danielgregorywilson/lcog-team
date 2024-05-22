<template>
<div class="q-mt-md">
  <div class="q-mt-md">
    <q-spinner-grid
      v-if="!expensesLoaded"
      class="spinner"
      color="primary"
      size="xl"
    />
    <div v-else>
      <q-table
        flat bordered
        :title="monthDisplay"
        :rows="rows"
        :columns="columns"
        row-key="name"
        binary-state-sort
        :pagination="pagination"
        class="expense-table"
      >
        <template v-slot:body="props">
          <q-tr :props="props" :no-hover="!props.row.submitted" @click="navigateToDetail(props.row.submitted, props.row.employeePk)">
            <q-td key="employee" :props="props">
              {{ props.row.employee }}
            </q-td>
            <q-td key="submitted" :props="props">
              <q-icon v-if="props.row.submitted" name="check" size="lg" />
            </q-td>
            <q-td key="approved" :props="props">
              <q-icon v-if="props.row.approved==true" color="green" name="check_circle" size="lg" />
              <q-icon v-else-if="props.row.approved==false" color="red" name="cancel" size="lg" />
            </q-td>
          </q-tr>
        </template>
      </q-table>
    </div>
  </div>
</div>
</template>

<style scoped lang="scss"></style>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { handlePromiseError } from 'src/stores'
import { usePurchaseStore } from 'src/stores/purchase';

// type Expense = {date: string, isToday: boolean}

const router = useRouter()
const purchaseStore = usePurchaseStore()

const props = defineProps<{
  monthDisplay: string
  monthInt: number
  yearInt: number
}>()

let thisMonthLoaded = ref(false)
let allExpensesLoaded = ref(false)

let firstOfThisMonth = ref(new Date())
let firstOfSelectedMonth = ref(new Date())

const pagination = {
  rowsPerPage: '50'
}

const columns = [
  { name: 'employee', required: true, label: 'Name', align: 'left' },
  { name: 'submitted', label: 'Submitted', field: 'submitted', sortable: true, align: 'center'},
  { name: 'approved', label: 'Approved', field: 'approved', sortable: true, align: 'center' }
]

const rows = ref([
  {
    employee: 'Dan Wilson',
    employeePk: 1,
    submitted: true,
    approved: true
  },
  {
    employee: 'Dan Hogue',
    employeePk: 2,
    submitted: true,
    approved: false
  },
  {
    employee: 'Andy Smith',
    employeePk: 3,
    submitted: false,
    approved: null
  }
])

function viewingThisMonth() {
  return firstOfSelectedMonth.value.getTime() ===
    firstOfThisMonth.value.getTime()
}

function expensesLoaded() {
  return (viewingThisMonth() && thisMonthLoaded.value) ||
    allExpensesLoaded.value
}

function retrieveThisMonthExpenses(): Promise<void> {
  return new Promise((resolve, reject) => {
    purchaseStore.getFiscalExpenseMonths(props.yearInt, props.monthInt)
      .then(() => {
        thisMonthLoaded.value = true
        resolve()
      })
      .catch((error) => {
        handlePromiseError(reject, 'Error retrieving fiscal expenses', error)
        reject()
      })
  })
}

function retrieveAllExpenses(): Promise<void> {
  return new Promise((resolve, reject) => {
    purchaseStore.getFiscalExpenseMonths()
      .then(() => {
        allExpensesLoaded.value = true
        resolve()
      })
      .catch((error) => {
        handlePromiseError(reject, 'Error retrieving fiscal expenses', error)
        reject()
      })
  })
}

function navigateToDetail(submitted: boolean, employeePk: number) {
  if (submitted) {
    router.push({
      name: 'expenses-review-detail',
      params: {
        employeePk: employeePk.toString(),
        month: props.monthInt,
        year: props.yearInt
      }
    })
    .catch(e => {
      console.error('Error navigating to time off request detail:', e)
    })
  }
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
  retrieveThisMonthExpenses().then(() => {
    retrieveAllExpenses()
  })
})

</script>

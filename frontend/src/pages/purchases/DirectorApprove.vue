<template>
<div class="q-mt-md">
  <div class="q-mt-md">
    <q-spinner-grid
      v-if="!EMsLoaded()"
      class="spinner"
      color="primary"
      size="xl"
    />
    <div v-else>
      <q-table
        flat bordered
        :title="monthDisplay"
        :rows="selectedMonthExpenseMonths()"
        :columns="columns"
        row-key="name"
        binary-state-sort
        :pagination="pagination"
        class="expense-table"
        no-data-label="No expenses entered this month"
      >
        <template v-slot:body="props">
          <q-tr
            :props="props"
            :no-hover="!expenseMonthManagerApproved(props.row)"
            class="cursor-pointer"
            @click="navigateToDetail(props.row.purchaser.pk)"
          >
            <q-td key="employee" :props="props">
              {{ props.row.purchaser.name }}
            </q-td>
            <q-td key="status" :props="props">
              <q-linear-progress
                size="25px"
                rounded
                :value="progressBarSize(props.row.status)"
                :color="progressBarColor(props.row.status)"
              >
                <div class="absolute-full flex flex-center">
                  <q-badge
                    color="white"
                    :text-color="progressBarColor(props.row.status)"
                    :label="progressBarLabel(props.row.status)"
                  />
                </div>
              </q-linear-progress>
            </q-td>
            <q-td key="approved" :props="props">
              <q-icon
                v-if="expenseMonthDirectorApproved(props.row)"
                color="green"
                name="check_circle"
                size="lg"
              />
              <q-icon
                v-else-if="expenseMonthDirectorDenied(props.row)"
                color="red"
                name="cancel"
                size="lg"
              />
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
import { ExpenseMonth } from 'src/types';

const router = useRouter()
const purchaseStore = usePurchaseStore()

const props = defineProps<{
  monthDisplay: string
  monthInt: number
  yearInt: number
}>()

let thisMonthEMsLoaded = ref(false)
let allEMsLoaded = ref(false)

let firstOfThisMonth = ref(new Date())
let firstOfSelectedMonth = ref(new Date())

const pagination = {
  rowsPerPage: 50
}

const columns = [
  {
    name: 'employee', required: true, label: 'Name', sortable: true,
    align: 'left'
  },
  {
    name: 'status', label: 'Status', field: 'status', sortable: true,
    align: 'center'
  },
  {
    name: 'approved', label: 'Director Approved', field: 'approved',
    sortable: true, align: 'center'
  }
]

function viewingThisMonth() {
  return firstOfSelectedMonth.value.getTime() ==
    firstOfThisMonth.value.getTime()
}

function EMsLoaded() {
  return (viewingThisMonth() && thisMonthEMsLoaded.value) || allEMsLoaded.value
}

function selectedMonthExpenseMonths() {
  return purchaseStore.directorExpenseMonths
    .filter(em => em.month == props.monthInt && em.year == props.yearInt)
}

function expenseMonthManagerApproved(expenseMonth: ExpenseMonth) {
  return [
    'approver_approved', 'director_approved', 'director_denied',
    'fiscal_approved', 'fiscal_denied'
  ]
    .includes(expenseMonth.status)
}

function expenseMonthDirectorApproved(em: ExpenseMonth) {
  return em.director_approved && em.director_approved_at != null
}

function expenseMonthDirectorDenied(em: ExpenseMonth) {
  return !em.director_approved && em.director_approved_at != null
}

function progressBarSize(status: string) {
  switch (status) {
    case 'draft':
      return 0
    case 'submitted':
    case 'approver_denied':
      return .25
    case 'approver_approved':
    case 'director_denied':
      return .5
    case 'director_approved':
    case 'fiscal_denied':
      return .75
    case 'fiscal_approved':
      return 1
    default:
      return 0
  }
}

function progressBarLabel(status: string) {
  switch (status) {
    case 'draft':
      return 'Not Submitted'
    case 'submitted':
      return 'Submitted by Employee'
    case 'approver_denied':
      return 'Denied by Manager'
    case 'approver_approved':
      return 'Approved by Manager'
    case 'director_denied':
      return 'Denied by Director'
    case 'director_approved':
      return 'Approved by Director'
    case 'fiscal_denied':
      return 'Denied by Fiscal'
    case 'fiscal_approved':
      return 'Approved by Fiscal'
    default:
      return 'Unknown'
  }
}

function progressBarColor(status: string) {
  switch (status) {
    case 'draft':
      return 'grey'
    case 'submitted':
      return 'blue'
    case 'approver_denied':
    case 'director_denied':
    case 'fiscal_denied':
      return 'red'
    case 'approver_approved':
    case 'director_approved':
    case 'fiscal_approved':
      return 'green'
    default:
      return 'grey'
  }
}

function retrieveThisMonthEMs(): Promise<void> {
  return new Promise((resolve, reject) => {
    purchaseStore.getDirectorExpenseMonths(props.yearInt, props.monthInt)
      .then(() => {
        thisMonthEMsLoaded.value = true
        resolve()
      })
      .catch((error) => {
        handlePromiseError(reject, 'Error retrieving director expenses', error)
        reject()
      })
  })
}

function retrieveAllEMs(): Promise<void> {
  return new Promise((resolve, reject) => {
    purchaseStore.getDirectorExpenseMonths()
      .then(() => {
        allEMsLoaded.value = true
        resolve()
      })
      .catch((error) => {
        handlePromiseError(reject, 'Error retrieving director expenses', error)
        reject()
      })
  })
}

function navigateToDetail(employeePk: number) {
  router.push({
    name: 'director-approve-expenses-detail',
    params: {
      employeePK: employeePk.toString(),
      year: props.yearInt,
      month: props.monthInt
    }
  })
  .catch(e => {
    console.error('Error navigating to time off request detail:', e)
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
  retrieveThisMonthEMs().then(() => {
    retrieveAllEMs()
  })
})

</script>

<template>
<q-page class="q-pa-md">
  <div class="q-gutter-md">
    <q-btn @click="setThisMonth()">This Month</q-btn>
    <q-btn-group>
      <q-btn color="secondary" icon="west" @click="monthBackward()"/>
      <q-btn color="secondary" icon="east" @click="monthForward()"/>
    </q-btn-group>
  </div>
  <q-spinner-grid
    v-if="!calendarLoaded"
    class="spinner q-mt-lg"
    color="primary"
    size="xl"
  />
  <div v-else class="q-mt-lg">
    <q-table
      flat bordered
      :title="monthDisplay()"
      :rows="rows"
      :columns="columns"
      row-key="name"
      binary-state-sort
      :pagination="pagination"
      class="expense-table"
    >
      <template v-slot:body="props">
        <q-tr :props="props" @click="navigateToDetail(props.row.employeePk)">
          <q-td key="employee" :props="props">
            {{ props.row.employee }}
          </q-td>
          <q-td key="approved" :props="props">
            <q-icon v-if="props.row.approved==true" color="green" name="check_circle" size="lg" class="q-mr-sm" />
            <q-icon v-else-if="props.row.approved==false" color="red" name="cancel" size="lg" class="q-mr-sm" />
          </q-td>
        </q-tr>
      </template>
    </q-table>
  </div>
</q-page>
</template>

<style scoped lang="scss">
  // .expense-table {
  //   width: 221px
  // }
</style>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useQuasar } from 'quasar'
import { useRouter } from 'vue-router'
import { useTimeOffStore } from 'src/stores/timeoff'

type Expense = {date: string, isToday: boolean}

const quasar = useQuasar()
const router = useRouter()
const timeOffStore = useTimeOffStore()

let submitted = ref(false)
let calendarLoaded = ref(true)
let showSubmitToFiscalDialog = ref(false)
let sendDialogMessage = ref('')
let showUnsubmitDialog = ref(false)

let today = ref(new Date())
let firstOfThisMonth = ref(new Date())
let firstOfSelectedMonth = ref(new Date())

const pagination = {
  rowsPerPage: '50'
}

const columns = [
  { name: 'employee', required: true, label: 'Name', align: 'left' },
  { name: 'approved', label: 'Approved', field: 'approved', align: 'center' }
]

const rows = ref([
  {
    employee: 'Dan Wilson',
    employeePk: 1,
    approved: true
  },
  {
    employee: 'Dan Hogue',
    employeePk: 2,
    approved: false
  },
  {
    employee: 'Andy Smith',
    employeePk: 3,
    approved: null
  }
])

function monthExpenses(): Expense[] {
  return []
  // const apiResults = timeOffStore.teamTimeOffRequests
  // let sortedTimeOff: TimeOffCalendarData = []
  // if (apiResults) {
  //   for (let i=0; i<5; i++) {
  //     let d = new Date(selectedMonday.value.getTime() + i*(1000 * 60 * 60 * 24))
  //     let isToday = d.setHours(0,0,0,0) === today.value.setHours(0,0,0,0)
  //     sortedTimeOff.push({
  //       date: d.toLocaleDateString('en-us', { weekday: 'long', month: 'long', day: 'numeric' }),
  //       isToday: isToday,
  //       requests: apiResults.filter(request => {
  //         const targetDateMS = d.setHours(0,0,0,0)

  //         const fromDate = new Date(request.start_date)
  //         const fromTZOffset = fromDate.getTimezoneOffset() * 60000
  //         const fromDateMS = new Date(fromDate.getTime() + fromTZOffset).setHours(0,0,0,0)

  //         const toDate = new Date(request.end_date)
  //         const toTZOffset = toDate.getTimezoneOffset() * 60000
  //         const toDateMS = new Date(toDate.getTime() + toTZOffset).setHours(0,0,0,0)

  //         if (fromDateMS <= targetDateMS && targetDateMS <= toDateMS) {
  //           return true
  //         } else {
  //           return false
  //         }
  //       })
  //     })
  //   }
  // }
  // return sortedTimeOff
}

function monthDisplay(): string {
  return `${firstOfSelectedMonth.value.toLocaleDateString('en-us', { month: 'long' })} ${firstOfSelectedMonth.value.getFullYear()}`
}

// TODO: This currently gets all time off; should probably just get for a period
function retrieveTeamTimeOff(): void {
  timeOffStore.getTeamTimeOffRequests()
    .then(() => {
      calendarLoaded.value = true
    })
    .catch(e => {
      console.error('Error retrieving team time off', e)
    })
}

function setDates() {
  let firstOfThisMonth = new Date()
  firstOfThisMonth.setDate(1)
  firstOfThisMonth.setHours(0,0,0,0)
  firstOfThisMonth.value = firstOfThisMonth
  firstOfSelectedMonth.value = firstOfThisMonth
}

function setThisMonth() {
  firstOfSelectedMonth.value = firstOfThisMonth.value
}

function monthBackward() {
  firstOfSelectedMonth.value = firstOfSelectedMonth.value.getMonth() === 0
    ? new Date(firstOfSelectedMonth.value.getFullYear() - 1, 11, 1)
    : new Date(firstOfSelectedMonth.value.getFullYear(), firstOfSelectedMonth.value.getMonth() - 1, 1)
}

function monthForward() {
  firstOfSelectedMonth.value = firstOfSelectedMonth.value.getMonth() === 11
    ? new Date(firstOfSelectedMonth.value.getFullYear() + 1, 0, 1)
    : new Date(firstOfSelectedMonth.value.getFullYear(), firstOfSelectedMonth.value.getMonth() + 1, 1)
}

function navigateToDetail(employeePk: number) {
  router.push({
    name: 'expenses-review-detail',
    params: {
      employeePk: employeePk.toString(),
      month: firstOfSelectedMonth.value.getMonth().toString(),
      year: firstOfSelectedMonth.value.getFullYear().toString()
    }
  })
    .catch(e => {
      console.error('Error navigating to time off request detail:', e)
    })
}

onMounted(() => {
  setDates()
  // retrieveTeamTimeOff()
})

</script>

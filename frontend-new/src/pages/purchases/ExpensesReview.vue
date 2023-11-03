<template>
<div class="q-mt-md">
  <div>
    <q-spinner-grid
      v-if="!calendarLoaded"
      class="spinner q-mt-lg"
      color="primary"
      size="xl"
    />
    <div v-else class="q-mt-lg">
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
  </div>
</div>
</template>

<style scoped lang="scss"></style>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

type Expense = {date: string, isToday: boolean}

const router = useRouter()

const props = defineProps<{
  monthDisplay: string
  monthInt: string
  yearInt: string
}>()

let calendarLoaded = ref(true)

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

function navigateToDetail(employeePk: number) {
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

onMounted(() => {
  // retrieveTeamTimeOff()
})

</script>

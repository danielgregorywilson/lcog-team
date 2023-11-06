<template>
<div class="q-mt-md">
  <div class="q-mt-md">
    <q-spinner-grid
      v-if="!calendarLoaded"
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

onMounted(() => {
  // retrieveTeamTimeOff()
})

</script>

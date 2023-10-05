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
    >
      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td key="name" :props="props">
            {{ props.row.name }}
            <q-popup-edit v-model="props.row.name" v-slot="scope">
              <q-input v-model="scope.value" dense autofocus counter @keyup.enter="scope.set" />
            </q-popup-edit>
          </q-td>
          <q-td key="date" :props="props">
            {{ props.row.date }}
            <q-popup-edit v-model="props.row.calories" title="Update date" buttons v-slot="scope">
              <q-input type="date" v-model="scope.value" dense autofocus />
            </q-popup-edit>
          </q-td>
          <q-td key="gl" :props="props">
            <div class="text-pre-wrap">{{ props.row.gl }}</div>
            <q-popup-edit v-model="props.row.gl" v-slot="scope">
              <q-input type="textarea" v-model="scope.value" dense autofocus />
            </q-popup-edit>
          </q-td>
          <q-td key="approver" :props="props">
            {{ props.row.approver }}
            <q-popup-edit v-model="props.row.approver" title="Update approver" buttons persistent v-slot="scope">
              <q-input type="number" v-model="scope.value" dense autofocus hint="Use buttons to close" />
            </q-popup-edit>
          </q-td>
          <q-td key="receipt" :props="props">{{ props.row.receipt }}</q-td>
        </q-tr>
      </template>
    </q-table>
  </div>
</q-page>
</template>

<script setup lang="ts">

import { onMounted, ref } from 'vue'
import { TimeOffRequestRetrieve } from 'src/types'
import { useTimeOffStore } from 'src/stores/timeoff'

type TimeOffCalendarData = Array<{date: string, isToday: boolean, requests: Array<TimeOffRequestRetrieve>}>

const timeOffStore = useTimeOffStore()

let calendarLoaded = ref(true)

let today = ref(new Date())
let firstOfThisMonth = ref(new Date())
let firstOfSelectedMonth = ref(new Date())

const pagination = {
  rowsPerPage: '50'
}

const columns = [
  {
    name: 'name',
    required: true,
    label: 'Name',
    align: 'left',
    field: row => row.name,
    format: val => `${val}`,
    sortable: true
  },
  { name: 'date', align: 'center', label: 'Date', field: 'calories', sortable: true },
  { name: 'gl', label: 'GL Code', field: 'fat', sortable: true, style: 'width: 10px' },
  { name: 'approver', label: 'Approver', field: 'approver' },
  { name: 'receipt', label: 'Receipt', field: 'receipt' }
]

const rows = [
  {
    name: 'Frozen Yogurt',
    date: new Date(),
    gl: '43-45045-232',
    approver: 'Danny',
    receipt: 'file.txt'
  },
  {
    name: 'Ice cream sandwich',
    date: new Date(),
    gl: '43-45045-232',
    approver: 'Danny',
    receipt: 'file.txt'
  },
  {
    name: 'Eclair',
    date: new Date(),
    gl: '43-45045-232',
    approver: 'Danny',
    receipt: 'file.txt'
  },
  {
    name: 'Cupcake',
    date: new Date(),
    gl: '43-45045-232',
    approver: 'Danny',
    receipt: 'file.txt'
  },
  {
    name: 'Gingerbread',
    date: new Date(),
    gl: '43-45045-232',
    approver: 'Danny',
    receipt: 'file.txt'
  },
  {
    name: 'Jelly bean',
    date: new Date(),
    gl: '43-45045-232',
    approver: 'Danny',
    receipt: 'file.txt'
  },
  {
    name: 'Lollipop',
    date: new Date(),
    gl: '43-45045-232',
    approver: 'Danny',
    receipt: 'file.txt'
  },
  {
    name: 'Honeycomb',
    date: new Date(),
    gl: '43-45045-232',
    approver: 'Danny',
    receipt: 'file.txt'
  },
  {
    name: 'Donut',
    date: new Date(),
    gl: '43-45045-232',
    approver: 'Danny',
    receipt: 'file.txt'
  },
  {
    name: 'KitKat',
    date: new Date(),
    gl: '43-45045-232',
    approver: 'Danny',
    receipt: 'file.txt'
  }
]

function monthExpenses(): TimeOffCalendarData {
  const apiResults = timeOffStore.teamTimeOffRequests
  let sortedTimeOff: TimeOffCalendarData = []
  if (apiResults) {
    for (let i=0; i<5; i++) {
      let d = new Date(selectedMonday.value.getTime() + i*(1000 * 60 * 60 * 24))
      let isToday = d.setHours(0,0,0,0) === today.value.setHours(0,0,0,0)
      sortedTimeOff.push({
        date: d.toLocaleDateString('en-us', { weekday: 'long', month: 'long', day: 'numeric' }),
        isToday: isToday,
        requests: apiResults.filter(request => {
          const targetDateMS = d.setHours(0,0,0,0)

          const fromDate = new Date(request.start_date)
          const fromTZOffset = fromDate.getTimezoneOffset() * 60000
          const fromDateMS = new Date(fromDate.getTime() + fromTZOffset).setHours(0,0,0,0)

          const toDate = new Date(request.end_date)
          const toTZOffset = toDate.getTimezoneOffset() * 60000
          const toDateMS = new Date(toDate.getTime() + toTZOffset).setHours(0,0,0,0)

          if (fromDateMS <= targetDateMS && targetDateMS <= toDateMS) {
            return true
          } else {
            return false
          }
        })
      })
    }
  }
  return sortedTimeOff
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

onMounted(() => {
  setDates()
  // retrieveTeamTimeOff()
})

</script>

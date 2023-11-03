<template>
<div class="q-mt-md">
  <div class="row q-gutter-md">
    <div v-if="approved" class="row items-center">
      <q-icon color="green" name="check_circle" size="lg" class="q-mr-sm" />
      <div>Approved</div>
    </div>
    <div v-else-if="denied" class="row items-center">
      <q-icon color="red" name="cancel" size="lg" class="q-mr-sm" />
      <div>Denied</div>
    </div>
  </div>
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
        :title="tableTitleDisplay()"
        :rows="rows"
        :columns="columns"
        row-key="name"
        binary-state-sort
        :pagination="pagination"
        class="expense-table"
      >
        <template v-slot:body="props">
          <q-tr :props="props">
            <q-td key="name" :props="props">
              {{ props.row.name }}
            </q-td>
            <q-td key="date" :props="props">
              {{ readableDate(props.row.date) }}
            </q-td>
            <q-td key="job" :props="props">
              <div class="text-pre-wrap">{{ props.row.job }}</div>
            </q-td>
            <q-td key="gl" :props="props">
              <div class="text-pre-wrap">{{ props.row.gl }}</div>
            </q-td>
            <q-td key="approver" :props="props">
              {{ props.row.approver.name }}
            </q-td>
            <q-td key="receipt" :props="props">
              {{ props.row.receipt }}
            </q-td>
          </q-tr>
        </template>
      </q-table>
      <div class="q-mt-sm q-gutter-md">
        <q-btn :class="approved?'bg-green':''" @click="showApproveDialog = true">Approve Expenses</q-btn>
        <q-btn :class="denied?'bg-red':''" @click="showDenyDialog = true">Deny Expenses</q-btn>
      </div>
    </div>
  </div>

  <!-- Approve Dialog -->
  <q-dialog v-model="showApproveDialog">
    <q-card class="q-pa-md" style="width: 400px">
      <div class="text-h6">Approve {{monthDisplay}} expenses for {{ employeeName }}?</div>
      <q-form
        @submit='onSubmitApproveDialog()'
        class="q-gutter-md"
      >
        <div class="row justify-between">
          <q-btn
            name="approve-dialog-button"
            label="Approve"
            icon-right="check"
            type="submit"
            color="primary"
          />
        </div>
      </q-form>
    </q-card>
  </q-dialog>

  <!-- Deny Dialog -->
  <q-dialog v-model="showDenyDialog">
    <q-card class="q-pa-md" style="width: 400px">
      <div class="text-h6">Deny {{monthDisplay}} expenses for {{ employeeName }}?</div>
      <q-form
        @submit='onSubmitDenyDialog()'
        class="q-gutter-md"
      >
        <q-input
          v-model="denyDialogMessage"
          filled
          type="textarea"
          label="Message to include"
          :rules="[ val => val && val.length > 0 || 'Must include a message']"
        />
        <div class="row justify-between">
          <q-btn
            name="deny-dialog-button"
            label="Send"
            icon-right="cancel"
            type="submit"
            color="primary"
          />
        </div>
      </q-form>
    </q-card>
  </q-dialog>


</div>
</template>

<style scoped lang="scss"></style>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useQuasar } from 'quasar'
import { readableDate } from 'src/filters'

const quasar = useQuasar()

let approved = ref(false)
let denied = ref(false)
let calendarLoaded = ref(true)
let showApproveDialog = ref(false)
let showDenyDialog = ref(false)
let denyDialogMessage = ref('')

let employeeName = 'Dan Wilson'

const props = defineProps<{
  monthDisplay: string
  monthInt: string
  yearInt: string
}>()

const pagination = {
  rowsPerPage: '50'
}

const columns = [
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
    name: 'gl', field: 'gl', label: 'GL Code', align: 'center', sortable: true,
    style: 'width: 10px'
  },
  { name: 'approver', field: 'approver', label: 'Approver', align: 'center' },
  { name: 'receipt', field: 'receipt', label: 'Receipt', align: 'center' }
]

const rows = ref([
  {
    name: 'Frozen Yogurt',
    date: '2023-10-01',
    job: '',
    gl: '43-45045-232',
    approver: { 'pk': 5, 'name': 'Dan Wilson', 'legal_name': 'Daniel Wilson' },
    receipt: 'file.txt'
  },
  {
    name: 'Ice cream sandwich',
    date: '2023-10-04',
    job: '123',
    gl: '55-55555-555',
    approver: {pk: -1, name: '', legal_name: ''},
    receipt: 'file.txt'
  },
  {
    name: 'Eclair',
    date: '2023-10-07',
    job: '',
    gl: '12-34567-890',
    approver: {pk: -1, name: '', legal_name: ''},
    receipt: 'file.txt'
  },
  {
    name: 'Cupcake',
    date: '2023-10-07',
    job: '',
    gl: '43-45045-232',
    approver: {pk: -1, name: '', legal_name: ''},
    receipt: 'file.txt'
  }
])

// function monthExpenses(): Expense[] {
//   return []
//   // const apiResults = timeOffStore.teamTimeOffRequests
//   // let sortedTimeOff: TimeOffCalendarData = []
//   // if (apiResults) {
//   //   for (let i=0; i<5; i++) {
//   //     let d = new Date(selectedMonday.value.getTime() + i*(1000 * 60 * 60 * 24))
//   //     let isToday = d.setHours(0,0,0,0) === today.value.setHours(0,0,0,0)
//   //     sortedTimeOff.push({
//   //       date: d.toLocaleDateString('en-us', { weekday: 'long', month: 'long', day: 'numeric' }),
//   //       isToday: isToday,
//   //       requests: apiResults.filter(request => {
//   //         const targetDateMS = d.setHours(0,0,0,0)

//   //         const fromDate = new Date(request.start_date)
//   //         const fromTZOffset = fromDate.getTimezoneOffset() * 60000
//   //         const fromDateMS = new Date(fromDate.getTime() + fromTZOffset).setHours(0,0,0,0)

//   //         const toDate = new Date(request.end_date)
//   //         const toTZOffset = toDate.getTimezoneOffset() * 60000
//   //         const toDateMS = new Date(toDate.getTime() + toTZOffset).setHours(0,0,0,0)

//   //         if (fromDateMS <= targetDateMS && targetDateMS <= toDateMS) {
//   //           return true
//   //         } else {
//   //           return false
//   //         }
//   //       })
//   //     })
//   //   }
//   // }
//   // return sortedTimeOff
// }

function tableTitleDisplay(): string {
  return `${props.monthDisplay} expenses for ${employeeName}`
}

// TODO: This currently gets all time off; should probably just get for a period
// function retrieveTeamTimeOff(): void {
//   timeOffStore.getTeamTimeOffRequests()
//     .then(() => {
//       calendarLoaded.value = true
//     })
//     .catch(e => {
//       console.error('Error retrieving team time off', e)
//     })
// }

function onSubmitApproveDialog() {
  // const extraMessage = type == 'ASSIGN' ? reassignDialogMessage.value : sendDialogMessage.value
  // workflowsStore.sendTransitionToEmailList(transitionPk.value, {
  //   type: type,
  //   reassignTo: assignee.value,
  //   update: sendDialogUpdate.value,
  //   extraMessage,
  //   senderName: userStore.getEmployeeProfile.name,
  //   senderEmail: userStore.getEmployeeProfile.email,
  //   transitionUrl: route.fullPath
  // })
  //   .then(() => {
  //     quasar.notify({
  //       message: 'Sent',
  //       color: 'positive',
  //       icon: 'send'
  //     })
  //     showSendToSDSHiringLeadsDialog.value = false
  //     showSendToFiscalDialog.value = false
  //     showSendToHRDialog.value = false
  //     showSendToSTNDialog.value = false
  //     showAssigneeDialog.value = false
  //     sendDialogUpdate.value = false
  //     sendDialogMessage.value = ''
  //     reassignDialogMessage.value = ''
  //     // Signal to WorkflowInstanceDetail that the transition was assigned or
  //     // completed, in which case we need to get the newly created process
  //     // instances.
  //     bus.emit('transitionReassigned', Math.random())
  //   })
  //   .catch(e => {
  //     console.error('Error sending email', e)
  //     quasar.notify({
  //       message: 'Error sending email',
  //       color: 'negative',
  //       icon: 'report_problem'
  //     })
  //   })
  showApproveDialog.value = false
  approved.value = true
  denied.value = false
  quasar.notify({
    message: 'Approved',
    color: 'positive',
    icon: 'send'
  })
}

function onSubmitDenyDialog() {
  showDenyDialog.value = false
  approved.value = false
  denied.value = true
  denyDialogMessage.value = ''
  quasar.notify({
    message: 'Denied',
    color: 'negative',
    icon: 'cancel'
  })
}

onMounted(() => {
  // retrieveTeamTimeOff()
})

</script>

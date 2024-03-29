<template>
<div class="q-mt-md">
  <div class="q-gutter-md">
    <q-btn v-if="submitted" @click="showUnsubmitDialog = true">Unsubmit</q-btn>
    <q-btn v-else @click="showSubmitToFiscalDialog = true">Submit to Fiscal</q-btn>
  </div>
  <div class="q-mt-md">
    <q-spinner-grid
      v-if="!calendarLoaded"
      class="spinner"
      color="primary"
      size="xl"
    />
    <q-table
      v-else
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
        <q-tr :props="props" :class="submitted?'bg-grey':''">
          <q-td key="name" :props="props">
            {{ props.row.name }}
            <q-popup-edit v-if="!submitted" v-model="props.row.name" buttons v-slot="scope">
              <q-input v-model="scope.value" dense autofocus @keyup.enter="scope.set()" />
            </q-popup-edit>
          </q-td>
          <q-td key="date" :props="props">
            {{ readableDate(props.row.date) }}
            <q-popup-edit v-if="!submitted" v-model="props.row.date" buttons v-slot="scope">
              <q-input type="date" v-model="scope.value" dense autofocus @keyup.enter="scope.set()" />
            </q-popup-edit>
          </q-td>
          <q-td key="job" :props="props">
            <div class="text-pre-wrap">{{ props.row.job }}</div>
            <q-popup-edit v-if="!submitted" v-model="props.row.job" buttons v-slot="scope">
              <q-input v-model="scope.value" dense autofocus @keyup.enter="scope.set()" />
            </q-popup-edit>
          </q-td>
          <q-td key="gls" :props="props">
            <div class="text-pre-wrap" v-for="gl in props.row.gls" :key="props.row.gls.indexOf(gl)">
              {{ gl.gl }}: {{ gl.percent }}%
            </div>
            <q-popup-edit v-if="!submitted" v-model="props.row.gls" buttons v-slot="scope">
              <div v-for="gl in scope.value" :key="scope.value.indexOf(gl)" class="row">
                <q-input
                  v-model="gl.gl"
                  class="q-mr-sm"
                  outlined dense autofocus
                  mask="##-#####-###"
                  @keyup.enter="scope.set()"
                  :rules="[
                    val => !!val || 'Required',
                  ]"
                />
                <div class="row">
                  <q-input
                    v-model="gl.percent"
                    type="number"
                    class="gl-percent"
                    outlined dense autofocus
                    @keyup.enter="scope.set()"
                    :rules="[
                      val => !!val || '* Required',
                      val => val <= 100 || 'Please use a number less than 100',
                    ]"
                  />
                  <div class="gl-percent-symbol">%</div>
                </div>
              </div>
              <q-btn @click="scope.value.push({gl: '', percent: 0})">Add a GL</q-btn>
            </q-popup-edit>
          </q-td>
          <q-td key="approver" :props="props">
            {{ props.row.approver.name }}
            <q-popup-edit v-if="!submitted" v-model="props.row.approver" buttons v-slot="scope">
              <EmployeeSelect
                name="approver"
                label="Approver"
                :employee="props.row.approver"
                :useLegalName="true"
                v-on:input="props.row.approver=$event"
                v-on:clear="props.row.approver=EmployeeSelect.emptyEmployee"
                :readOnly=false
                @keyup.enter="scope.set()"
              />
            </q-popup-edit>
          </q-td>
          <q-td key="approvalNotes" :props="props">
            {{ props.row.approvalNotes }}
            <q-popup-edit v-if="!submitted" v-model="props.row.approvalNotes" buttons v-slot="scope">
              <q-input v-model="scope.value" dense autofocus @keyup.enter="scope.set()" />
            </q-popup-edit>
          </q-td>
          <q-td key="receipt" :props="props">
            {{ props.row.receipt }}
            <q-popup-edit v-if="!submitted" v-model="props.row.receipt" buttons>
              <FileUploader
                label="Receipt"
                :file="props.row.receipt"
                contentTypeAppLabel="purchases"
                contentTypeModel="expense"
                :readOnly=false
              />
            </q-popup-edit>
          </q-td>
        </q-tr>
      </template>
      <template v-slot:bottom-row v-if="!submitted">
        <q-tr @click="clickAddExpense()" class="cursor-pointer row-add-new">
          <q-td colspan="100%">
            <q-icon name="add" size="md" class="q-pr-sm"/>New Expense
          </q-td>
        </q-tr>
      </template>
    </q-table>
  </div>

  <!-- Submit to Fiscal Dialog -->
  <q-dialog v-model="showSubmitToFiscalDialog">
    <q-card class="q-pa-md" style="width: 400px">
      <div class="text-h6">Submit {{ monthDisplay }} expenses to Fiscal?</div>
      <q-form
        @submit='onSubmitFiscalDialog()'
        class="q-gutter-md"
      >
        <q-input
          v-model="sendDialogMessage"
          filled
          type="textarea"
          label="Extra message to include"
        />
        <div class="row justify-between">
          <q-btn
            name="send-fiscal-dialog-button"
            label="Send"
            icon-right="send"
            type="submit"
            color="primary"
            :disable="formErrors()"
          />
          <!-- <div
            v-if="formErrors()"
            class="text-red text-bold"
            style="width:180px;"
          >
            There are errors in the form. Fix before submitting.
          </div> -->
        </div>
      </q-form>
    </q-card>
  </q-dialog>

  <!-- Unsubmit Dialog -->
  <q-dialog v-model="showUnsubmitDialog">
    <q-card class="q-pa-md" style="width: 400px">
      <div class="text-h6">Unsubmit {{ monthDisplay }} expenses?</div>
      <q-form
        @submit='onUnsubmitDialog()'
        class="q-gutter-md"
      >
        <div class="row justify-between">
          <q-btn
            name="unsubmit-dialog-button"
            label="Unsubmit"
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

<style scoped lang="scss">
  .approval-notes {
    white-space: normal;
  }

  .gl-percent {
    max-width: 80px;
  }

  .gl-percent-symbol {
    margin: 9px 0 0 3px;
  }
</style>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useQuasar } from 'quasar'
import EmployeeSelect from 'src/components/EmployeeSelect.vue'
import FileUploader from 'src/components/FileUploader.vue'
import { readableDate } from 'src/filters'

// type Expense = {date: string, isToday: boolean}

const quasar = useQuasar()

const props = defineProps<{
  monthDisplay: string
}>()

let submitted = ref(false)
let calendarLoaded = ref(true)
let showSubmitToFiscalDialog = ref(false)
let sendDialogMessage = ref('')
let showUnsubmitDialog = ref(false)

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
    name: 'gls', field: 'gls', label: 'GL Codes', align: 'center', sortable: true,
    style: 'width: 10px'
  },
  { name: 'approver', field: 'approver', label: 'Approver', align: 'center' },
  {
    name: 'approvalNotes', field: 'approvalNotes', label: 'Approval Notes',
    align: 'center', classes: 'approval-notes', headerClasses: 'approval-notes'
  },
  { name: 'receipt', field: 'receipt', label: 'Receipt', align: 'center' }
]

const rows = ref([
  {
    name: 'Frozen Yogurt',
    date: '2023-10-01',
    job: '',
    gls: [{gl: '43-45045-232', percent: 100}],
    approver: { 'pk': 5, 'name': 'Dan Wilson', 'legal_name': 'Daniel Wilson' },
    approvalNotes: 'Felicity feigned faintness so I fetched froyo. Follow?',
    receipt: 'file.txt'
  },
  {
    name: 'Ice cream sandwich',
    date: '2023-10-04',
    job: '123',
    gls: [{gl: '55-55555-555', percent: 50}, {gl: '43-45045-232', percent: 50}],
    approver: {pk: -1, name: '', legal_name: ''},
    approvalNotes: '',
    receipt: 'file.txt'
  },
  {
    name: 'Eclair',
    date: '2023-10-07',
    job: '',
    gls: [{gl: '12-34567-890', percent: 100}],
    approver: {pk: -1, name: '', legal_name: ''},
    approvalNotes: '',
    receipt: 'file.txt'
  },
  {
    name: 'Cupcake',
    date: '2023-10-07',
    job: '',
    gls: [{gl: '43-45045-232', percent: 100}],
    approver: {pk: -1, name: '', legal_name: ''},
    approvalNotes: '',
    receipt: 'file.txt'
  }
])

function tableTitleDisplay(): string {
  const submittedText = submitted.value ? ' - Submitted' : ''
  return `${props.monthDisplay}${submittedText}`
}

// function monthExpenses(): Expense[] {
//   return []
//   const apiResults = timeOffStore.teamTimeOffRequests
//   let sortedTimeOff: TimeOffCalendarData = []
//   if (apiResults) {
//     for (let i=0; i<5; i++) {
//       let d = new Date(selectedMonday.value.getTime() + i*(1000 * 60 * 60 * 24))
//       let isToday = d.setHours(0,0,0,0) === today.value.setHours(0,0,0,0)
//       sortedTimeOff.push({
//         date: d.toLocaleDateString('en-us', { weekday: 'long', month: 'long', day: 'numeric' }),
//         isToday: isToday,
//         requests: apiResults.filter(request => {
//           const targetDateMS = d.setHours(0,0,0,0)

//           const fromDate = new Date(request.start_date)
//           const fromTZOffset = fromDate.getTimezoneOffset() * 60000
//           const fromDateMS = new Date(fromDate.getTime() + fromTZOffset).setHours(0,0,0,0)

//           const toDate = new Date(request.end_date)
//           const toTZOffset = toDate.getTimezoneOffset() * 60000
//           const toDateMS = new Date(toDate.getTime() + toTZOffset).setHours(0,0,0,0)

//           if (fromDateMS <= targetDateMS && targetDateMS <= toDateMS) {
//             return true
//           } else {
//             return false
//           }
//         })
//       })
//     }
//   }
//   return sortedTimeOff
// }

function clickAddExpense(): void {
  rows.value.push({
    name: '',
    date: '',
    job: '',
    gls: [{gl: '', percent: 0}],
    approver: {pk: -1, name: '', legal_name: ''},
    approvalNotes: '',
    receipt: ''
  })
}

function formErrorItems(): Array<[string, string]> {
  let errorItems: Array<[string, string]> = []
  // if (computerTypeCurrentVal.value == 'New' && !computerGLCurrentVal.value) {
  //   errorItems.push(
  //     ['computer-type', 'Provide a valid GL code for computer purchase']
  //   )
  // }
  // if (
  //   computerTypeCurrentVal.value == 'Repurposed' &&
  //   !computerDescriptionCurrentVal.value
  // ) {
  //   errorItems.push(
  //     ['computer-type', 'Provide a description of existing computer']
  //   )
  // }
  return errorItems
}

function formErrors() {
  return formErrorItems().length > 0
}

function onSubmitFiscalDialog() {
  showSubmitToFiscalDialog.value = false
  submitted.value = true
  rows.value.forEach(row => row.submitted = true)
  quasar.notify({
    message: 'Sent',
    color: 'positive',
    icon: 'send'
  })
}

function onUnsubmitDialog() {
  showUnsubmitDialog.value = false
  submitted.value = false
  rows.value.forEach(row => row.submitted = false)
  quasar.notify({
    message: 'Unsubmitted',
    color: 'positive',
    icon: 'cancel'
  })
}

onMounted(() => {
  // retrieveExpenses()
})

</script>

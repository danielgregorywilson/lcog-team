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
      :title="monthDisplay"
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
          <q-td key="gl" :props="props">
            <div class="text-pre-wrap">{{ props.row.gl }}</div>
            <q-popup-edit v-if="!submitted" v-model="props.row.gl" buttons v-slot="scope">
              <q-input v-model="scope.value" dense autofocus @keyup.enter="scope.set()" />
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

<style scoped lang="scss"></style>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useQuasar } from 'quasar'
import EmployeeSelect from 'src/components/EmployeeSelect.vue'
import FileUploader from 'src/components/FileUploader.vue'
import { readableDate } from 'src/filters'

type Expense = {date: string, isToday: boolean}

const quasar = useQuasar()

defineProps<{
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

function clickAddExpense(): void {
  rows.value.push({
    name: '',
    date: '',
    job: '',
    gl: '',
    approver: {pk: -1, name: '', legal_name: ''},
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

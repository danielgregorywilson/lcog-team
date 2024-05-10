<template>
<div class="q-mt-md">
  <div class="q-gutter-md">
    <q-btn v-if="submitted" @click="showUnsubmitDialog = true">Unsubmit</q-btn>
    <q-btn v-else @click="showSubmitToFiscalDialog = true">Submit to Fiscal</q-btn>
  </div>
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
      <template v-slot:body="props">
        <q-tr :props="props" :class="submitted?'bg-grey':''">
          <q-td key="name" :props="props">
            {{ props.row.name }}
            <q-popup-edit
              v-if="!submitted"
              v-model="props.row.name"
              buttons
              v-slot="scope"
              @save="(val) => updateName(props.row.pk, val)"
            >
              <q-input v-model="scope.value" dense autofocus />
            </q-popup-edit>
          </q-td>
          <q-td key="date" :props="props">
            {{ readableDateNEW(props.row.date) }}
            <q-popup-edit
              v-if="!submitted"
              v-model="props.row.date"
              buttons
              v-slot="scope"
              @save="(val) => updateDate(props.row.pk, val)"
            >
              <q-input type="date" v-model="scope.value" dense autofocus />
            </q-popup-edit>
          </q-td>
          <q-td key="job" :props="props">
            <div class="text-pre-wrap">{{ props.row.job }}</div>
            <q-popup-edit
              v-if="!submitted"
              v-model="props.row.job"
              buttons
              v-slot="scope"
              @save="(val) => updateJob(props.row.pk, val)"
            >
              <q-input v-model="scope.value" dense autofocus />
            </q-popup-edit>
          </q-td>
          <q-td key="gls" :props="props">
            <div
              class="text-pre-wrap"
              v-for="gl in props.row.gls"
              :key="props.row.gls.indexOf(gl)"
            >
              {{ gl.gl }}: {{ gl.percent }}%
            </div>
            <q-popup-edit
              v-if="!submitted"
              v-model="props.row.gls"
              buttons
              v-slot="scope"
              @save="(val) => updateGLs(props.row.pk, val)"
            >
              <div
                v-for="(gl, idx) in scope.value"
                :key="scope.value.indexOf(gl)"
                class="row"
              >
                <q-input
                  v-model="gl.gl"
                  class="q-mr-sm"
                  outlined dense autofocus
                  mask="##-#####-###"
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
                <q-icon
                  name="cancel"
                  size="sm"
                  @click.stop="scope.value.splice(idx, 1)"
                  class="cursor-pointer q-mt-sm q-ml-sm"
                />
              </div>
              <q-btn @click="scope.value.push({gl: '', percent: 0})">
                Add a GL
              </q-btn>
            </q-popup-edit>
          </q-td>
          <q-td key="approver" :props="props">
            {{ props.row.approver?.name }}
            <q-popup-edit
              v-if="!submitted"
              v-model="props.row.approver"
              buttons
              v-slot="scope"
              @save="(val) => updateApprover(props.row.pk, val)"
            >
              <EmployeeSelect
                name="approver"
                label="Approver"
                :employee="scope.value"
                :useLegalName="true"
                v-on:input="scope.value=$event"
                v-on:clear="scope.value=emptyEmployee"
                :readOnly=false
              />
            </q-popup-edit>
          </q-td>
          <q-td key="approvalNotes" :props="props">
            {{ props.row.approval_notes }}
            <q-popup-edit
              v-if="!submitted"
              v-model="props.row.approval_notes"
              buttons
              v-slot="scope"
              @save="(val) => updateApprovalNotes(props.row.pk, val)"
            >
              <q-input v-model="scope.value" dense autofocus />
            </q-popup-edit>
          </q-td>
          <q-td key="receipt" :props="props">
            {{ props.row.receipt?.split('/').pop() }}
            <q-popup-edit
              v-if="!submitted"
              v-model="props.row.receipt"
              buttons
              v-slot="scope"
            >
              <FileUploader
                :file="scope.value"
                contentTypeAppLabel="purchases"
                contentTypeModel="expense"
                :objectPk="props.row.pk.toString()"
                :readOnly=false
                v-on="{
                  'uploaded': (url: string) => {
                    updateReceipt(props.row.pk, url)
                    retrieveAllMyExpenses()
                  }
                }"
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
import { onMounted, Ref, ref } from 'vue'
import { useQuasar } from 'quasar'

import EmployeeSelect from 'src/components/EmployeeSelect.vue'
import FileUploader from 'src/components/FileUploader.vue'
import { readableDateNEW } from 'src/filters'
import { handlePromiseError } from 'src/stores'
import { usePurchaseStore } from 'src/stores/purchase'
import { emptyEmployee, Expense, GL, SimpleEmployeeRetrieve } from 'src/types'

const quasar = useQuasar()
const purchaseStore = usePurchaseStore()

const props = defineProps<{
  monthDisplay: string
  dayInt: number
  monthInt: number
  yearInt: number
}>()

let thisMonthLoaded = ref(false)
let allExpensesLoaded = ref(false)

let expenses = ref([]) as Ref<Expense[]>
let submitted = ref(false)
let showSubmitToFiscalDialog = ref(false)
let sendDialogMessage = ref('')
let showUnsubmitDialog = ref(false)

let firstOfThisMonth = ref(new Date())
let firstOfSelectedMonth = ref(new Date())

function viewingThisMonth() {
  return firstOfSelectedMonth.value.getTime() ===
    firstOfThisMonth.value.getTime()
}

function expensesLoaded() {
  return (viewingThisMonth() && thisMonthLoaded.value) ||
    allExpensesLoaded.value
}

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


function tableTitleDisplay(): string {
  const submittedText = submitted.value ? ' - Submitted' : ''
  return `${props.monthDisplay}${submittedText}`
}

function selectedMonthExpenses(): Expense[] {
  const apiResults = purchaseStore.myExpenses
  let exps: Expense[] = []
  if (apiResults) {
    exps = apiResults.filter(exp => {
      let [y, m] = exp.date.split('-').map(s => parseInt(s))
      m -= 1 // JS months are 0-indexed
      return m === props.monthInt && y === props.yearInt
    })
  }
  return exps
}

function clickAddExpense(): void {

  purchaseStore.createExpense({
    name: '',
    date: `${ props.yearInt }-${ props.monthInt + 1 }-${ props.dayInt }`,
    job: '',
    gls: [],
    approval_notes: '',
  })
    .then(() => {
      retrieveAllMyExpenses()
    })
    .catch((error) => {
      console.log('Error adding expense', error)
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
  expenses.value.forEach(row => row.submitted = true)
  quasar.notify({
    message: 'Sent',
    color: 'positive',
    icon: 'send'
  })
}

function onUnsubmitDialog() {
  showUnsubmitDialog.value = false
  submitted.value = false
  expenses.value.forEach(row => row.submitted = false)
  quasar.notify({
    message: 'Unsubmitted',
    color: 'positive',
    icon: 'cancel'
  })
}

function retrieveThisMonthExpenses(): Promise<void> {
  // Get all my expenses for this month
  return new Promise((resolve, reject) => {
    purchaseStore.getMyExpenses(props.yearInt, props.monthInt)
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

function retrieveAllMyExpenses() {
  purchaseStore.getMyExpenses()
    .then(() => {
      allExpensesLoaded.value = true
    })
    .catch((error) => {
      console.log('Error retrieving expenses', error)
    })
}

function updateExpense(row: Expense) {
  purchaseStore.updateExpense(row)
    .catch((error) => {
      console.log('Error updating expense', error)
    })
}

function updateName(pk: number, val: string) {
  const row = expenses.value.find(row => row.pk === pk)
  if (row) {
    row.name = val
    updateExpense(row)
  }
}

function updateDate(pk: number, val: string) {
  const row = expenses.value.find(row => row.pk === pk)
  if (row) {
    row.date = val
    updateExpense(row)
  }
}

function updateJob(pk: number, val: string) {
  const row = expenses.value.find(row => row.pk === pk)
  if (row) {
    row.job = val
    updateExpense(row)
  }
}

function updateGLs(pk: number, val: Array<GL>) {
  const row = expenses.value.find(row => row.pk === pk)
  if (row) {
    row.gls = val
    updateExpense(row)
  }
}

function updateApprover(pk: number, val: SimpleEmployeeRetrieve) {
  const row = expenses.value.find(row => row.pk === pk)
  if (row) {
    row.approver = val
    updateExpense(row)
  }
}

function updateApprovalNotes(pk: number, val: string) {
  const row = expenses.value.find(row => row.pk === pk)
  if (row) {
    row.approval_notes = val
    updateExpense(row)
  }
}

function updateReceipt(pk: number, val: string) {
  const row = expenses.value.find(row => row.pk === pk)
  if (row) {
    row.receipt_link = val
    updateExpense(row)
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
    retrieveAllMyExpenses()
  })
})

</script>

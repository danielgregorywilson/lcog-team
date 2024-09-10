<template>
<div class="q-mt-md">
  <div v-if="purchaseStore.selectedExpenseMonth">
    <div class="row q-gutter-md">
      <q-btn
        v-if="!monthSubmitted()"
        @click="showSubmitDialog = true"
        :disabled="formErrors() || !statementSelected()"
      >
        Submit for Approval
      </q-btn>
      <q-btn v-if="canUnsubmitMonth()" @click="showUnsubmitDialog = true">
        Unsubmit
      </q-btn>
      <q-btn v-if="formErrors()" @click="showErrorsDialog = true">
        <div>Correct Errors</div>
        <q-icon color="orange" name="warning" size="md" />
      </q-btn>
      <q-btn v-if="!statementSelected()" flat class="no-pointer-events">
        <div>Select a CC statement</div>
        <q-icon color="orange" name="warning" size="md" />
      </q-btn>
      <q-btn
        v-else-if="!expensesMatchStatment()"
        flat
        class="no-pointer-events"
      >
        <div>Entered expenses do not match statement</div>
        <q-icon color="orange" name="warning" size="md" />
      </q-btn>
    </div>
    <div v-if="selectedMonthNotes().length">
      <ul id="denial-notes" class="q-mt-md q-pa-sm q-pl-lg bg-info font-bold">
        <li
          v-for="note of selectedMonthNotes()"
          :key="selectedMonthNotes().indexOf(note)"
        >
          From <span class="text-bold">{{ note.approver }}</span>
          <span v-if="note.expense">
            about <span class="text-bold">{{ note.expense }}</span>
          </span>: {{ note.note }}
        </li>
      </ul>
    </div>
    <div class="q-mt-md">
      <q-spinner-grid
        v-if="!expensesLoaded"
        class="spinner"
        color="primary"
        size="xl"
      />
      <div v-else>
        <div class="text-h6">Submitted Total: ${{ expensesTotal() }}</div>
        <q-table
          flat bordered
          :title="tableTitleDisplay()"
          :rows="selectedMonthExpenses()"
          :columns="columns"
          :dense="$q.screen.lt.lg"
          :grid="$q.screen.lt.md"
          row-key="name"
          binary-state-sort
          :pagination="pagination"
          class="expense-table"
          no-data-label="No expenses entered this month"
        >
          <template v-slot:body="props">
            <q-tr
              :props="props"
              :class="expenseClass(props.row)"
            >
              <q-td key="name" :props="props" style="white-space: normal;">
                {{ props.row.name }}
                <q-popup-edit
                  v-if="!monthSubmitted()"
                  v-model="props.row.name"
                  buttons
                  v-slot="scope"
                  @save="(val) => updateExpense(props.row.pk, 'name', val)"
                >
                  <q-input
                    v-model="scope.value"
                    maxlength="255"
                    dense
                    autofocus
                    @keyup.enter="scope.set()"
                  />
                </q-popup-edit>
              </q-td>
              <q-td key="date" :props="props">
                {{ readableDateNEW(props.row.date) }}
                <q-popup-edit
                  v-if="!monthSubmitted()"
                  v-model="props.row.date"
                  buttons
                  v-slot="scope"
                  @save="(val) => updateExpense(props.row.pk, 'date', val)"
                >
                  <q-input
                    type="date"
                    v-model="scope.value"
                    dense
                    autofocus
                    @keyup.enter="scope.set()"
                  />
                </q-popup-edit>
              </q-td>
              <q-td key="vendor" :props="props" style="white-space: normal;">
                <div class="text-pre-wrap">{{ props.row.vendor }}</div>
                <q-popup-edit
                  v-if="!monthSubmitted()"
                  v-model="props.row.vendor"
                  buttons
                  v-slot="scope"
                  @save="(val) => updateExpense(props.row.pk, 'vendor', val)"
                >
                  <q-input
                    v-model="scope.value"
                    maxlength="255"
                    dense
                    autofocus
                    @keyup.enter="scope.set()"
                  />
                </q-popup-edit>
              </q-td>
              <q-td key="amount" :props="props">
                {{ props.row.amount }}
                <q-popup-edit
                  v-if="!monthSubmitted()"
                  v-model="props.row.amount"
                  buttons
                  v-slot="scope"
                  @save="(val) => updateExpense(props.row.pk, 'amount', val)"
                >
                  <q-input
                    v-model="scope.value"
                    mask="#.##"
                    fill-mask="0"
                    reverse-fill-mask
                    dense
                    autofocus
                    @keyup.enter="scope.set()"
                  />
                </q-popup-edit>
              </q-td>
              <q-td key="job" :props="props">
                <div class="text-pre-wrap">{{ props.row.job }}</div>
                <q-popup-edit
                  v-if="!monthSubmitted()"
                  v-model="props.row.job"
                  buttons
                  v-slot="scope"
                  @save="(val) => updateExpense(props.row.pk, 'job', val)"
                >
                  <q-input
                    v-model="scope.value"
                    maxlength="255"
                    dense
                    autofocus
                    @keyup.enter="scope.set()"
                  />
                </q-popup-edit>
              </q-td>
              <q-td key="gls" :props="props">
                <div
                  class="text-pre-wrap"
                  v-for="gl in props.row.gls"
                  :key="props.row.gls.indexOf(gl)"
                >
                  {{ gl.code }}: ${{ gl.amount }} – {{ gl.approver?.name }}
                </div>
                <q-popup-edit
                  v-if="!monthSubmitted()"
                  v-model="props.row.gls"
                  buttons
                  v-slot="scope"
                  @save="(val) => updateExpense(props.row.pk, 'gls', val)"
                >
                  <div class="gl-popup-edit">
                    <div
                      v-for="(gl, idx) in scope.value"
                      :key="scope.value.indexOf(gl)"
                      class="row items-center"
                    >
                      <q-input
                        v-model="gl.code"
                        class="q-mr-sm q-pa-none"
                        outlined dense autofocus
                        mask="###-##-####-#####"
                        fill-mask="___-__-____-_____"
                        :rules="[
                          val => !!val || 'Required',
                        ]"
                      />
                      <div class="row q-mr-sm">
                        <div class="gl-dollar-symbol">$</div>
                        <q-input
                          v-model="gl.amount"
                          class="gl-amount q-pa-none"
                          outlined dense
                          mask="#.##"
                          fill-mask="0"
                          reverse-fill-mask
                          @keyup.enter="scope.set()"
                          :rules="[
                            val => !!val || '* Required',
                          ]"
                        />
                      </div>
                      <EmployeeSelect
                        name="approver"
                        label="Approver"
                        :employee="gl.approver"
                        :useLegalName="true"
                        v-on:input="gl.approver=$event"
                        v-on:clear="gl.approver=emptyEmployee"
                        :readOnly=false
                        :employeeFilterFn="
                          (employee: SimpleEmployeeRetrieve) => {
                            return employee.is_expense_approver
                          }
                        "
                      />
                      <q-icon
                        name="cancel"
                        size="sm"
                        @click.stop="scope.value.splice(idx, 1)"
                        class="cursor-pointer q-ml-sm"
                      />
                    </div>
                    <div class="row justify-center q-mt-sm">
                      <q-btn class="col-6" @click="scope.value.push(
                        {code: '', amount: 0, approver: emptyEmployee}
                      )">
                        Add a GL
                      </q-btn>
                    </div>
                  </div>
                </q-popup-edit>
              </q-td>
              <q-td key="receipt" :props="props">
                <div class="row justify-center">
                  <DocumentViewer
                    v-if="props.row.receipt"
                    :documentUrl="props.row.receipt"
                    iconButton
                    flat
                  />
                  <!-- Button to upload file -->
                  <q-btn icon="cloud_upload"
                    flat
                    :disable="monthSubmitted()"
                  >
                    <q-popup-edit
                      v-if="!monthSubmitted()"
                      v-model="props.row.receipt"
                      buttons
                      v-slot="scope"
                    >
                      <FileUploader
                        :file="scope.value"
                        contentTypeAppLabel="purchases"
                        contentTypeModel="expense"
                        :readOnly=false
                        :objectPk="props.row.pk.toString()"
                        allowedFileTypes="image/jpeg,image/png,.pdf"
                        v-on="{
                          'uploaded': (url: string) => {
                            uploadedReceipt(props.row.pk)
                          }
                        }"
                      />
                      <div class="q-mt-sm">
                        Supported filetypes: JPEG, PNG, PDF
                      </div>
                    </q-popup-edit>
                  </q-btn>
                </div>
              </q-td>
              <q-td key="actions" :props="props">
                <q-btn
                  v-if="!monthSubmitted()"
                  class="col"
                  dense
                  round
                  flat
                  @click="updateExpense(
                    props.row.pk, 'repeat', !props.row.repeat
                  )"
                  :icon="props.row.repeat ? 'repeat_on' : 'repeat'"
                >
                  <q-tooltip>
                    <div v-if="props.row.repeat">
                      Expense will repeat next month
                    </div>
                    <div v-else>Click to repeat expense next month</div>
                  </q-tooltip>
                </q-btn>
                <q-btn
                  v-if="!monthSubmitted()"
                  class="col"
                  dense
                  round
                  flat
                  @click="showDeleteDialog(props.row)"
                  icon="delete"
                />
              </q-td>
            </q-tr>
          </template>
          <!-- GRID MODE -->
          <template v-slot:item="props">
            <div class="q-pa-xs col-xs-12 col-sm-6 col-md-4 col-lg-3">
              <q-card
                class="q-py-sm"
                :class="monthSubmitted()?'bg-grey':'cursor-pointer'"
              >
                <q-list dense>
                  <q-item v-for="col in props.cols" :key="col.name">
                    <div class="q-table__grid-item-row">
                      <div class="q-table__grid-item-title">
                        {{ col.label }}
                      </div>
                      <div
                        class="q-table__grid-item-value"
                        v-if="col.name == 'date'"
                      >
                        {{ readableDateNEW(col.value) }}
                      </div>
                      <div
                        class="q-table__grid-item-value"
                        v-else-if="col.name == 'gls'"
                      >
                        <div
                          class="text-pre-wrap"
                          v-for="gl in props.row.gls"
                          :key="props.row.gls.indexOf(gl)"
                        >
                          {{ gl.code }}: ${{ gl.amount }} –
                          {{ gl.approver?.name }}
                        </div>
                      </div>
                      <div
                        class="q-table__grid-item-value row"
                        v-else-if="col.name == 'receipt'"
                      >
                        <DocumentViewer
                          v-if="col.value"
                          :documentUrl="col.value"
                          iconButton
                          flat
                        />
                        <!-- Button to upload file -->
                        <q-btn icon="cloud_upload"
                          flat
                          :disable="monthSubmitted()"
                        >
                          <q-popup-edit
                            v-if="!monthSubmitted()"
                            v-model="props.row.receipt"
                            buttons
                            v-slot="scope"
                          >
                            <FileUploader
                              :file="scope.value"
                              contentTypeAppLabel="purchases"
                              contentTypeModel="expense"
                              :readOnly=false
                              :objectPk="props.row.pk.toString()"
                              allowedFileTypes="image/jpeg,image/png,.pdf"
                              v-on="{
                                'uploaded': (url: string) => {
                                  retrieveAllMyExpenses()
                                }
                              }"
                            />
                            <div class="q-mt-sm">
                              Supported filetypes: JPEG, PNG, PDF
                            </div>
                          </q-popup-edit>
                        </q-btn>
                      </div>
                      <div class="q-table__grid-item-value" v-else>
                        {{ col.value }}
                      </div>
                    </div>
                  </q-item>
                </q-list>
              </q-card>
            </div>
          </template>
        </q-table>
      </div>
      <div class="row justify-center">
        <q-btn
          v-if="!monthSubmitted()"
          color="primary"
          class="q-mt-sm"
          @click="clickAddExpense()"
          icon="add"
        >
          New Expense
        </q-btn>
      </div>
      
    </div>
  </div>
  <div v-else>
    <q-card>
      <q-card-section class="row items-center">
        <div class="text-h6">{{ purchaseStore.monthDisplay }} not started.</div>
        <q-btn
          color="primary"
          class="q-ml-sm"
          @click="createExpenseMonth().then(() => retrieveAllMyExpenses())"
        >
          Get started
        </q-btn>
      </q-card-section>
    </q-card>
  </div>

  <!-- Statements -->
  <div v-if="thisMonthStatementsLoaded" class="q-mt-md">
    <div v-if="statementChoices().length">
      <q-select
        v-if="thisMonthStatementsLoaded"
        :bg-color="selectedStatement ? '': 'info'"
        filled
        :disable="monthSubmitted()"
        v-model="selectedStatement"
        :options="statementChoices()"
        label="Select your card"
        dense
        outlined
        @update:model-value="updateSelectedStatement()"
      />
      <StatementTable :statement="selectedStatement?.value" />
    </div>
    <div v-else>
      <q-card>
        <q-card-section>
          <div class="text-h6">No statements uploaded for this month</div>
        </q-card-section>
      </q-card>
    </div> 
  </div>

  <!-- Errors Dialog -->
  <q-dialog v-model="showErrorsDialog">
    <q-card style="width: 350px">
      <q-list bordered separator>
        <q-item
          v-for="(item, index) in formErrorItems()"
          :key="index"
          clickable
        >
          <q-item-label>{{item}}</q-item-label>
        </q-item>
      </q-list>
    </q-card>
  </q-dialog>

  <!-- Delete Expense Dialog -->
  <q-dialog v-model="deleteDialogVisible">
    <q-card>
      <q-card-section>
        <div class="row items-center">
          <q-avatar
            icon="book"
            color="primary"
            text-color="white"
          />
          <span class="q-ml-sm">
            Are you sure you want to delete this expense?
          </span>
        </div>
        <div
          v-if="deleteDialogExpenseName"
          class="row justify-center text-center"
        >
          Name: {{ deleteDialogExpenseName }}
        </div>
        <div
          v-if="deleteDialogExpenseDate"
          class="row justify-center text-center"
        >
          Date: {{ deleteDialogExpenseDate }}
        </div>
      </q-card-section>

      <q-card-actions class="row justify-around">
        <q-btn flat label="Cancel" color="primary" v-close-popup />
        <q-btn
          flat
          label="Yes, delete it"
          color="primary"
          @click="deleteExpense()"
          v-close-popup
        />
      </q-card-actions>
    </q-card>
  </q-dialog>

  <!-- Submit for approval Dialog -->
  <q-dialog v-model="showSubmitDialog">
    <q-card class="q-pa-md" style="width: 400px">
      <div class="text-h6">
        Submit {{ purchaseStore.monthDisplay }} expenses for approval?
      </div>
      <div
        v-if="!expensesMatchStatment()"
        class="row items-center q-gutter-sm q-mb-md"
      >
        <q-icon color="orange" name="warning" size="md" />  
        <div class="col text-red text-body1 text-bold">
          <span v-if="!totalsMatch()">
            WARNING! Selected statement has a total of
            ${{ selectedStatementTotal() }}, and you entered
            ${{ expensesTotal() }}.
          </span>
          <span v-if="!numExpensesMatch()">
            WARNING! Selected statement has
            {{ selectedStatement?.value.items.length }} items, and you entered
            {{ selectedMonthExpenses().length }}.
          </span>
          Enter explanation below.
        </div>
      </div>
      <q-form
        @submit='onSubmitDialog()'
        class="q-gutter-md"
      >
        <q-input
          v-model="submitterNote"
          filled
          type="textarea"
          label="Extra message for approver and fiscal"
        />
        <div class="row justify-between">
          <q-btn
            name="send-fiscal-dialog-button"
            label="Send"
            icon-right="send"
            type="submit"
            color="primary"
            :disable="!expensesMatchStatment() && !submitterNote"
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
      <div class="text-h6">
        Unsubmit {{ purchaseStore.monthDisplay }} expenses?
      </div>
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
#denial-notes {
  font-size: 1.2em;
}

.gl-popup-edit {
  min-width: 500px;
}

.gl-amount {
  max-width: 180px;
}

.gl-dollar-symbol {
  margin: 9px 0 0 3px;
}
</style>

<script setup lang="ts">
import { onMounted, Ref, ref, watch } from 'vue'
import { useQuasar } from 'quasar'

import DocumentViewer from 'src/components/DocumentViewer.vue'
import EmployeeSelect from 'src/components/EmployeeSelect.vue'
import FileUploader from 'src/components/FileUploader.vue'
import StatementTable from 'src/components/purchases/StatementTable.vue'
import { readableDateNEW, readableDateTime } from 'src/filters'
import { handlePromiseError } from 'src/stores'
import { usePurchaseStore } from 'src/stores/purchase'
import {
  emptyEmployee, Expense, ExpenseMonth, ExpenseStatement, GL,
  SimpleEmployeeRetrieve 
} from 'src/types'


const quasar = useQuasar()
const purchaseStore = usePurchaseStore()

let thisMonthLoaded = ref(false)
let allExpensesLoaded = ref(false)

let thisMonthStatementsLoaded = ref(false)
let allStatementsLoaded = ref(false)
// SelectedStatement is a q-select option, so it has a label and a value.
let selectedStatement = ref(null) as 
  Ref<{label: string, value: ExpenseStatement} | null>

let showErrorsDialog = ref(false)
let showSubmitDialog = ref(false)
let submitterNote = ref('')
let showUnsubmitDialog = ref(false)

let deleteDialogVisible = ref(false)
let expensePkToDelete = ref(-1)
let deleteDialogExpenseName = ref('')
let deleteDialogExpenseDate = ref('')

function viewingThisMonth() {
  return purchaseStore.firstOfSelectedMonth.getTime() ===
    purchaseStore.firstOfThisMonth.getTime()
}

function expensesLoaded() {
  return (viewingThisMonth() && thisMonthLoaded.value) ||
    allExpensesLoaded.value
}

const pagination = {
  rowsPerPage: 50
}

const columns = [
  {
    name: 'name', field: 'name', label: 'Item', required: true, align: 'left',
    sortable: true
  },
  {
    name: 'date', field: 'date', label: 'Date', align: 'center', sortable: true
  },
  {
    name: 'vendor', field: 'vendor', label: 'Vendor', align: 'center',
    sortable: true
  },
  { name: 'amount', field: 'amount', label: 'Amount', align: 'center' },
  {
    name: 'job', field: 'job', label: 'Job #', align: 'center', sortable: true
  },
  {
    name: 'gls', field: 'gls', label: 'GL Codes – Approver', align: 'center',
    sortable: true, style: 'width: 10px'
  },
  { name: 'receipt', field: 'receipt', label: 'Receipt', align: 'center' },
  { name: 'actions', label: 'Actions', align: 'center', field: '' },
]


function tableTitleDisplay(): string {
  let statusText = 'Draft'
  if (purchaseStore.selectedExpenseMonth?.status == 'fiscal_approved') {
    statusText = 'Fiscal Approved - You\'re All Set!'
  } else if (purchaseStore.selectedExpenseMonth?.status == 'fiscal_denied') {
    statusText = 'Fiscal Denied - Correct and Resubmit'
  } else if (
    purchaseStore.selectedExpenseMonth?.status == 'director_approved'
  ) {
    statusText = 'Director Approved - Waiting on Fiscal'
  } else if (purchaseStore.selectedExpenseMonth?.status == 'director_denied') {
    statusText = 'Director Denied - Correct and Resubmit'
  } else if (
    purchaseStore.selectedExpenseMonth?.status == 'approver_approved'
  ) {
    if (purchaseStore.selectedExpenseMonth?.card.requires_director_approval) {
      statusText = 'Approver(s) Approved - Waiting on Director'
    } else {
      statusText = 'Approver(s) Approved - Waiting on Fiscal'
    }
  } else if (purchaseStore.selectedExpenseMonth?.status == 'approver_denied') {
    statusText = 'Approver(s) Denied - Correct and Resubmit'
  } else if (purchaseStore.selectedExpenseMonth?.status == 'submitted') {
    statusText = 'Submitted - Waiting on Approver(s)'
  }
  return `${ purchaseStore.monthDisplay } - ${ statusText }`
}

function selectedMonthExpenses(): Expense[] {
  const month = purchaseStore.selectedExpenseMonth
  if (month !== undefined) {
    return month.expenses
  } else {
    return []
  }
}

function selectedMonthNotes(): Array<{
  type: string, approver: string, date: string, expense?: string, note: string
}> {
  let notes = []
  let em = purchaseStore.selectedExpenseMonth
  if (!em) {
    return []
  }
  let fiscalNote = em?.fiscal_note
  let date = em ? readableDateTime(em?.fiscal_approved_at) : ''
  if (fiscalNote) {
    notes.push({
      type: 'fiscal',
      approver: em.fiscal_approver.name,
      date,
      note: fiscalNote
    })
  }
  let directorNote = em?.director_note
  let directorDate = em ? readableDateTime(em?.director_approved_at) : ''
  if (directorNote) {
    notes.push({
      type: 'director',
      approver: em.card.director_name,
      date: directorDate,
      note: directorNote
    })
  }
  for (let exp of selectedMonthExpenses()) {
    for (let gl of exp.gls) {
      let date = readableDateTime(gl.approved_at)
      if (gl.approver && gl.approved_at && !gl.approved) {
        notes.push({
          type: 'approver',
          approver: gl.approver.name,
          date,
          expense: exp.name,
          note: gl.approver_note
        })
      }
    }
  }
  return notes
}

function expensesTotal() {
  return selectedMonthExpenses().reduce(
    (acc, exp) => acc + parseFloat(exp.amount), 0
  )
}

function selectedStatementTotal() {
  if (!selectedStatement.value) {
    return 0
  }
  return selectedStatement?.value.value.items.reduce(
    (acc, item) => acc + parseFloat(item.amount), 0
  ).toFixed(2)
}

function totalsMatch() {
  return selectedStatementTotal() == expensesTotal()
}

function numExpensesMatch() {
  if (!selectedStatement.value) {
    return true
  }
  return selectedStatement?.value.value.items.length ==
    selectedMonthExpenses().length
}

function expensesMatchStatment(): boolean {
  return numExpensesMatch() && totalsMatch()
}

function monthSubmitted() {
  const ems = purchaseStore.expenseMonths
  return ems.some(em => {
    return em.month === purchaseStore.monthInt &&
      em.year === purchaseStore.yearInt &&
      em.status !== 'draft'
  })
}

function expenseApproved(expense: Expense) {
  return expense.status === 'approver_approved'
}

function expenseDenied(expense: Expense) {
  return expense.status === 'approver_denied'
}

function monthApproved() {
  return purchaseStore.selectedExpenseMonth?.status === 'fiscal_approved'
}

function monthDenied() {
  return purchaseStore.selectedExpenseMonth?.status === 'fiscal_denied' || 
    purchaseStore.selectedExpenseMonth?.status === 'director_denied'
}

function expenseClass(expense: Expense) {
  if (!expense) {
    return ''
  }
  if (monthApproved()) {
    return 'bg-green'
  } else if (monthDenied() || expenseDenied(expense)) {
    return 'bg-red'
  } else if (expenseApproved(expense) || monthSubmitted()) {
    return 'bg-grey'
  } else {
    return 'cursor-pointer'
  }
}

function clickAddExpense(): void {

  purchaseStore.createExpense({
    name: '',
    date: `${ purchaseStore.yearInt }-${ purchaseStore.monthInt }-` +
      `${ purchaseStore.dayInt }`,
    job: '',
    gls: [],
  })
    .then(() => {
      retrieveAllMyExpenses()
    })
    .catch((error) => {
      console.log('Error adding expense', error)
    })
}

function formErrorItems() {
  let errorItems: string[] = []
  for (let exp of selectedMonthExpenses()) {
    if (!exp.name) {
      errorItems.push(`Provide a name for the expense on ${exp.date}`)
    }
    if (parseFloat(exp.amount) <= 0) {
      errorItems.push(
        `Provide an amount for ${exp.name} ${typeof parseFloat(exp.amount)}`
      )
    }
    if (!exp.job) {
      errorItems.push(`Provide a job number for ${exp.name}, or enter 'None'`)
    }
    for (let gl of exp.gls) {
      if (!gl.code || gl.code.length !== 17) {
        errorItems.push(
          `Provide a valid GL code for each GL row in ${exp.name}`
        )
      }
      if (!gl.amount) {
        errorItems.push(
          `Provide a GL amount for each GL row in ${exp.name}`
        )
      }
      if (!gl.approver || gl.approver?.pk == -1) {
        errorItems.push(`Provide an approver for each GL row in ${exp.name}`)
      }
    }
    const GLsTotal = exp.gls.reduce(
      (acc, gl) => acc + parseFloat(gl.amount), 0
    )
    if (GLsTotal.toFixed(2) !== parseFloat(exp.amount).toFixed(2)) {
      errorItems.push(`GLs for ${exp.name} must add to ${exp.amount}`)
    }
    if (!exp.receipt) {
      errorItems.push(
        `Provide a receipt or appropriate documentation for ${exp.name}`
      )
    }
  }
  return errorItems
}

function formErrors() {
  return formErrorItems().length > 0
}

function canUnsubmitMonth() {
  return monthSubmitted() && !monthApproved()
}

function onSubmitDialog() {
  purchaseStore.submitExpenseMonth({
    yearInt: purchaseStore.yearInt, monthInt: purchaseStore.monthInt,
    note: submitterNote.value
  })
    .then(() => {
      showSubmitDialog.value = false
      retrieveAllMyExpenses()
      quasar.notify({
        message: 'Sent',
        color: 'positive',
        icon: 'send'
      })
    })
    .catch((error) => {
      console.log('Error submitting expenses', error)
    })
}

function onUnsubmitDialog() {
  purchaseStore.submitExpenseMonth({
    yearInt: purchaseStore.yearInt, monthInt: purchaseStore.monthInt,
    unsubmit: true
  })
    .then(() => {
      showUnsubmitDialog.value = false
      retrieveAllMyExpenses()
      quasar.notify({
        message: 'Unsubmitted',
        color: 'positive',
        icon: 'cancel'
      })
    })
    .catch((error) => {
      console.log('Error unsubmitting expenses', error)
    })
}

function retrieveRecentExpenseMonths(): Promise<void> {
  return new Promise((resolve, reject) => {
    purchaseStore.getExpenseMonths(
      purchaseStore.firstOfThisMonth.getFullYear(),
      purchaseStore.firstOfThisMonth.getMonth() + 1
    )
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
  purchaseStore.getExpenseMonths()
    .then(() => {
      allExpensesLoaded.value = true
    })
    .catch((error) => {
      console.log('Error retrieving expenses', error)
    })
}

function updateExpense(
  pk: number,
  field: 'name' | 'date' | 'amount' | 'vendor' | 'job' | 'gls' | 'repeat',
  val: string | Array<GL> | boolean
) {
  const exp = purchaseStore.myExpenses.find(exp => exp.pk === pk)
  if (exp) {
    if (field === 'gls') {
      exp.gls = val as Array<GL>
    } else if (field === 'repeat') {
      exp.repeat = val as boolean
    } else {
      exp[field] = val as string
    }
    purchaseStore.updateExpense(exp)
      .catch((error) => {
        console.log('Error updating expense', error)
      })
  }
}

function uploadedReceipt(pk: number) {
  purchaseStore.clearExpenseGLApprovals(pk)
    .then(() => {
      retrieveAllMyExpenses()
    })
}

function showDeleteDialog(expense: Expense): void {
  expensePkToDelete.value = expense.pk
  deleteDialogExpenseName.value = expense.name
  deleteDialogExpenseDate.value = expense.date
  deleteDialogVisible.value = true
}

function deleteExpense(): void {
  purchaseStore.deleteExpense(expensePkToDelete.value)
    .then(() => {
      quasar.notify('Deleted an expense.')
      retrieveAllMyExpenses()
    })
    .catch(e => {
      console.error(e)
    })
}

function retrieveThisMonthStatements(): Promise<void> {
  return new Promise((resolve, reject) => {
    purchaseStore.getExpenseStatements(
      purchaseStore.yearInt, purchaseStore.monthInt
    )
      .then(() => {
        thisMonthStatementsLoaded.value = true
        resolve()
      })
      .catch((error) => {
        handlePromiseError(reject, 'Error retrieving expense statements', error)
        reject()
      })
  })
}

function retrieveAllStatements(): Promise<void> {
  return new Promise((resolve, reject) => {
    purchaseStore.getExpenseStatements()
      .then(() => {
        allStatementsLoaded.value = true
        resolve()
      })
      .catch((error) => {
        handlePromiseError(reject, 'Error retrieving expense statements', error)
        reject()
      })
  })
}

function thisMonthStatements(): Array<ExpenseStatement> {
  return purchaseStore.expenseStatements.filter(es => {
    return es.month === purchaseStore.monthInt &&
      es.year === purchaseStore.yearInt
  })
}

function statementChoices(): Array<{label: string, value: ExpenseStatement}> {
  return thisMonthStatements().map(es => {
    return {
      label: es.card.display,
      value: es
    }
  })
}

function updateSelectedStatement() {
  new Promise((resolve) => {
    const em = purchaseStore.selectedExpenseMonth
    if (!em) {
      createExpenseMonth().then((newEM) => {
        if (selectedStatement.value) {
          purchaseStore.setExpenseMonthCard(
            newEM.pk, selectedStatement.value.value.card.pk
          ).then(() => {
            resolve(newEM)
          })
        }
      })
    }
    if (em && selectedStatement.value) {
      purchaseStore.setExpenseMonthCard(
        em.pk, selectedStatement.value.value.card.pk
      ).then(() => {
        resolve(em)
      })
    }
  }).then(() => {
    retrieveAllMyExpenses()
  })
}

function statementSelected(): boolean {
  return selectedStatement.value !== null
}

function setSelectedStatement() {
  selectedStatement.value = statementChoices().find(
    sc => sc.value.card.pk === purchaseStore.selectedExpenseMonth?.card?.pk
  ) || null
}

function createExpenseMonth(): Promise<ExpenseMonth> {
  return new Promise ((resolve, reject) => {
    purchaseStore.createExpenseMonth({
      month: purchaseStore.monthInt,
      year: purchaseStore.yearInt
    })
      .then((em) => {
        resolve(em)
      })
      .catch((error) => {
        handlePromiseError(reject, 'Error creating expense month', error)
        reject()
      })
  })
}

onMounted(() => {
  retrieveRecentExpenseMonths().then(() => {
    retrieveAllMyExpenses()
    // Don't retrieve statements until we've gotten expenses
    // so we can set selected expense card.
    retrieveThisMonthStatements().then(() => {
      retrieveAllStatements().then(() => {
        setSelectedStatement()
      })
    })
  })
})

watch(() => purchaseStore.monthInt, (first, second) => {
  if (first !== second) {
    setSelectedStatement()
  }
})

</script>

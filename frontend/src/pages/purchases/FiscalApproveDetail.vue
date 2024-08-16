<template>
<div class="q-mt-md">
  <!-- Statement -->
  <div v-if="statement">
    <div class="row items-center justify-between q-mt-md">
      <div class="text-h5">
        Statement for {{ card?.display }}
        in {{ monthDisplay }}
      </div>
      <div v-if="!props.print">
        <q-btn v-if="!totalsMatch()" flat class="no-pointer-events">
          <div>Expenses total does not match statement</div>
          <q-icon color="orange" name="warning" size="md" />
        </q-btn>
        <q-btn v-if="!numExpensesMatch()" flat class="no-pointer-events">
          <div>Number of expenses does not match statement</div>
          <q-icon color="orange" name="warning" size="md" />
        </q-btn>
        <q-btn v-if="expensesMatchStatment()" flat class="no-pointer-events">
          <div>Statement and expenses seem to match</div>
          <q-icon color="green" name="check" size="md" />
        </q-btn>
        <q-btn @click="navigateToPrintView()" label="Print" />
      </div>
    </div>
    <StatementTable :statement="statement" />
  </div>
  <div v-else>
    <div class = "text-h5">No card selected in {{ monthDisplay }}</div>
  </div>
  
  <!-- Expense Months -->
  <q-spinner-grid
    v-if="!expensesLoaded()"
    class="spinner"
    color="primary"
    size="xl"
  />
  <div v-else-if="selectedMonthCardExpenseMonths().length">
    <div v-for="em of selectedMonthCardExpenseMonths()" :key="em.pk">
      <div class="q-mt-lg">
        <q-table
          flat bordered
          :title="tableTitleDisplay(em)"
          :rows="em.expenses"
          :columns="props.print ? printColumns : columns"
          :dense="$q.screen.lt.lg"
          :grid="$q.screen.lt.md"
          row-key="name"
          binary-state-sort
          :pagination="pagination"
          class="expense-table"
          no-data-label="No expenses entered this month"
        >
          <template v-slot:body-cell-date="props">
            <q-td key="date" :props="props">
              {{ readableDateNEW(props.row.date) }}
            </q-td>
          </template>
          <template v-slot:body-cell-gls="props">
            <q-td key="gls" :props="props">
              <div
                class="text-pre-wrap"
                v-for="gl in props.row.gls"
                :key="props.row.gls.indexOf(gl)"
              >
                {{ gl.code }}: ${{ gl.amount }} – {{ gl.approver.name }}
              </div>
            </q-td>
          </template>
          <template v-slot:body-cell-approvedAt="props">
            <q-td key="date" :props="props" style="white-space: normal;">
              {{ readableDateTime(props.row.approved_at) }}
            </q-td>
          </template>
          <template v-slot:body-cell-receipt="props">
            <q-td key="receipt" :props="props">
              <DocumentViewer
                v-if="props.row.receipt"
                :documentUrl="props.row.receipt"
                iconButton
              />
            </q-td>
          </template>
          <!-- GRID MODE -->
          <template v-slot:item="props">
            <div class="q-pa-xs col-xs-12 col-sm-6 col-md-4 col-lg-3">
              <q-card class="q-py-sm">
                <q-list dense>
                  <q-item v-for="col in props.cols" :key="col.name">
                    <div class="q-table__grid-item-row">
                      <div class="q-table__grid-item-title">
                        {{ col.label }}
                      </div>
                      <div
                        class="q-table__grid-item-value"
                        v-if="col.label == 'Date'"
                      >
                        {{ readableDateNEW(col.value) }}
                      </div>
                      <div
                        class="q-table__grid-item-value"
                        v-else-if="col.label == 'GL Codes'"
                      >
                        <div
                          class="text-pre-wrap"
                          v-for="gl in props.row.gls"
                          :key="props.row.gls.indexOf(gl)"
                        >
                          {{ gl.code }}: ${{ gl.amount }} –
                          {{ gl.approver.name }}
                        </div>
                      </div>
                      <div
                        class="q-table__grid-item-value"
                        v-else-if="col.label == 'Approved At'"
                      >
                        {{ readableDateTime(col.value) }}
                      </div>
                      <div
                        class="q-table__grid-item-value"
                        v-else-if="col.label == 'Receipt'"
                      >
                        <DocumentViewer
                          v-if="col.value"
                          :documentUrl="col.value"
                          iconButton
                        />
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

        <div v-if="em.submitter_note && !props.print">
          <div id="submitter-note" class="q-mt-md q-pa-sm bg-info font-bold">
            <div>Submitter Note:</div>
            <div>{{ em.submitter_note }}</div>
          </div>
        </div>
        
        <div
          v-if="!props.print"
          class="q-mt-sm q-gutter-md row justify-between"
        >
          <div>
            <q-btn
              :class="EMApproved(em)?'bg-green':''"
              :disable="!fiscalCanApprove(em) || EMApproved(em)"
              @click="onShowApproveDialog(em)"
              class="q-mr-md"
            >
              Approve Expenses
              <q-tooltip v-if="!fiscalCanApprove(em)">
                Month not yet submitted
              </q-tooltip>
            </q-btn>
            <q-btn
              :class="EMDenied(em)?'bg-red':''"
              :disable="!fiscalCanApprove(em) || EMDenied(em)"
              @click="onShowDenyDialog(em)"
            >
              Deny Expenses
              <q-tooltip v-if="!fiscalCanApprove(em)">
                Month not yet submitted
              </q-tooltip>
            </q-btn>
          </div>
        </div>
      </div>

      <!-- Display Receipts for Print View -->
      <div v-if="props.print">
        <div
          v-for="expense in em.expenses"
          :key="expense.pk"
        >
          <q-img v-if="expense.receipt_type == 'image'" :src="expense.receipt" />
          <iframe
            v-else-if="expense.receipt_type == 'pdf'"  
            :src="expense.receipt"
            width="100%"
            height="950px"
          />
          <div class="text-h4 text-negative" v-else>
            Receipt is of filetype {{ expense.receipt_type }} and cannot be
            displayed. <a href="expense.receipt">Click here to download.</a>
          </div>
        </div>
      </div>

    </div>
  </div>
  <div v-else class="text-h5">
    No expenses entered by {{ routeEmployeeName }} in {{ monthDisplay }}
  </div>

  <!-- Approve Dialog -->
  <q-dialog v-model="showApproveDialog">
    <q-card class="q-pa-md" style="width: 400px">
      <div class="text-h6">
        Approve {{monthDisplay}} expenses for {{ emToApproveEmployeeName }}?
      </div>
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

  <!-- Deny ExpenseMonth Dialog -->
  <q-dialog v-model="showDenyDialog">
    <q-card class="q-pa-md" style="width: 400px">
      <div class="text-h6">
        Deny {{ monthDisplay }} expenses for {{ emToApproveEmployeeName }}?
      </div>
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

<style scoped lang="scss">
#submitter-note {
  font-size: 1.2em;
  font-weight: bold;
}
</style>

<script setup lang="ts">
import { useQuasar } from 'quasar'
import { onMounted, Ref, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import DocumentViewer from 'src/components/DocumentViewer.vue'
import StatementTable from 'src/components/purchases/StatementTable.vue'
import { readableDateNEW, readableDateTime } from 'src/filters'
import { handlePromiseError } from 'src/stores'
import { usePeopleStore } from 'src/stores/people'
import { usePurchaseStore } from 'src/stores/purchase'
import { ExpenseCard, ExpenseMonth, ExpenseStatement } from 'src/types'
import { getRouteParam } from 'src/utils'


const route = useRoute()
const router = useRouter()
const quasar = useQuasar()
const peopleStore = usePeopleStore()
const purchaseStore = usePurchaseStore()

const props = defineProps<{
  monthDisplay?: string
  monthInt?: number
  yearInt?: number
  print?: boolean
}>()

let emToApprovePK = ref(-1)
let emToApproveEmployeeName = ref('')
let showApproveDialog = ref(false)
let showDenyDialog = ref(false)
let denyDialogMessage = ref('')

let monthDisplay = ref(props.monthDisplay)
let monthInt = ref(props.monthInt)
let yearInt = ref(props.yearInt)

let card = ref(null) as Ref<ExpenseCard | null>
let statement = ref(null) as Ref<ExpenseStatement | null>

let routeEmployeePK = ref(-1)
let routeEmployeeName = ref('')

let thisMonthLoaded = ref(false)
let allExpensesLoaded = ref(false)

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

const printColumns = [
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
  {
    name: 'amount', field: 'amount', label: 'Amount', align: 'center',
    sortable: true
  },
  {
    name: 'job', field: 'job', label: 'Job #', align: 'center', sortable: true
  },
  {
    name: 'gls', field: 'gls', label: 'GL Codes', align: 'center',
    sortable: true, style: 'width: 10px'
  },
  {
    name: 'approvedAt', field: 'approved_at', label: 'Approved At',
    align: 'center'
  },
]

const columns = printColumns.concat([{
  name: 'receipt', field: 'receipt', label: 'Receipt', align: 'center'
}])

function tableTitleDisplay(em: ExpenseMonth): string {
  return `${ monthDisplay.value } expenses for ${ em.purchaser.name }`
}

function selectedMonthCardExpenseMonths(): Array<ExpenseMonth> {
  let currentCard = null
  let currentStatement = null
  const allEMs = purchaseStore.fiscalExpenseMonths.filter(em => {
    return em.month === monthInt.value && em.year === yearInt.value
  })
  let ems: Array<ExpenseMonth> = []
  if (allEMs.length) {
    const selectedEmployeeEM = allEMs.filter(em => {
      return em.purchaser.pk === routeEmployeePK.value
    })[0]
    if (selectedEmployeeEM) {
      currentCard = selectedEmployeeEM.card
      currentStatement = selectedEmployeeEM.statement
      ems = allEMs.filter(em => {
        return em.card?.pk === selectedEmployeeEM.card?.pk
      })
    }
  }
  card.value = currentCard
  statement.value = currentStatement
  if (!ems.length) {
    setEmployeeName()
  }
  return ems
}

function setEmployeeName() {
  peopleStore.getSimpleEmployeeDetail(
    { pk: routeEmployeePK.value }
  ).then((employee) => {
    routeEmployeeName.value = employee.name
  })
}

function fiscalCanApprove(expenseMonth: ExpenseMonth) {
  if (expenseMonth.card?.requires_director_approval) {
    return ['director_approved', 'fiscal_approved', 'fiscal_denied']
      .includes(expenseMonth.status)
  } else {
    return ['approver_approved', 'fiscal_approved', 'fiscal_denied']
      .includes(expenseMonth.status)
  }
}

function EMApproved(em: ExpenseMonth): boolean {
  return em.status === 'fiscal_approved'
}

function EMDenied(em: ExpenseMonth): boolean {
  return em.status === 'fiscal_denied'
}

function retrieveThisMonthEmployeeExpenses(): Promise<void> {
  return new Promise((resolve, reject) => {
    const employeePK = routeEmployeePK.value
    if (!employeePK) {
      return
    }
    purchaseStore.getFiscalExpenseMonths(
      yearInt.value, monthInt.value, employeePK
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

function retrieveAllEmployeeExpenses() {
  const employeePK = routeEmployeePK.value
  if (!employeePK) {
    return
  }
  purchaseStore.getFiscalExpenseMonths(null, null, employeePK)
    .then(() => {
      allExpensesLoaded.value = true
    })
    .catch((error) => {
      console.log('Error retrieving expenses', error)
    })
}

function onShowApproveDialog(em: ExpenseMonth) {
  emToApprovePK.value = em.pk
  emToApproveEmployeeName.value = em.purchaser.name
  showApproveDialog.value = true
}

function onShowDenyDialog(em: ExpenseMonth) {
  emToApprovePK.value = em.pk
  emToApproveEmployeeName.value = em.purchaser.name
  showDenyDialog.value = true
}

function onSubmitApproveDialog() {
  if (emToApprovePK.value == -1) {
    quasar.notify({
      message: 'No expenses to approve',
      color: 'negative',
      icon: 'cancel'
    })
    return
  } else {
    purchaseStore.approveExpenseMonth(emToApprovePK.value, true)
      .then(() => {
        retrieveAllEmployeeExpenses()
        showApproveDialog.value = false
        quasar.notify({
          message: 'Approved',
          color: 'positive',
          icon: 'send'
        })
      })
      .catch(() => {
        quasar.notify({
          message: 'Error approving expenses',
          color: 'negative',
          icon: 'cancel'
        })
      })
  }
}

function onSubmitDenyDialog() {
  if (emToApprovePK.value == -1) {
    quasar.notify({
      message: 'No expenses to approve',
      color: 'negative',
      icon: 'cancel'
    })
    return
  } else {
    purchaseStore.approveExpenseMonth(
      emToApprovePK.value, false, denyDialogMessage.value
    )
      .then(() => {
        retrieveAllEmployeeExpenses()
        showDenyDialog.value = false
        denyDialogMessage.value = ''
        quasar.notify({
          message: 'Denied',
          color: 'negative',
          icon: 'cancel'
        })
      })
      .catch(() => {
        quasar.notify({
          message: 'Error approving expenses',
          color: 'negative',
          icon: 'cancel'
        })
      })
    }
}

function setDates() {
  return new Promise((resolve) => {
    let theFirst = new Date()
    theFirst.setDate(1)
    theFirst.setHours(0,0,0,0)
    firstOfThisMonth.value = theFirst
    firstOfSelectedMonth.value = theFirst
    resolve(null)
  })
}

function navigateToPrintView() {
  const employeePK = routeEmployeePK.value
  if (!employeePK) {
    return
  }
  router.push({
    name: 'expense-month-print',
    params: {
      employeePK: employeePK,
      month: monthInt.value,
      year: yearInt.value
    }
  })
}

function expensesTotal() {
  let total = 0
  for (let em of selectedMonthCardExpenseMonths()) {
    total += em.expenses.reduce(
      (acc, expense) => acc + parseFloat(expense.amount), 0
    )
  }
  return total
}

function totalsMatch() {
  const statementTotal = statement.value?.items?.reduce(
    (acc, item) => acc + parseFloat(item.amount), 0
  )
  return statementTotal == expensesTotal()
}

function numExpensesMatch() {
  const expenses = []
  for (let em of selectedMonthCardExpenseMonths()) {
    expenses.push(...em.expenses)
  }
  return expenses.length == statement.value?.items?.length
}

function expensesMatchStatment(): boolean {
  return totalsMatch() && numExpensesMatch()
}

function handlePrint() {
  const monthParam = getRouteParam(route, 'month')
  const yearParam = getRouteParam(route, 'year')
  if (!monthParam || !yearParam) {
    return
  } else {
    monthInt.value = parseInt(monthParam)
    yearInt.value = parseInt(yearParam)
    var months = [
      'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
      'September', 'October', 'November', 'December'
    ]
    monthDisplay.value = `${months[monthInt.value - 1]} ${yearInt.value}`
  }
  // Load expense month if not already loaded; otherwise mark as loaded
  if (purchaseStore.fiscalExpenseMonths.length == 0) {
    retrieveThisMonthEmployeeExpenses()
  } else {
    thisMonthLoaded.value = true
  }
}

onMounted(() => {
  const employeePK = getRouteParam(route, 'employeePK')
  routeEmployeePK.value = parseInt(employeePK ? employeePK : '-1')
  if (props.print) {
    handlePrint()
  } else {
    setDates().then(() => {
      retrieveThisMonthEmployeeExpenses().then(() => {
        retrieveAllEmployeeExpenses()
      })
    })
  }
})

watch(() => props.monthInt, (first, second) => {
  if (first !== second) {
    monthInt.value = props.monthInt
  }
})

watch(() => props.yearInt, (first, second) => {
  if (first !== second) {
    yearInt.value = props.yearInt
  }
})

watch(() => props.monthDisplay, (first, second) => {
  if (first !== second) {
    monthDisplay.value = props.monthDisplay
  }
})

</script>

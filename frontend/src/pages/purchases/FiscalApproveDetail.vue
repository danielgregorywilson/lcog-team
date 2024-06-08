<template>
<div class="q-mt-md">
  <div v-if="!props.print" class="row q-gutter-md">
    <div v-if="selectedMonthApproved()" class="row items-center">
      <q-icon color="green" name="check_circle" size="lg" class="q-mr-sm" />
      <div>Approved</div>
    </div>
    <div v-else-if="selectedMonthDenied()" class="row items-center">
      <q-icon color="red" name="cancel" size="lg" class="q-mr-sm" />
      <div>Denied</div>
    </div>
  </div>
  <div class="q-mt-md">
    <q-spinner-grid
      v-if="!expensesLoaded"
      class="spinner"
      color="primary"
      size="xl"
    />
    <div v-else>
      <q-table
        flat bordered
        :title="tableTitleDisplay()"
        :rows="selectedMonthExpenseMonthExpenses()"
        :columns="props.print ? printColumns : columns"
        :dense="$q.screen.lt.lg"
        :grid="$q.screen.lt.md"
        row-key="name"
        binary-state-sort
        :pagination="pagination"
        class="expense-table"
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
              {{ gl.code }}: {{ gl.percent }}% – {{ gl.approver.name }}
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
                    <div class="q-table__grid-item-title">{{ col.label }}</div>
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
                        {{ gl.code }}: {{ gl.percent }}% –
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
      <div v-if="!props.print" class="q-mt-sm q-gutter-md row justify-between">
        <div>
          <q-btn
            :class="selectedMonthApproved()?'bg-green':''"
            :disable="selectedMonthApproved()"
            @click="showApproveDialog = true"
            class="q-mr-md"
          >
            Approve Expenses
          </q-btn>
          <q-btn
            :class="selectedMonthDenied()?'bg-red':''"
            :disable="selectedMonthDenied()"
            @click="showDenyDialog = true"
          >
            Deny Expenses
          </q-btn>
        </div>
        <q-btn @click="navigateToPrintView()" label="Print" />
      </div>
    </div>
  </div>

  <!-- Display Receipts for Print View -->
  <div v-if="props.print">
    <div
      v-for="expense in selectedMonthExpenseMonthExpenses()"
      :key="expense.pk"
    >
      <q-img :src="expense.receipt" />
    </div>
  </div>

  <!-- Approve Dialog -->
  <q-dialog v-model="showApproveDialog">
    <q-card class="q-pa-md" style="width: 400px">
      <div class="text-h6">
        Approve {{monthDisplay}} expenses for {{ employeeName }}?
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

  <!-- Deny Dialog -->
  <q-dialog v-model="showDenyDialog">
    <q-card class="q-pa-md" style="width: 400px">
      <div class="text-h6">
        Deny {{monthDisplay}} expenses for {{ employeeName }}?
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
.approval-notes {
  white-space: normal;
}
</style>

<script setup lang="ts">
import { useQuasar } from 'quasar'
import { onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import DocumentViewer from 'src/components/DocumentViewer.vue'
import { readableDateNEW, readableDateTime } from 'src/filters'
import { handlePromiseError } from 'src/stores'
import { usePeopleStore } from 'src/stores/people'
import { usePurchaseStore } from 'src/stores/purchase'
import { Expense, ExpenseMonth } from 'src/types'
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

let showApproveDialog = ref(false)
let showDenyDialog = ref(false)
let denyDialogMessage = ref('')

let monthDisplay = ref(props.monthDisplay)
let monthInt = ref(props.monthInt)
let yearInt = ref(props.yearInt)

let employeeName = ref('')
let employeePK = ref(0)

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
    name: 'name', field: 'name', label: 'Name', required: true, align: 'left',
    sortable: true
  },
  {
    name: 'date', field: 'date', label: 'Date', align: 'center', sortable: true
  },
  {
    name: 'description', field: 'description', label: 'Description',
    align: 'center', sortable: true
  },
  {
    name: 'vendor', field: 'vendor', label: 'Vendor', align: 'center',
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

const columns = printColumns.concat(
  [{ name: 'receipt', field: 'receipt', label: 'Receipt', align: 'center' }]
)

function tableTitleDisplay(): string {
  return `${monthDisplay.value} expenses for ${employeeName.value}`
}

function selectedMonthExpenseMonth(): ExpenseMonth | null {
  const ems = purchaseStore.fiscalExpenseMonths
  let em: ExpenseMonth | null = null
  if (ems.length) {
    const currentExpenseMonths = ems.filter(em => {
      return em.month === monthInt.value && em.year === yearInt.value
    })
    if (currentExpenseMonths.length) {
      em = currentExpenseMonths[0]
    }
  }
  return em
}

function selectedMonthExpenseMonthExpenses(): Expense[] {
  const em = selectedMonthExpenseMonth()
  if (em) return em.expenses.all()
  return []
}

function selectedMonthApproved(): boolean {
  const em = selectedMonthExpenseMonth()
  if (em) return em.status === 'fiscal_approved'
  return false
}

function selectedMonthDenied(): boolean {
  const em = selectedMonthExpenseMonth()
  if (em) return em.status === 'fiscal_denied'
  return false
}

function getEmployeeFromRoute() {
  return new Promise((resolve, reject) => {
    const PK = getRouteParam(route, 'employeePK')
    if (PK) {
      employeePK.value = parseInt(PK)
      peopleStore.getSimpleEmployeeDetail({pk: parseInt(PK)})
        .then((employee) => {
          employeeName.value = employee.name
          resolve(employee)
        })
        .catch((error) => {
          reject(error)
        })
    } else {
      reject()
    }
  }).catch(() => {
    quasar.notify({
      message: 'Couldn\'t get employee',
      color: 'negative',
      icon: 'cancel'
    })
  })
}

function retrieveThisMonthEmployeeExpenses(): Promise<void> {
  return new Promise((resolve, reject) => {
    purchaseStore.getFiscalExpenseMonths(yearInt.value, monthInt.value)
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
  const employeePK = getRouteParam(route, 'employeePK')
  if (!employeePK) {
    return
  }
  purchaseStore.getFiscalExpenseMonths(null, null, parseInt(employeePK))
    .then(() => {
      allExpensesLoaded.value = true
    })
    .catch((error) => {
      console.log('Error retrieving expenses', error)
    })
}

function onSubmitApproveDialog() {
  showApproveDialog.value = false
  const pk = selectedMonthExpenseMonth()?.pk
  if (!pk) {
    quasar.notify({
      message: 'No expenses to approve',
      color: 'negative',
      icon: 'cancel'
    })
    return
  } else {
    purchaseStore.approveExpenseMonth(pk, true)
      .then(() => {
        retrieveAllEmployeeExpenses()
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
  showDenyDialog.value = false
  const pk = selectedMonthExpenseMonth()?.pk
  if (!pk) {
    quasar.notify({
      message: 'No expenses to approve',
      color: 'negative',
      icon: 'cancel'
    })
    return
  } else {
    purchaseStore.approveExpenseMonth(pk, false)
      .then(() => {
        retrieveAllEmployeeExpenses()
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
  const employeePK = getRouteParam(route, 'employeePK')
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
  getEmployeeFromRoute().then(() => {
    if (purchaseStore.fiscalExpenseMonths.length === 0) {
      retrieveThisMonthEmployeeExpenses().then(() => {
        window.print()
      })
    } else {
      window.print()
    }
  })
}

onMounted(() => {
  if (props.print) {
    handlePrint()
  } else {
    setDates().then(() => {
      getEmployeeFromRoute().then(() => {
        if (purchaseStore.fiscalExpenseMonths.length === 0) {
          retrieveThisMonthEmployeeExpenses().then(() => {
            retrieveAllEmployeeExpenses()
          })
        }
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

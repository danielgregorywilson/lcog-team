<template>
<div class="q-mt-md">
  <div class="q-mt-md">
    <q-spinner-grid
      v-if="!expensesLoaded()"
      class="spinner"
      color="primary"
      size="xl"
    />
    <div v-else>
      <q-table
        flat bordered
        :title="monthDisplay"
        :rows="selectedMonthExpenseMonths()"
        :columns="columns"
        row-key="name"
        binary-state-sort
        :pagination="pagination"
        class="expense-table"
        no-data-label="No expenses entered this month"
      >
        <template v-slot:body="props">
          <q-tr
            :props="props"
            class="cursor-pointer"
            @click="navigateToDetail(props.row.purchaser.pk)"
          >
            <q-td key="employee" :props="props">
              {{ props.row.purchaser.name }}
            </q-td>
            <q-td key="status" :props="props">
              <q-linear-progress
                size="25px"
                rounded
                :value="progressBarSize(props.row.status)"
                :color="progressBarColor(props.row.status)"
              >
                <div class="absolute-full flex flex-center">
                  <q-badge
                    color="white"
                    :text-color="progressBarColor(props.row.status)"
                    :label="progressBarLabel(props.row.status)"
                  />
                </div>
              </q-linear-progress>
            </q-td>
            <q-td key="approved" :props="props">
              <q-icon
                v-if="expenseMonthFiscalApproved(props.row)"
                color="green"
                name="check_circle"
                size="lg"
              />
              <q-icon
                v-else-if="expenseMonthFiscalDenied(props.row)"
                color="red"
                name="cancel"
                size="lg"
              />
            </q-td>
          </q-tr>
        </template>
      </q-table>
    </div>
    <div class="q-mt-sm">
      <div class="text-h5 text-center">Expense Statements</div>
      <div class="row justify-between q-gutter-md q-mt-none">
        <div class="col">
          <q-spinner-grid
            v-if="!statementsLoaded"
            class="spinner"
            color="primary"
            size="xl"
          />
          <div v-else>
            <q-table
              flat bordered dense
              :rows="selectedMonthStatements()"
              :columns="statementCols"
              row-key="name"
              binary-state-sort
              :pagination="pagination"
              class="expense-table"
            >
              <template v-slot:body-cell-card="props">
                <q-td key="card" :props="props">
                  {{ props.row.card.display }}
                </q-td>
              </template>
              <template v-slot:body-cell-actions="props">
                <q-td key="actions" :props="props">
                  <q-btn
                    icon="visibility"  
                    round
                    flat    
                    @click="showStatmentDialog(props.row)"
                  />
                  <q-btn
                    icon="delete"
                    round
                    flat
                    @click="showDeleteStatementDialog(props.row)"  
                  />
                </q-td>
              </template>
            </q-table>
          </div>
        </div>
        <div class="col row justify-center">
          <div class="text-h6">
            Upload Statements for {{ monthDisplay }}
          </div>
          <FileUploader
              :file=selectedFiles
              multiple
              contentTypeAppLabel="purchases"
              contentTypeModel="expensestatement"
              :data="{
                'year': props.yearInt,
                'month': props.monthInt
              }"
              :readOnly=false
              v-on="{
                'uploaded': (url: string) => {
                  retrieveAllStatements()
                }
              }"
            />
        </div>
      </div>
    </div>
  </div>

  <!-- Statement Dialog -->
  <q-dialog v-model="statementDialogVisible">
    <q-card>
      <q-card-section>
        <div class="row items-center">
          <q-avatar
            icon="book"
            color="primary"
            text-color="white"
          />
          <span class="q-ml-sm">
            Card Number:
            <span class="text-bold">{{ statementDialogStatement.card.display }}</span>
          </span>
        </div>
        <q-markup-table class="q-mt-md">
          <thead>
            <tr>
              <th>Date</th>
              <th>Item</th>
              <th>Amount</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in statementDialogStatement.items" :key="item.pk">
              <td>{{ readableDateNEW(item.date) }}</td>
              <td>{{ item.description }}</td>
              <td>${{ item.amount }}</td>
            </tr>
          </tbody>
        </q-markup-table>
      </q-card-section>

      <q-card-actions class="row justify-around">
        <q-btn flat label="Close" color="primary" v-close-popup />
        <q-btn
          flat
          label="Delete"
          color="primary"
          @click="showDeleteStatementDialog(statementDialogStatement)"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>

  <!-- Delete Statement Dialog -->
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
            Are you sure you want to delete this statement?
          </span>
        </div>
        <div
          v-if="deleteDialogStatementNumber"
          class="row justify-center text-center"
        >
          Number: {{ deleteDialogStatementNumber }}
        </div>
        <div class="row justify-center text-center">
          Month: {{ monthDisplay }}
        </div>
      </q-card-section>

      <q-card-actions class="row justify-around">
        <q-btn flat label="Cancel" color="primary" v-close-popup />
        <q-btn
          flat
          label="Yes, delete it"
          color="primary"
          @click="deleteStatement()"
          v-close-popup
        />
      </q-card-actions>
    </q-card>
  </q-dialog>

</div>
</template>

<style scoped lang="scss"></style>

<script setup lang="ts">
import { useQuasar } from 'quasar'
import { onMounted, Ref, ref } from 'vue'
import { useRouter } from 'vue-router'
import FileUploader from 'src/components/FileUploader.vue'
import { readableDateNEW } from 'src/filters'
import { handlePromiseError } from 'src/stores'
import { usePurchaseStore } from 'src/stores/purchase';
import { ExpenseMonth, ExpenseStatement } from 'src/types';

const quasar = useQuasar()
const router = useRouter()
const purchaseStore = usePurchaseStore()

const props = defineProps<{
  monthDisplay: string
  monthInt: number
  yearInt: number
}>()

let thisMonthExpensesLoaded = ref(false)
let allExpensesLoaded = ref(false)
let thisMonthStatementsLoaded = ref(false)
let allStatementsLoaded = ref(false)

let firstOfThisMonth = ref(new Date())
let firstOfSelectedMonth = ref(new Date())

let statementDialogVisible = ref(false)
let statementDialogStatement = ref({}) as Ref<ExpenseStatement>

let deleteDialogVisible = ref(false)
let statementPkToDelete = ref(-1)
let deleteDialogStatementNumber = ref('')

let selectedFiles = ref(new File([''], ''))

const pagination = {
  rowsPerPage: 50
}

const columns = [
  {
    name: 'employee', required: true, label: 'Name', sortable: true,
    align: 'left'
  },
  {
    name: 'status', label: 'Status', field: 'status', sortable: true,
    align: 'center'
  },
  {
    name: 'approved', label: 'Fiscal Approved', field: 'approved', sortable: true,
    align: 'center'
  }
]

const statementCols = [
  {
    name: 'card', required: true, label: 'Card', field: 'card', sortable: true,
    align: 'center'
  },
  { name: 'actions', label: 'Actions', field: 'actions', align: 'center' }
]

function viewingThisMonth() {
  return firstOfSelectedMonth.value.getTime() ===
    firstOfThisMonth.value.getTime()
}

function expensesLoaded() {
  return (viewingThisMonth() && thisMonthExpensesLoaded.value) ||
    allExpensesLoaded.value
}

function statementsLoaded() {
  return (viewingThisMonth() && thisMonthStatementsLoaded.value) ||
    allStatementsLoaded.value
}

function selectedMonthExpenseMonths() {
  return purchaseStore.fiscalExpenseMonths
    .filter(em => em.month == props.monthInt && em.year == props.yearInt)
}

function selectedMonthStatements() {
  return purchaseStore.expenseStatements
    .filter(s => s.month === props.monthInt && s.year == props.yearInt)
}

function expenseMonthFiscalApproved(expenseMonth: ExpenseMonth) {
  return expenseMonth.status == 'fiscal_approved'
}

function expenseMonthFiscalDenied(expenseMonth: ExpenseMonth) {
  return expenseMonth.status == 'fiscal_denied'
}

function progressBarSize(status: string) {
  switch (status) {
    case 'draft':
      return 0
    case 'submitted':
    case 'approver_denied':
      return .25
    case 'approver_approved':
    case 'director_denied':
      return .5
    case 'director_approved':
    case 'fiscal_denied':
      return .75
    case 'fiscal_approved':
      return 1
    default:
      return 0
  }
}

function progressBarLabel(status: string) {
  switch (status) {
    case 'draft':
      return 'Not Submitted'
    case 'submitted':
      return 'Submitted by Employee'
    case 'approver_denied':
      return 'Denied by Manager'
    case 'approver_approved':
      return 'Approved by Manager'
    case 'director_denied':
      return 'Denied by Director'
    case 'director_approved':
      return 'Approved by Director'
    case 'fiscal_denied':
      return 'Denied by Fiscal'
    case 'fiscal_approved':
      return 'Approved by Fiscal'
    default:
      return 'Unknown'
  }
}

function progressBarColor(status: string) {
  switch (status) {
    case 'draft':
      return 'grey'
    case 'submitted':
      return 'blue'
    case 'approver_denied':
    case 'director_denied':
    case 'fiscal_denied':
      return 'red'
    case 'approver_approved':
    case 'director_approved':
    case 'fiscal_approved':
      return 'green'
    default:
      return 'grey'
  }
}

function retrieveThisMonthEMs(): Promise<void> {
  return new Promise((resolve, reject) => {
    purchaseStore.getFiscalExpenseMonths(props.yearInt, props.monthInt)
      .then(() => {
        thisMonthExpensesLoaded.value = true
        resolve()
      })
      .catch((error) => {
        handlePromiseError(reject, 'Error retrieving fiscal expenses', error)
        reject()
      })
  })
}

function retrieveAllEMs(): Promise<void> {
  return new Promise((resolve, reject) => {
    purchaseStore.getFiscalExpenseMonths()
      .then(() => {
        allExpensesLoaded.value = true
        resolve()
      })
      .catch((error) => {
        handlePromiseError(reject, 'Error retrieving fiscal expenses', error)
        reject()
      })
  })
}

function retrieveThisMonthStatements(): Promise<void> {
  return new Promise((resolve, reject) => {
    purchaseStore.getExpenseStatements(props.yearInt, props.monthInt)
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

function navigateToDetail(employeePk: number) {
  router.push({
    name: 'fiscal-approve-expenses-detail',
    params: {
      employeePK: employeePk.toString(),
      year: props.yearInt,
      month: props.monthInt
    }
  })
  .catch(e => {
    console.error('Error navigating to time off request detail:', e)
  })
}

function showStatmentDialog(statement: any) {
  statementDialogStatement.value = statement
  statementDialogVisible.value = true
}

function showDeleteStatementDialog(statement: any) {
  deleteDialogStatementNumber.value = statement.card.display
  statementPkToDelete.value = statement.pk
  deleteDialogVisible.value = true
}

function deleteStatement(): void {
  purchaseStore.deleteExpenseStatement(statementPkToDelete.value)
    .then(() => {
      statementDialogVisible.value = false
      quasar.notify('Deleted a statement.')
      retrieveAllStatements()
    })
    .catch(e => {
      console.error(e)
    })
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
  retrieveThisMonthEMs().then(() => {
    retrieveAllEMs()
  })
  retrieveThisMonthStatements().then(() => {
    retrieveAllStatements()
  })
})

</script>

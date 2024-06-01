<template>
<div class="q-mt-md">
  <div class="q-gutter-md">
    <q-btn v-if="monthSubmitted()" @click="showUnsubmitDialog = true">
      Unsubmit
    </q-btn>
    <q-btn v-else @click="showSubmitDialog = true" :disabled="formErrors()">
      Submit for Approval
    </q-btn>
    <q-btn v-if="formErrors()" @click="showErrorsDialog = true">
      <div>Correct Errors</div>
      <q-icon color="orange" name="warning" size="md" />
    </q-btn>
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
      :dense="$q.screen.lt.lg"
      :grid="$q.screen.lt.md"
      row-key="name"
      binary-state-sort
      :pagination="pagination"
      class="expense-table"
    >
      <template v-slot:body="props">

        <q-tr
          :props="props"
          :class="rowSubmitted(props.row)?'bg-grey':'cursor-pointer'"
        >
          <q-td key="name" :props="props">
            {{ props.row.name }}
            <q-popup-edit
              v-if="!rowSubmitted(props.row)"
              v-model="props.row.name"
              buttons
              v-slot="scope"
              @save="(val) => updateExpense(props.row.pk, 'name', val)"
            >
              <q-input v-model="scope.value" dense autofocus />
            </q-popup-edit>
          </q-td>
          <q-td key="date" :props="props">
            {{ readableDateNEW(props.row.date) }}
            <q-popup-edit
              v-if="!rowSubmitted(props.row)"
              v-model="props.row.date"
              buttons
              v-slot="scope"
              @save="(val) => updateExpense(props.row.pk, 'date', val)"
            >
              <q-input type="date" v-model="scope.value" dense autofocus />
            </q-popup-edit>
          </q-td>
          <q-td key="description" :props="props">
            <div class="text-pre-wrap">{{ props.row.description }}</div>
            <q-popup-edit
              v-if="!rowSubmitted(props.row)"
              v-model="props.row.job"
              buttons
              v-slot="scope"
              @save="(val) => updateExpense(props.row.pk, 'description', val)"
            >
              <q-input v-model="scope.value" dense autofocus />
            </q-popup-edit>
          </q-td>
          <q-td key="vendor" :props="props">
            <div class="text-pre-wrap">{{ props.row.vendor }}</div>
            <q-popup-edit
              v-if="!rowSubmitted(props.row)"
              v-model="props.row.vendor"
              buttons
              v-slot="scope"
              @save="(val) => updateExpense(props.row.pk, 'vendor', val)"
            >
              <q-input v-model="scope.value" dense autofocus />
            </q-popup-edit>
          </q-td>
          <q-td key="job" :props="props">
            <div class="text-pre-wrap">{{ props.row.job }}</div>
            <q-popup-edit
              v-if="!rowSubmitted(props.row)"
              v-model="props.row.job"
              buttons
              v-slot="scope"
              @save="(val) => updateExpense(props.row.pk, 'job', val)"
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
              v-if="!rowSubmitted(props.row)"
              v-model="props.row.gls"
              buttons
              v-slot="scope"
              @save="(val) => updateExpense(props.row.pk, 'gls', val)"
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
              <q-btn @click="scope.value.push({gl: '', percent: 100})">
                Add a GL
              </q-btn>
            </q-popup-edit>
          </q-td>
          <q-td key="approver" :props="props">
            {{ props.row.approver?.name }}
            <q-popup-edit
              v-if="!rowSubmitted(props.row)"
              v-model="props.row.approver"
              buttons
              v-slot="scope"
              @save="(val) => updateExpense(props.row.pk, 'approver', val)"
            >
              <EmployeeSelect
                name="approver"
                label="Approver"
                :employee="scope.value"
                :useLegalName="true"
                v-on:input="scope.value=$event"
                v-on:clear="scope.value=emptyEmployee"
                :readOnly=false
                :employeeFilterFn="(employee: SimpleEmployeeRetrieve) => {
                  return employee.is_expense_approver
                }"
              />
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
                :disable="rowSubmitted(props.row)"
              >
                <q-popup-edit
                  v-if="!rowSubmitted(props.row)"
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
                    allowedFileTypes="image/*,.pdf"
                    v-on="{
                      'uploaded': (url: string) => {
                        retrieveAllMyExpenses()
                      }
                    }"
                  />
                  <div class="q-mt-sm">
                    Supported filetypes: Images and PDFs
                  </div>
                </q-popup-edit>
              </q-btn>
            </div>
          </q-td>
        </q-tr>
      </template>
      <!-- For grid mode, we need to specify everything in order for our action buttons to render -->
      <template v-slot:item="props">
        <div class="q-pa-xs col-xs-12 col-sm-6 col-md-4 col-lg-3">
          <q-card class="q-py-sm" :class="rowSubmitted(props.row)?'bg-grey':'cursor-pointer'">
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
                      {{ gl.gl }}: {{ gl.percent }}%
                    </div>
                  </div>
                  <div
                      class="q-table__grid-item-value"
                      v-else-if="col.label == 'Approver'"
                    >
                      {{ col.value.name }}
                    </div>
                  <div
                    class="q-table__grid-item-value row"
                    v-else-if="col.label == 'Receipt'"
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
                      :disable="rowSubmitted(props.row)"
                    >
                      <q-popup-edit
                        v-if="!rowSubmitted(props.row)"
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
                          allowedFileTypes="image/*,.pdf"
                          v-on="{
                            'uploaded': (url: string) => {
                              retrieveAllMyExpenses()
                            }
                          }"
                        />
                        <div class="q-mt-sm">
                          Supported filetypes: Images and PDFs
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
      <template v-slot:bottom-row v-if="!monthSubmitted()">
        <q-tr @click="clickAddExpense()" class="cursor-pointer row-add-new">
          <q-td colspan="100%">
            <q-icon name="add" size="md" class="q-pr-sm"/>New Expense
          </q-td>
        </q-tr>
      </template>
    </q-table>
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

  <!-- Submit to Fiscal Dialog -->
  <q-dialog v-model="showSubmitDialog">
    <q-card class="q-pa-md" style="width: 400px">
      <div class="text-h6">
        Submit {{ monthDisplay }} expenses for approval?
      </div>
      <q-form
        @submit='onSubmitDialog()'
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

import DocumentViewer from 'src/components/DocumentViewer.vue'
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

let showErrorsDialog = ref(false)
let showSubmitDialog = ref(false)
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
  { name: 'approver', field: 'approver', label: 'Approver', align: 'center' },
  { name: 'receipt', field: 'receipt', label: 'Receipt', align: 'center' }
]


function tableTitleDisplay(): string {
  const submittedText = monthSubmitted() ? ' - Submitted' : ''
  return `${props.monthDisplay}${submittedText}`
}

function selectedMonthExpenses(): Expense[] {
  const apiResults = purchaseStore.myExpenses
  let exps: Expense[] = []
  if (apiResults) {
    exps = apiResults.filter(exp => {
      let [y, m] = exp.date.split('-').map(s => parseInt(s))
      return m === props.monthInt && y === props.yearInt
    })
  }
  return exps
}

function monthSubmitted() {
  const ems = purchaseStore.expenseMonths
  return ems.some(em => {
    return em.month === props.monthInt && em.year === props.yearInt &&
      em.status !== 'draft'
  })
}

function rowSubmitted(row: Expense) {
  return ['submitted', 'approver_approved', 'fiscal_approved']
    .includes(row.status)
}

function clickAddExpense(): void {

  purchaseStore.createExpense({
    name: '',
    date: `${ props.yearInt }-${ props.monthInt }-${ props.dayInt }`,
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
    for (let gl of exp.gls) {
      if (!gl.gl || gl.gl.length !== 12) {
        errorItems.push(`Provide a valid GL code for each GL row in ${exp.name}`)
      }
      if (!gl.percent) {
        errorItems.push(`Provide a GL percentage for each GL row in ${exp.name}`)
      }
    }
    const GLsTotal = exp.gls.reduce((acc, gl) => acc + parseFloat(gl.percent), 0)
    if (GLsTotal !== 100) {
      errorItems.push(`GL percentages of ${exp.name} must add to 100`)
    }
    if (!exp.approver || exp.approver?.pk == -1) {
      errorItems.push(`Provide an approver for ${exp.name}`)
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

function onSubmitDialog() {
  purchaseStore.submitExpenseMonth({
    yearInt: props.yearInt, monthInt: props.monthInt
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
    yearInt: props.yearInt, monthInt: props.monthInt, unsubmit: true
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

function retrieveThisMonthExpenses(): Promise<void> {
  return new Promise((resolve, reject) => {
    purchaseStore.getExpenseMonths(props.yearInt, props.monthInt)
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
  field:
    'name' | 'date' | 'description' | 'vendor' | 'job' | 'gls' | 'approver',
  val: string | Array<GL> | SimpleEmployeeRetrieve
) {
  const exp = purchaseStore.myExpenses.find(exp => exp.pk === pk)
  if (exp) {
    if (field === 'gls') {
      exp.gls = val as Array<GL>
    } else if (field === 'approver') {
      exp.approver = val as SimpleEmployeeRetrieve
    } else {
      exp[field] = val as string
    }
    purchaseStore.updateExpense(exp)
      .catch((error) => {
        console.log('Error updating expense', error)
      })
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

<template>
<div class="q-mt-md">
  <div class="q-mt-md">
    <q-spinner-grid
      v-if="!expensesLoaded"
      class="spinner"
      color="primary"
      size="xl"
    />
    <div v-else>
      <div v-if="largeExpense()" class="text-h6 text-warning">
        Take Note! Expense of $1000 or more
      </div>
      <q-table
        flat bordered
        :title="tableTitleDisplay()"
        :rows="selectedMonthExpenseGLs()"
        :columns="columns"
        :dense="$q.screen.lt.lg"
        :grid="$q.screen.lt.md"
        row-key="name"
        binary-state-sort
        :pagination="pagination"
        class="expense-table"
        no-data-label="No expenses entered this month"
      >
        <template v-slot:body-cell-expense_name="props">
          <q-td key="expense_name" :props="props" style="white-space: normal;">
            {{ props.row.expense_name }}
            <q-popup-edit
              v-if="!monthLocked()"
              v-model="props.row.expense_name"
              buttons
              v-slot="scope"
              @save="(val: string) => updateGL(props.row.pk, 'name', val)"
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
        </template>
        <template v-slot:body-cell-expense_date="props">
          <q-td key="expense_date" :props="props">
            {{ readableDateNEW(props.row.expense_date) }}
            <q-popup-edit
              v-if="!monthLocked()"
              v-model="props.row.expense_date"
              buttons
              v-slot="scope"
              @save="(val: string) => updateGL(props.row.pk, 'date', val)"
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
        </template>
        <template v-slot:body-cell-expense_vendor="props">
          <q-td
            key="expense_vendor"
            :props="props"
            style="white-space: normal;"
          >
            {{ props.row.expense_vendor }}
            <q-popup-edit
              v-if="!monthLocked()"
              v-model="props.row.expense_vendor"
              buttons
              v-slot="scope"
              @save="(val: string) => updateGL(props.row.pk, 'vendor', val)"
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
        </template>
        <template v-slot:body-cell-expense_amount="props">
          <q-td
            key="expense_amount"
            :props="props"
            style="white-space: normal;"
            :class="props.row.amount >= 1000 ? 'bg-yellow' : ''"
          >
            ${{ props.row.amount }}
          </q-td>
        </template>
        <template v-slot:body-cell-gl="props">
          <q-td key="gl" :props="props">
            <span>{{ props.row.code }} (Job: {{ props.row.job }}</span>
            <span v-if="props.row.activity">, Activity: {{ props.row.activity }}</span>
            <span>): ${{ props.row.amount }}</span>
            <q-popup-edit
              v-if="!monthLocked()"
              v-model="props.row"
              buttons
              v-slot="scope"
              :validate="GLValidation"
              @save="(val: GLWithApprover) => {updateGL(props.row.pk, 'gl', {
                'code': val.code,
                'job': val.job,
                'activity': val.activity,
                'approver': val.approver
              })}"
            >
              <div class="gl-popup-edit">
                <q-input
                  v-model="scope.value.code"
                  class="q-mr-sm q-pa-none"
                  outlined dense autofocus
                  mask="###-##-####-#####"
                  fill-mask="___-__-____-_____"
                  :rules="[
                    (val: string) => !!val || 'Required',
                  ]"
                />
                <q-input
                  v-model="scope.value.job"
                  label="Job #" stack-label
                  class="q-mr-sm q-pa-none"
                  outlined dense
                  :rules="[
                    (val: string) => !!val || 'Required or \'None\'',
                  ]"
                />
                <q-input
                  v-model="scope.value.activity"
                  label="Activity #" stack-label
                  class="q-mr-sm q-pa-none"
                  outlined dense
                  maxlength="7"
                />
                <div class="row q-mr-sm">
                  ${{  scope.value.amount }}
                  <!-- <div class="gl-dollar-symbol">$</div>
                  <q-input
                    v-model="gl.amount"
                    class="gl-amount q-pa-none"
                    outlined
                    dense
                    :error="errorAmount"
                    :error-message="errorMessageAmount"
                    @keyup.enter="scope.set()"
                    :rules="[
                      (val: string) => !!val || '* Required',
                    ]"
                  /> -->
                </div>
                <EmployeeSelect
                  name="approver"
                  label="Approver"
                  :employee="scope.value.approver"
                  :useLegalName="true"
                  v-on:input="scope.value.approver=$event"
                  v-on:clear="scope.value.approver=emptyEmployee"
                  :readOnly=false
                  :employeeFilterFn="
                    (employee: SimpleEmployeeRetrieve) => {
                      return employee.is_expense_approver
                    }
                  "
                />
              </div>
            </q-popup-edit>
          </q-td>
        </template>
        <template v-slot:body-cell-receipt="props">
          <q-td key="receipt" :props="props">
            <DocumentViewer
              v-if="props.row.expense_receipt"
              :documentUrl="props.row.expense_receipt"
              iconButton
              flat
            />
          </q-td>
        </template>
        <template v-slot:body-cell-note="props">
          <q-td key="em_note" :props="props">
            <q-icon v-if="props.row.em_note" name="note" size="md">
              <q-tooltip class="text-body2 bg-info text-black">
                {{ props.row.em_note }}
              </q-tooltip>
            </q-icon>
          </q-td>
        </template>
        <template v-slot:body-cell-approve="props">
          <q-td :props="props" style="min-width: 100px;">
            <div class="row justify-center">
              {{ props.row.status }}
              <q-btn 
                dense round color="red" icon="close"
                :outline="!props.row.approved_at ||
                  (props.row.approved_at && props.row.approved)"
                :disable="!canApprove ||
                  (props.row.approved_at && !props.row.approved)"
                class="q-mr-sm"
                @click="openDenyGLDialog(
                  props.row.pk,
                  props.row.expense_name,
                  props.row.expense_purchaser
                )"
              />
              <q-btn
                dense round color="green" icon="check"
                :outline="!props.row.approved_at ||
                  (props.row.approved_at && !props.row.approved)"
                :disable="!canApprove ||
                  (props.row.approved_at && props.row.approved)"
                @click="approveGL(props.row.pk, true)"
              />
            </div>
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
                      v-if="col.label == 'Purchaser'"
                    >
                      {{ col.value.name }}
                    </div>
                    <div
                      class="q-table__grid-item-value"
                      v-else-if="col.label == 'Date'"
                    >
                      {{ readableDateNEW(col.value) }}
                    </div>
                    <div
                      class="q-table__grid-item-value"
                      v-else-if="col.label == 'Amount'"
                      :class="props.row.amount >= 1000 ? 'bg-yellow' : ''"
                    >
                      ${{ col.value }}
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
                        {{ gl.gl }}: ${{ gl.amount }}
                      </div>
                    </div>
                    <div
                      class="q-table__grid-item-value"
                      v-else-if="col.label == 'Receipt'"
                    >
                      <DocumentViewer
                        v-if="col.value"
                        :documentUrl="col.value"
                        :iconButton="true"
                      />
                    </div>
                    <div
                      v-else-if="col.label == 'Approve?'"  
                      class="q-table__grid-item-value row q-gutter-sm"  
                    >
                      <q-btn 
                        dense round color="red" icon="close"
                        :outline="!props.row.approved_at ||
                          (props.row.approved_at && props.row.approved)"
                        :disable="!canApprove ||
                          (props.row.approved_at && !props.row.approved)"
                        class="q-mr-sm"
                        @click="openDenyGLDialog(
                          props.row.pk,
                          props.row.expense_name,
                          props.row.expense_purchaser
                        )"
                      />
                      <q-btn
                        dense round color="green" icon="check"
                        :outline="!props.row.approved_at ||
                          (props.row.approved_at && !props.row.approved)"
                        :disable="!canApprove ||
                          (props.row.approved_at && props.row.approved)"
                        @click="approveGL(props.row.pk, true)"
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
    </div>
  </div>

  <!-- Deny ExpenseGL Dialog -->
  <q-dialog v-model="showDenyDialog">
    <q-card class="q-pa-md" style="width: 400px">
      <div class="text-h6">
        Deny {{ deniedGLPurchaserName }}'s purchase of {{deniedGLExpenseName}}?
      </div>
      <q-form
        @submit='approveGL(deniedGLPK, false)'
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
.gl-popup-edit {
  min-width: 993px;
}
</style>

<script setup lang="ts">
import { onMounted, ref } from 'vue'

import DocumentViewer from 'src/components/DocumentViewer.vue'
import EmployeeSelect from 'src/components/EmployeeSelect.vue'
import { readableDateNEW } from 'src/filters'
import { handlePromiseError } from 'src/stores'
import { usePurchaseStore } from 'src/stores/purchase'
import {
  emptyEmployee, GL, GLWithApprover, SimpleEmployeeRetrieve
} from 'src/types'

const purchaseStore = usePurchaseStore()

let thisMonthLoaded = ref(false)
let allExpensesLoaded = ref(false)

let showDenyDialog = ref(false)
let deniedGLPK = ref(0)
let deniedGLExpenseName = ref('')
let deniedGLPurchaserName = ref('')
let denyDialogMessage = ref('')

let errorAmount = ref(false)
let errorMessageAmount = ref('')

const canApprove = ref(true)

const pagination = {
  rowsPerPage: '50'
}

const columns = [
  { 
    name: 'expense_purchaser', field: 'expense_purchaser', label: 'Purchaser',
    required: true, align: 'left', sortable: true
  },
  {
    name: 'expense_name', field: 'expense_name', label: 'Item', required: true,
    align: 'left', sortable: true
  },
  {
    name: 'expense_date', field: 'expense_date', label: 'Date', align: 'center',
    sortable: true
  },
  {
    name: 'expense_vendor', field: 'expense_vendor', label: 'Vendor',
    align: 'center', sortable: true
  },
  {
    name: 'expense_amount', field: 'expense_amount', label: 'Amount',
    align: 'center'
  },
  {
    name: 'gl', field: 'gl', label: 'GL Code', align: 'center',
    sortable: true, style: 'width: 10px'
  },
  { name: 'receipt', field: 'receipt', label: 'Receipt', align: 'center' },
  { name: 'note', field: 'em_note', label: 'Note', align: 'center' },
  { name: 'approve', label: 'Approve?', field: 'approved', align: 'center' },
]

function viewingThisMonth() {
  return purchaseStore.firstOfSelectedMonth.getTime() ===
    purchaseStore.firstOfThisMonth.getTime()
}

function expensesLoaded() {
  return (viewingThisMonth() && thisMonthLoaded.value) ||
    allExpensesLoaded.value
}

function largeExpense() {
  return selectedMonthExpenseGLs().some(gl => parseFloat(gl.amount) >= 1000)
}

function tableTitleDisplay(): string {
  return `${purchaseStore.monthDisplay} - Expenses to Approve`
}

function selectedMonthExpenseGLs(): GL[] {
  const apiResults = purchaseStore.approvalExpenseGLs
  let gls: GL[] = []
  if (apiResults) {
    gls = apiResults.filter(gl => {
      return gl.em_month === purchaseStore.monthInt && 
        gl.em_year === purchaseStore.yearInt
    })
  }
  return gls
}

function retrieveThisMonthExpenseGLsToApprove(): Promise<void> {
  return new Promise((resolve, reject) => {
    purchaseStore.getApprovalGLs(purchaseStore.yearInt, purchaseStore.monthInt)
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

function retrieveAllExpenseGLsToApprove(): Promise<void> {
  return new Promise((resolve, reject) => {
    purchaseStore.getApprovalGLs()
      .then(() => {
        allExpensesLoaded.value = true
        resolve()
      })
      .catch((error) => {
        handlePromiseError(reject, 'Error retrieving expenses', error)
        reject()
      })
  })
}

function monthLocked() {
  return purchaseStore.expenseMonthLocked
}

function updateGL(
  pk: number,
  field: 'name' | 'date' | 'vendor' | 'gl',
  val: string | {
    'code': string, 'job': string, 'activity': string,
    'approver': SimpleEmployeeRetrieve
  }
) {
  if (monthLocked()) {
    return
  }
  purchaseStore.updateGL(pk, field, val)
    .then(() => {
      retrieveThisMonthExpenseGLsToApprove()
    })
    .catch((error) => {
      console.log('Error updating expense GL', error)
    })
}

function approveGL(pk: number, approved: boolean) {
  canApprove.value = false
  setTimeout(() => {
    canApprove.value = true
  }, 1500)
  purchaseStore.approveGL(pk, approved, denyDialogMessage.value)
    .then(() => {
      retrieveAllExpenseGLsToApprove()
      showDenyDialog.value = false
      denyDialogMessage.value = ''
    })
    .catch((error) => {
      console.log('Error approving GL', error)
    })
}

function  openDenyGLDialog(
  pk: number, expenseName: string, purchaserName: string
) {
  deniedGLPK.value = pk
  deniedGLExpenseName.value = expenseName
  deniedGLPurchaserName.value = purchaserName
  showDenyDialog.value = true
}

function GLValidation (gl: any) {
  if (isNaN(parseFloat(gl.amount))) {
    errorAmount.value = true
    errorMessageAmount.value = 'The value must be a number!'
    return false
  }
  errorAmount.value = false
  errorMessageAmount.value = ''
  return true
}

onMounted(() => {
  retrieveThisMonthExpenseGLsToApprove().then(() => {
    retrieveAllExpenseGLsToApprove()
  })
})

</script>

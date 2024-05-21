import axios from 'axios'
import { defineStore } from 'pinia'
import ApproveExpenses from 'src/pages/purchases/ApproveExpenses.vue'
import ExpensesBase from 'src/pages/purchases/ExpensesBase.vue'

import { apiURL, handlePromiseError } from 'src/stores/index'
import { Expense, ExpenseCreate, ExpenseMonth } from 'src/types'

export const usePurchaseStore = defineStore('purchase', {
  state: () => ({
    expenseMonths: [] as Array<ExpenseMonth>,
    myExpenses: [] as Array<Expense>,
    approvalExpenses: [] as Array<Expense>,
    numExpensesToApprove: 0,
    numExpensesFiscalToApprove: 0
  }),

  getters: {},

  actions: {
    createExpense(data: ExpenseCreate): Promise<Expense> {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/expense`, method: 'POST', data })
          .then((resp) => {
            resolve(resp.data)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error creating expense', e)
          })
      })
    },
    updateExpense(data: Expense): Promise<Expense> {
      return new Promise((resolve, reject) => {
        axios({
          url: `${ apiURL }api/v1/expense/${ data.pk }`, method: 'PUT', data
        })
          .then((resp) => {
            resolve(resp.data)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error updating expense', e)
          })
      })
    },
    
    /////////////////
    /// Submitter ///
    /////////////////

    getExpenseMonths(
      yearInt: number | null = null, monthInt: number | null = null
    ): Promise<null> {
      return new Promise((resolve, reject) => {
        let dateParam = ''
        if (!!yearInt && !!monthInt) {
          dateParam = `?year=${ yearInt }&month=${ monthInt }`
        }
        axios({
          url: `${ apiURL }api/v1/expensemonth${ dateParam }`
        })
          .then(resp => {
            const ems = resp.data.results
            this.expenseMonths = ems
            let expenses = [] as Array<Expense>
            for (const em of ems) {
              expenses = expenses.concat(em.expenses)
            }
            this.myExpenses = expenses
            resolve(resp.data.results)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error getting expense months', e)
          })
      })
    },
    submitExpenseMonth(
      data: { yearInt: number, monthInt: number, unsubmit?: boolean }
    ): Promise<null> {
      return new Promise((resolve, reject) => {
        axios({
          url: `${ apiURL }api/v1/expensemonth/submit`,
          data: data,
          method: 'POST'
        })
          .then(() => {
            resolve(null)
          })
          .catch(e => {
            handlePromiseError(
              reject,
              `Error ${ data['unsubmit'] ? 'un' : ''}submitting expense month`,
              e
            )
          })
      })
    },

    ////////////////
    /// Approver ///
    ////////////////

    getApprovalExpenses(
      yearInt: number | null = null,
      monthInt: number | null = null
    ): Promise<null> {
      return new Promise((resolve, reject) => {
        let params = `?approve=true`
        if (!!yearInt && !!monthInt) {
          params = `?year=${ yearInt }&month=${ monthInt }&approve=true`
        }
        axios({
          url: `${ apiURL }api/v1/expense${ params }`
        })
          .then(resp => {
            const exps = resp.data.results
            let toApproveCount = 0
            let expenses = [] as Array<Expense>
            for (const exp of exps) {
              if (exp.status == 'submitted') {
                toApproveCount++
              }
              expenses = expenses.concat(exp)
            }
            this.approvalExpenses = expenses
            this.numExpensesToApprove = toApproveCount
            resolve(resp.data.results)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error getting approval expenses', e)
          })
      })
    },

    approveExpense(pk: number, approve: boolean): Promise<Expense> {
      return new Promise((resolve, reject) => {
        axios({
          url: `${ apiURL }api/v1/expense/${ pk }/approve`,
          method: 'PUT',
          data: { approve }
        })
          .then(resp => {
            resolve(resp.data)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error approving expense', e)
          })
      })
    },

    authLogout() {
      return new Promise((resolve) => {
        this.$reset()
        resolve('Successfully triggered logout')
      })
    }
  }
})

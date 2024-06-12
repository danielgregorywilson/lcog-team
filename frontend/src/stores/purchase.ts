import axios from 'axios'
import { defineStore } from 'pinia'

import { apiURL, handlePromiseError } from 'src/stores/index'
import { Expense, ExpenseCreate, ExpenseMonth, GL } from 'src/types'

export const usePurchaseStore = defineStore('purchase', {
  state: () => ({
    expenseMonths: [] as Array<ExpenseMonth>,
    myExpenses: [] as Array<Expense>,
    approvalExpenseGLs: [] as Array<GL>,
    fiscalExpenseMonths: [] as Array<ExpenseMonth>,
    numExpenseGLsToApprove: 0,
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
    deleteExpense(pk: number): Promise<null> {
      return new Promise((resolve, reject) => {
        axios({
          url: `${ apiURL }api/v1/expense/${ pk }`, method: 'DELETE'
        })
          .then(() => {
            resolve(null)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error deleting expense', e)
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
        let params = ''
        if (!!yearInt && !!monthInt) {
          params = `?year=${ yearInt }&month=${ monthInt }`
        }
        axios({
          url: `${ apiURL }api/v1/expensemonth${ params }`
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
    clearExpenseGLApprovals(pk: number): Promise<null> {
      return new Promise((resolve, reject) => {
        axios({
          url: `${ apiURL }api/v1/expense/${ pk }/clear_approvals`,
          method: 'PUT'
        })
          .then(() => {
            resolve(null)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error clearing GL approvals', e)
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

    getApprovalGLs(
      yearInt: number | null = null,
      monthInt: number | null = null
    ): Promise<null> {
      return new Promise((resolve, reject) => {
        let params = '?approve=true'
        if (!!yearInt && !!monthInt) {
          params = `?year=${ yearInt }&month=${ monthInt }&approve=true`
        }
        axios({
          url: `${ apiURL }api/v1/expense-gl${ params }`
        })
          .then(resp => {
            const expGLs = resp.data.results as Array<GL>
            let toApproveCount = 0
            let expenseGLs = [] as Array<GL>
            for (const gl of expGLs) {
              if (!gl.approved_at) {
                toApproveCount++
              }
              expenseGLs = expenseGLs.concat(gl)
            }
            this.approvalExpenseGLs = expenseGLs
            this.numExpenseGLsToApprove = toApproveCount
            resolve(resp.data.results)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error getting approval expense GLs', e)
          })
      })
    },

    approveGL(pk: number, approve: boolean): Promise<Expense> {
      return new Promise((resolve, reject) => {
        axios({
          url: `${ apiURL }api/v1/expense-gl/${ pk }/approve`,
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

    //////////////
    /// Fiscal ///
    //////////////

    getFiscalExpenseMonths(
      yearInt: number | null = null,
      monthInt: number | null = null,
      employeePK: number | null = null 
    ): Promise<null> {
      return new Promise((resolve, reject) => {
        let params = '?fiscal=true'
        if (!!yearInt && !!monthInt) {
          params += `&year=${ yearInt }&month=${ monthInt }`
        }
        if (!!employeePK) {
          params += `&employee=${ employeePK }`
        }
        axios({
          url: `${ apiURL }api/v1/expensemonth${ params }`
        })
          .then(resp => {
            const ems: ExpenseMonth[] = resp.data.results
            this.fiscalExpenseMonths = ems
            this.numExpensesFiscalToApprove = ems.filter(
              em => em.status == 'approver_approved'
            ).length
            resolve(resp.data.results)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error getting fiscal expense months', e)
          })
      })
    },

    approveExpenseMonth(pk: number, approve: boolean): Promise<ExpenseMonth> {
      return new Promise((resolve, reject) => {
        axios({
          url: `${ apiURL }api/v1/expensemonth/${ pk }/approve`,
          method: 'PUT',
          data: { approve }
        })
          .then(resp => {
            resolve(resp.data)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error approving expense month', e)
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

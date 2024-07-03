import axios from 'axios'
import { defineStore } from 'pinia'

import { apiURL, handlePromiseError } from 'src/stores/index'
import {
  Expense, ExpenseCreate, ExpenseMonth, ExpenseMonthCreate, ExpenseStatement, GL
} from 'src/types'

export const usePurchaseStore = defineStore('purchase', {
  state: () => ({
    expenseMonths: [] as Array<ExpenseMonth>,
    myExpenses: [] as Array<Expense>,
    approvalExpenseGLs: [] as Array<GL>,
    directorExpenseMonths: [] as Array<ExpenseMonth>,
    fiscalExpenseMonths: [] as Array<ExpenseMonth>,
    expenseStatements: [] as Array<ExpenseStatement>,
    numExpenseGLsToApprove: 0,
    numExpensesDirectorToApprove: 0,
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
    createExpenseMonth(data: ExpenseMonthCreate): Promise<ExpenseMonth> {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/expense-month`, method: 'POST', data })
          .then((resp) => {
            resolve(resp.data)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error creating expense month', e)
          })
      })
    },

    //////////////////
    /// Statements ///
    //////////////////

    getExpenseStatements(
      yearInt: number | null = null, monthInt: number | null = null
    ): Promise<null> {
      return new Promise((resolve, reject) => {
        let params = ''
        if (!!yearInt && !!monthInt) {
          params = `?year=${ yearInt }&month=${ monthInt }`
        }
        axios({
          url: `${ apiURL }api/v1/expense-statement${ params }`
        })
          .then(resp => {
            this.expenseStatements = resp.data.results
            resolve(resp.data.results)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error getting expense statements', e)
          })
      })
    },

    deleteExpenseStatement(pk: number): Promise<null> {
      return new Promise((resolve, reject) => {
        axios({
          url: `${ apiURL }api/v1/expense-statement/${ pk }`, method: 'DELETE'
        })
          .then(() => {
            resolve(null)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error deleting expense statement', e)
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
          url: `${ apiURL }api/v1/expense-month${ params }`
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
    setExpenseMonthCard(
      pk: number, cardPk: number
    ): Promise<ExpenseMonth> {
      return new Promise((resolve, reject) => {
        axios({
          url: `${ apiURL }api/v1/expense-month/${ pk }/set_card`,
          method: 'PUT',
          data: { cardPk: cardPk }
        })
          .then(resp => {
            resolve(resp.data)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error setting expense month card', e)
          })
      })
    },
    submitExpenseMonth(
      data: {
        yearInt: number, monthInt: number, note?: string, unsubmit?: boolean
      }
    ): Promise<null> {
      return new Promise((resolve, reject) => {
        axios({
          url: `${ apiURL }api/v1/expense-month/submit`,
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

    approveGL(
      pk: number, approve: boolean, deny_note: string
    ): Promise<Expense> {
      return new Promise((resolve, reject) => {
        axios({
          url: `${ apiURL }api/v1/expense-gl/${ pk }/approver_approve`,
          method: 'PUT',
          data: { approve, deny_note }
        })
          .then(resp => {
            resolve(resp.data)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error approving expense', e)
          })
      })
    },

    /////////////////////////
    /// Division Director ///
    /////////////////////////

    getDirectorExpenseMonths(
      yearInt: number | null = null,
      monthInt: number | null = null,
      employeePK: number | null = null
    ): Promise<null> {
      return new Promise((resolve, reject) => {
        let params = '?director=true'
        if (!!yearInt && !!monthInt) {
          params += `&year=${ yearInt }&month=${ monthInt }`
        }
        if (!!employeePK) {
          params += `&employee=${ employeePK }`
        }
        axios({
          url: `${ apiURL }api/v1/expense-month${ params }`
        })
          .then(resp => {
            const ems: ExpenseMonth[] = resp.data.results
            this.directorExpenseMonths = ems
            this.numExpensesDirectorToApprove = ems.filter(
              em => {
                // Count if director approval required and not approved yet
                return em.card.requires_director_approval &&
                  em.status == 'approver_approved' &&
                  !em.director_approved_at
              }
            ).length
            resolve(resp.data.results)
          })
          .catch(e => {
            handlePromiseError(
              reject, 'Error getting division director expense months', e
            )
          })
      })
    },

    directorApproveExpenseMonth(
      pk: number, approve: boolean, deny_note?: string
    ): Promise<ExpenseMonth> {
      return new Promise((resolve, reject) => {
        axios({
          url: `${ apiURL }api/v1/expense-month/${ pk }/director_approve`,
          method: 'PUT',
          data: { approve, deny_note }
        })
          .then(resp => {
            resolve(resp.data)
          })
          .catch(e => {
            handlePromiseError(
              reject, 'Error director approving expense month', e
            )
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
          url: `${ apiURL }api/v1/expense-month${ params }`
        })
          .then(resp => {
            const ems: ExpenseMonth[] = resp.data.results
            this.fiscalExpenseMonths = ems
            this.numExpensesFiscalToApprove = ems.filter(
              em => {
                if (em.card.requires_director_approval) {
                  // If director approval required, count if approved
                  return em.director_approved &&
                    !['fiscal_approved', 'fiscal_denied'].includes(em.status)
                } else {
                  // Otherwise, count if approver approved
                  return em.status == 'approver_approved'
                }
              }
            ).length
            resolve(resp.data.results)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error getting fiscal expense months', e)
          })
      })
    },

    approveExpenseMonth(
      pk: number, approve: boolean, deny_note?: string
    ): Promise<ExpenseMonth> {
      return new Promise((resolve, reject) => {
        axios({
          url: `${ apiURL }api/v1/expense-month/${ pk }/fiscal_approve`,
          method: 'PUT',
          data: { approve, deny_note }
        })
          .then(resp => {
            resolve(resp.data)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error approving expense month', e)
          })
      })
    },

    uploadExpenseStatement(
      yearInt: number, monthInt: number, file: File
    ): Promise<null> {
      return new Promise((resolve, reject) => {
        const formData = new FormData()
        formData.append('year', yearInt.toString())
        formData.append('month', monthInt.toString())
        formData.append('statement', file)
        axios({
          url: `${ apiURL }api/v1/expense-statement`,
          method: 'POST',
          data: formData,
          headers: { 'Content-Type': 'multipart/form-data' }
        })
          .then(() => {
            resolve(null)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error uploading expense statements', e)
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

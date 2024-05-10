import axios from 'axios'
import { defineStore } from 'pinia'

import { apiURL, handlePromiseError } from 'src/stores/index'
import { Expense, ExpenseCreate } from 'src/types'

export const usePurchaseStore = defineStore('purchase', {
  state: () => ({
    myExpenses: [] as Array<Expense>,
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
    getMyExpenses(
      yearInt: number | null = null, monthInt: number | null = null
    ): Promise<Array<Expense>> {
      return new Promise((resolve, reject) => {
        let dateParam = ''
        if (yearInt && monthInt) {
          const firstDay =
            new Date(yearInt, monthInt, 1).toISOString().split('T')[0]
          const lastDay =
            new Date(yearInt, monthInt + 1, 0).toISOString().split('T')[0]
          dateParam = `?start=${ firstDay }&end=${ lastDay }`
        }
        axios({ url: `${ apiURL }api/v1/expense${ dateParam }` })
          .then(resp => {
            this.myExpenses = resp.data.results
            resolve(resp.data.results)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error getting all expenses', e)
          })
      })
    },
    submitExpenseMonth(yearInt: number, monthInt: number): Promise<null> {
      return new Promise((resolve, reject) => {
        axios({
          url: `${ apiURL }api/v1/expense/submit/${ yearInt }/${ monthInt }`, method: 'POST'
        })
          .then(() => {
            resolve(null)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error submitting expense month', e)
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

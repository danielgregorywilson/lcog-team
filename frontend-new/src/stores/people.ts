import axios from 'axios'
import { defineStore } from 'pinia'

import { apiURL, handlePromiseError } from 'src/stores/index'
import { EmployeeRetrieve, EmployeeUpdatePartial, SimpleEmployeeRetrieve, Unit } from 'src/types'

export const usePeopleStore = defineStore('people', {
  state: () => ({
    simpleEmployeeList: [] as Array<SimpleEmployeeRetrieve>,
    simpleEmployeeDetail: { pk: -1, name: '' } as SimpleEmployeeRetrieve,
    unitList: [] as Array<Unit>
  }),

  getters: {},

  actions: {
    getSimpleEmployeeList() {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/employee/simple_list`})
          .then(resp => {
            this.simpleEmployeeList = resp.data
            resolve('Successfully got simple employee list')
          })
          .catch(e => {
            handlePromiseError(reject, 'Error getting simple employee list', e)
          })
      })
    },
    getSimpleEmployeeDetail(data: {pk: string}) {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/employee/${ data.pk }/simple_detail`})
          .then(resp => {
            this.simpleEmployeeDetail = resp.data
            resolve('Successfully got simple employee detail')
          })
          .catch(e => {
            handlePromiseError(reject, 'Error getting simple employee detail', e)
          })
      })
    },
    updatePartialEmployee(pk: string, data: EmployeeUpdatePartial): Promise<EmployeeRetrieve> {
      return new Promise((resolve, reject) => {
        axios({
          url: `${ apiURL }api/v1/employee/${ pk }`,
          method: 'PATCH',
          data: data
        })
        .then(resp => {
          resolve(resp.data)
        })
        .catch(e => {
          handlePromiseError(reject, 'Error updating employee', e)
        })
      })
    },
    getUnitList() {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/unit`})
        .then(resp => {
          this.unitList = resp.data.results
          resolve('Successfully got unit list')
        })
        .catch(e => {
          handlePromiseError(reject, 'Error getting unit list', e)
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

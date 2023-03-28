import axios from 'axios';
import { defineStore } from 'pinia';
import { PeopleStateInterface } from 'src/types';

import { handlePromiseError } from './index'

const apiURL = process.env.API_URL ?
  process.env.API_URL : 'https://api.team.lcog.org/'

export const usePeopleStore = defineStore('people', {
  state: (): PeopleStateInterface => ({
    simpleEmployeeList: [],
    simpleEmployeeDetail: { pk: -1, name: '' },
    unitList: [],
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
            console.error('Error getting simple employee list:', e)
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
    getUnitList() {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/unit`})
        .then(resp => {
          this.unitList = resp.data
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
});

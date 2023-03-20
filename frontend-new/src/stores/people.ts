import axios from 'axios';
import { defineStore } from 'pinia';
import { PeopleStateInterface } from 'src/types';

const apiURL = process.env.API_URL ?
  process.env.API_URL : 'https://api.team.lcog.org/'

export const usePeopleStore = defineStore('people', {
  state: (): PeopleStateInterface => ({
    simpleEmployeeList: [],
    simpleEmployeeDetail: { pk: -1, name: '' },
    unitList: [],
  }),

  getters: { },

  actions: {
    getSimpleEmployeeList() {
      axios({ url: `${ apiURL }api/v1/employee/simple_list`})
        .then(resp => {
          this.simpleEmployeeList = resp.data
        })
        .catch(e => {
          console.error('Error getting simple employee list:', e)
        })
    },
    getSimpleEmployeeDetail(data: {pk: number}) {
      axios({ url: `${ apiURL }api/v1/employee/${ data.pk }/simple_detail`})
        .then(resp => {
          this.simpleEmployeeDetail = resp.data
        })
        .catch(e => {
          console.error('Error getting simple employee detail:', e)
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
          console.error('Error getting unit list:', e)
          reject('Error getting unit list')
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

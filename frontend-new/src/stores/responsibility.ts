import axios from 'axios'
import { defineStore } from 'pinia'

import {
  EmployeeResponsibilitiesInterface, Responsibility, ResponsibilityCreate,
  ResponsibilityNameUpdate, ResponsibilityStateInterface,
  ResponsibilityTagCreate, ResponsibilityTagUpdate, ResponsibilityUpdate
} from 'src/types'

import { handlePromiseError } from './index'

const apiURL = process.env.API_URL ?
  process.env.API_URL : 'https://api.team.lcog.org/'

export const useResponsibilityStore = defineStore('responsibility', {
  state: (): ResponsibilityStateInterface => ({
    allResponsibilities: [],
    orphanedResponsibilities: [],
    employeePrimaryResponsibilities: [],
    employeeSecondaryResponsibilities: [],
    tagWithResponsibilities: [],
    allTags: { results: [] },
    // simpleEmployeeList: [],
    // simpleEmployeeDetail: { pk: -1, name: '' },
    simpleTagList: []
  }),

  getters: {},

  actions: {
    createResponsibility(data: ResponsibilityCreate) {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/responsibilities`, data, method: 'POST' })
          .then(resp => {
            resolve(resp)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error creating responsibility', e)
          })
      })
    },
    getAllResponsibilities() {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/responsibilities` })
          .then((resp: {data: {results: Array<Responsibility>}}) => {
            this.allResponsibilities = resp.data.results
            resolve(resp)
          })
          .catch(e => {
            console.error('Error getting all responsibilities:', e)
            reject(e)
          })
      })
    },
    getOrphanedResponsibilities() {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/responsibilities?orphaned=true` })
          .then((resp: {data: {results: Array<Responsibility>}}) => {
            this.orphanedResponsibilities = resp.data.results
            resolve(resp)
          })
          .catch(e => {
            console.error('Error getting orphaned responsibilities:', e)
            reject(e)
          })
      })
    },
    getEmployeePrimaryResponsibilities(data: {pk: string}) {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/responsibilities?employee=${ data.pk }` })
          .then(resp => {
            const responsibilities: Array<Responsibility> = resp.data.results
            const employeeResponsibilities = this.employeePrimaryResponsibilities
            const thisEmployeeResponsibilities = employeeResponsibilities.filter(employeeObj => employeeObj.pk == data.pk)[0]
            if (thisEmployeeResponsibilities) {
              thisEmployeeResponsibilities.responsibilities = responsibilities
            } else {
              const employeeResponsibilitiesObj: EmployeeResponsibilitiesInterface = {pk: data.pk, responsibilities}
              employeeResponsibilities.push(employeeResponsibilitiesObj)
            }
            this.employeePrimaryResponsibilities = employeeResponsibilities
            resolve(resp)
          })
          .catch(e => {
            console.error('Error getting employee primary responsibilities:', e)
            reject(e)
          })
      })
    },
    getEmployeeSecondaryResponsibilities(data: {pk: string}) {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/responsibilities?employee=${ data.pk }&secondary=true` })
          .then(resp => {
            const responsibilities: Array<Responsibility> = resp.data.results
            const employeeResponsibilities = this.employeeSecondaryResponsibilities
            const thisEmployeeResponsibilities = employeeResponsibilities.filter(employeeObj => employeeObj.pk == data.pk)[0]
            if (thisEmployeeResponsibilities) {
              thisEmployeeResponsibilities.responsibilities = responsibilities
            } else {
              const employeeResponsibilitiesObj: EmployeeResponsibilitiesInterface = {pk: data.pk, responsibilities}
              employeeResponsibilities.push(employeeResponsibilitiesObj)
            }
            this.employeeSecondaryResponsibilities = employeeResponsibilities
            resolve(resp)
          })
          .catch(e => {
            console.error('Error getting employee secondary responsibilities:', e)
            reject(e)
          })
      })
    },
    updateResponsibility(pk: string, data: ResponsibilityUpdate) {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/responsibilities/${pk}`, data, method: 'PUT' })
          .then(resp => {
            resolve(resp)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error updating responsibility', e)
          })
      })
    },
    updateResponsibilityName(data: ResponsibilityNameUpdate) {
      this.allResponsibilities.results.filter(r => r.pk == data.pk)[0].name = data.name
    },
    deleteResponsibility(pk: string) {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/responsibilities/${pk}`, method: 'DELETE' })
          .then(resp => {
            resolve(resp)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error deleting responsibility', e)
          })
      })
    },
    
    //////////
    // Tags //
    //////////

    createTag(pk: string, data: ResponsibilityTagCreate) {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/responsibilitytags`, data, method: 'POST' })
          .then(resp => {
            resolve(resp)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error creating tag', e)
          })
      })
    },
    getAllTags() {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/responsibilitytags` })
          .then(resp => {
            this.allTags = resp.data
            resolve(resp)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error getting all tags', e)
          })
      })
    },
    getTagWithResponsibilities(pk: string) {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/responsibilitytags/${ pk }` })
          .then(resp => {
            this.tagWithResponsibilities = resp.data
            resolve(resp)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error getting tag responsibilities', e)
          })
      })
    },
    getSimpleTagList() {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/responsibilitytags/simple_list`})
          .then(resp => {
            this.simpleTagList = resp.data
            resolve('Successfully got simple tag list')
          })
          .catch(e => {
            console.error('Error getting simple tag list:', e)
            reject(`Error getting simple tag list: ${ e }`)
          })
      })
    },
    updateTag(pk: string, data: ResponsibilityTagUpdate) {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/responsibilitytags/${pk}`, data, method: 'PUT' })
          .then(resp => {
            resolve(resp)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error updating tag', e)
          })
      })
    },
    deleteTag(pk: string) {
      return new Promise((resolve, reject) => {
        axios({ url: `${ apiURL }api/v1/responsibilitytags/${pk}`, method: 'DELETE' })
          .then(resp => {
            resolve(resp)
          })
          .catch(e => {
            handlePromiseError(reject, 'Error deleting tag', e)
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

<!-- Not converted from Quasar 1/Vue 2 -->
<template>
  <q-page class="q-pa-md">
    <div class="text-h4">Mileage Reimbursement</div>
    <div class="q-my-md row justify-between">
      <div class="q-gutter-sm">
        <q-btn :to="{ name: 'mileage-reimbursement-create' }" unelevated rounded color="primary" icon="directions_car" label="Request Reimbursement" />
        <q-btn :to="{ name: 'mileage-reimbursement-list' }" unelevated rounded color="primary" icon="list" label="View Requests" />
        <!-- <q-btn :to="{ name: 'orphaned-responsibilities' }" unelevated rounded color="primary" icon="visibility_off" label="View Orphaned" /> -->
      </div>
    </div>
    <router-view :key="$route.path" />
  </q-page>
</template>

<style scoped lang="scss">
</style>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { Notify } from 'quasar'
import { bus } from '../../App.vue'
import { Responsibility, SimpleEmployeeRetrieve, VuexStoreGetters } from '../../store/types'
import ResponsibilityDataService from '../../services/ResponsibilityDataService'

@Component
export default class Responsibilities extends Vue {
  private addDialogVisible = false
  private addFormName = ''
  private emptyEmployee = {name: '', pk: -1}
  private addFormPrimaryEmployee = this.emptyEmployee
  private addFormSecondaryEmployee = this.emptyEmployee

  private editDialogVisible = false
  private pkToEdit = -1
  private editFormName = ''
  private editFormPrimaryEmployee = this.emptyEmployee
  private editFormSecondaryEmployee = this.emptyEmployee
  
  private deleteDialogVisible = false
  private deleteDialogResponsibilityName = ''
  private rowPkToDelete = ''

  private getters = this.$store.getters as VuexStoreGetters

  private needle = '' // For filtering employee list

  ///////////////
  // EMPLOYEES //
  ///////////////
  private employees(): Array<SimpleEmployeeRetrieve> {    
    const employees = this.getters['responsibilityModule/simpleEmployeeList']
    return employees.filter((employee) => {
      return employee.name.toLowerCase().indexOf(this.needle) != -1
    })
  }

  private retrieveSimpleEmployeeList(): void {
    this.$store.dispatch('responsibilityModule/getSimpleEmployeeList')
      .catch(e => {
        console.error('Error retrieving simple employee list', e)
      })
  }

  private filterFn (val: string, update: Function) { // eslint-disable-line @typescript-eslint/ban-types
    update(() => {
      this.needle = val.toLowerCase()
    })
  }

  //////////////
  // ADD FORM //
  //////////////
  private clearAddForm() {
    this.addFormName = ''
    this.addFormPrimaryEmployee = this.emptyEmployee
    this.addFormSecondaryEmployee = this.emptyEmployee
  }

  private onAddFormSubmit () {
    this.createResponsibility()
      .then(() => {
        this.updateResponsibiliyLists()
        this.addDialogVisible = false
        Notify.create('Created responsibility')
        this.clearAddForm()
      })
      .catch(e => {
        console.error('Error creating Responsibility:', e)
      })
   }

  private createResponsibility() {
    return new Promise((resolve, reject) => {
      ResponsibilityDataService.create({
        name: this.addFormName,
        primary_employee: this.addFormPrimaryEmployee.pk,
        secondary_employee: this.addFormSecondaryEmployee.pk
      })
        .then(() => {
          resolve('Created')
        })
        .catch(e => {
          console.error('Error creating Responsibility:', e)
          reject(e)
        })
    })
  }

  ///////////////
  // EDIT FORM //
  ///////////////

  private openEditDialog(row: Responsibility) {
    this.pkToEdit = row.pk
    this.editFormName = row.name
    if (row.primary_employee_pk && row.primary_employee_name) {
      this.editFormPrimaryEmployee = { pk: row.primary_employee_pk, name: row.primary_employee_name}
    }
    if (row.secondary_employee_pk && row.secondary_employee_name) {
      this.editFormSecondaryEmployee = { pk: row.secondary_employee_pk, name: row.secondary_employee_name}
    }
    this.editDialogVisible = true
  }

  private clearEditForm() {
    this.pkToEdit = -1
    this.editFormName = ''
    this.editFormPrimaryEmployee = this.emptyEmployee
    this.editFormSecondaryEmployee = this.emptyEmployee
  }

  private onEditFormSubmit () {
    this.editResponsibility()
      .then(() => {
        this.updateResponsibiliyLists()
        this.editDialogVisible = false
        Notify.create('Updated responsibility')
        this.clearEditForm()
      })
      .catch(e => {
        console.error('Error updating Responsibility:', e)
      })
  }

  private editResponsibility() {
    return new Promise((resolve, reject) => {
      ResponsibilityDataService.update(this.pkToEdit.toString(), {
        name: this.editFormName,
        primary_employee: this.editFormPrimaryEmployee.pk,
        secondary_employee: this.editFormSecondaryEmployee.pk
      })
        .then(() => {
          resolve('Updated')
        })
        .catch(e => {
          console.error('Error updating Responsibility:', e)
          reject(e)
        })
    })
  }

  /////////////////
  // DELETE FORM //
  /////////////////

  private openDeleteDialog(row: Responsibility) {
    this.rowPkToDelete = row.pk.toString()
    this.deleteDialogResponsibilityName = row.name
    this.deleteDialogVisible = true;
  }

  private deleteRow(): void {
    ResponsibilityDataService.delete(this.rowPkToDelete)
      .then(() => {
        this.updateResponsibiliyLists()
        Notify.create('Deleted a responsibility.')
      })
      .catch(e => {
        console.error('Error deleting responsibility', e)
      })
  }

  ///////////////
  // SET STATE //
  ///////////////

  // Update the various responsibility lists in Vuex
  private updateResponsibiliyLists(): void {
    this.retrieveAllResponsibilites()
    this.retrieveOrphanedResponsibilites()
    const pk = this.$route.params.pk
    if (pk) {
      this.retrieveEmployeeResponsibilites(pk)
      this.retrieveEmployeeSecondaryResponsibilites(pk)
    }
  }

  // Update All Responsibilities Table
  private retrieveAllResponsibilites(): void {
    this.$store.dispatch('responsibilityModule/getAllResponsibilities')
      .catch(e => {
        console.error('Error retrieving responsibilities', e)
      })
  }

  // Update Orphaned Responsibilities Table
  private retrieveOrphanedResponsibilites(): void {
    this.$store.dispatch('responsibilityModule/getOrphanedResponsibilities')
      .catch(e => {
        console.error('Error retrieving orphaned responsibilities', e)
      })
  }

  // Update Employee Responsibilities Table
  private retrieveEmployeeResponsibilites(employeePk: string | (string | null)[]): void {
    this.$store.dispatch('responsibilityModule/getEmployeePrimaryResponsibilities', {pk: employeePk})
      .catch(e => {
        console.error('Error retrieving employee responsibilities', e)
      })
  }

  // Update Employee Secondary Responsibilities Table
  private retrieveEmployeeSecondaryResponsibilites(employeePk: string | (string | null)[]): void {
    this.$store.dispatch('responsibilityModule/getEmployeeSecondaryResponsibilities', {pk: employeePk})
      .catch(e => {
        console.error('Error retrieving employee secondary responsibilities', e)
      })
  }

  created() {
    // We trigger opening the edit and delete dialogs in AllResponsibilities, EmployeeResponsibilites, or OrphanedResponsibilities
    bus.$on('emitOpenEditDialog', (row: Responsibility) => { // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-call
      this.openEditDialog(row)
    })
    bus.$on('emitOpenDeleteDialog', (row: Responsibility) => { // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-call
      this.openDeleteDialog(row)
    })
  }

  mounted() {
    if (!this.employees().length) {
      this.retrieveSimpleEmployeeList()
    }
    
  }
}
</script>

<template>
  <q-page class="q-pa-md">
    <div class="q-mb-md row justify-between">
      <div class="q-gutter-sm">
        <q-btn :to="{ name: 'all-responsibilities' }" unelevated rounded color="primary" icon="visibility" label="View All" />
        <q-btn :to="{ name: 'orphaned-responsibilities' }" unelevated rounded color="primary" icon="visibility_off" label="View Orphaned" />
      </div>
      <div>
        <q-btn unelevated rounded color="primary" icon="add" label="Add" @click="addDialogVisible=true" />
      </div>
    </div>
    <router-view :key="$route.path" />

    <!-- ADD RESPONSIBILITY DIALOG -->
    <q-dialog v-model="addDialogVisible">
      <q-card>
        <q-card-section>
          <q-form
            @submit="onAddFormSubmit"
            @reset="clearAddForm"
            class="q-gutter-sm"
          >
            <div class="text-h5">Add a Responsibility</div>
            <q-input
              filled
              v-model="addFormName"
              label="Name"
            />
            <!-- <q-select v-model="addFormPrimaryEmployee" :options="employeeOptions" option-value="pk" option-label="name" label="Primary Employee" use-input hide-selected fill-input input-debounce="0" @filter="filterFn"> -->
            <q-select v-model="addFormPrimaryEmployee" :options="employees()" option-value="pk" option-label="name" label="Primary Employee" use-input hide-selected fill-input input-debounce="0">
              <template v-slot:no-option>
                <q-item>
                  <q-item-section class="text-grey">
                    No results
                  </q-item-section>
                </q-item>
              </template>
              <template v-if="addFormPrimaryEmployee.name" v-slot:append>
                <q-icon name="cancel" @click.stop="addFormPrimaryEmployee = emptyEmployee" class="cursor-pointer" />
              </template>
            </q-select>
            <q-select v-model="addFormSecondaryEmployee" :options="employees()" option-value="pk" option-label="name" label="Secondary Employee"  use-input hide-selected fill-input input-debounce="0">
              <template v-slot:no-option>
                <q-item>
                  <q-item-section class="text-grey">
                    No results
                  </q-item-section>
                </q-item>
              </template>
              <template v-if="addFormSecondaryEmployee.name" v-slot:append>
                <q-icon name="cancel" @click.stop="addFormSecondaryEmployee = emptyEmployee" class="cursor-pointer" />
              </template>
            </q-select>
            <div>
              <q-btn label="Submit" type="submit" color="primary" :disable="!addFormName"/>
              <q-btn label="Reset" type="reset" color="primary" flat class="q-ml-sm" />
            </div>
          </q-form>
        </q-card-section>
      </q-card>
    </q-dialog>

    <!-- EDIT RESPONSIBILITY DIALOG -->
    <q-dialog v-model="editDialogVisible">
      <q-card>
        <q-card-section>
          <q-form
            @submit="onEditFormSubmit"
            class="q-gutter-sm"
          >
            <div class="text-h5">Edit Responsibility</div>
            <q-input
              filled
              v-model="editFormName"
              label="Name"
            />
            <!-- <q-select v-model="formPrimaryEmployee" :options="employeeOptions" option-value="pk" option-label="name" label="Primary Employee" use-input hide-selected fill-input input-debounce="0" @filter="filterFn"> -->
            <q-select v-model="editFormPrimaryEmployee" :options="employees()" option-value="pk" option-label="name" label="Primary Employee" use-input hide-selected fill-input input-debounce="0">
              <template v-slot:no-option>
                <q-item>
                  <q-item-section class="text-grey">
                    No results
                  </q-item-section>
                </q-item>
              </template>
              <template v-if="editFormPrimaryEmployee.name" v-slot:append>
                <q-icon name="cancel" @click.stop="editFormPrimaryEmployee = emptyEmployee" class="cursor-pointer" />
              </template>
            </q-select>
            <q-select v-model="editFormSecondaryEmployee" :options="employees()" option-value="pk" option-label="name" label="Secondary Employee"  use-input hide-selected fill-input input-debounce="0">
              <template v-slot:no-option>
                <q-item>
                  <q-item-section class="text-grey">
                    No results
                  </q-item-section>
                </q-item>
              </template>
              <template v-if="editFormSecondaryEmployee.name" v-slot:append>
                <q-icon name="cancel" @click.stop="editFormSecondaryEmployee = emptyEmployee" class="cursor-pointer" />
              </template>
            </q-select>
            <div>
              <q-btn label="Submit" type="submit" color="primary" :disable="!editFormName"/>
            </div>
          </q-form>
        </q-card-section>
      </q-card>
    </q-dialog>

    <!-- DELETE RESPONSIBILITY DIALOG -->
    <q-dialog v-model="deleteDialogVisible">
      <q-card>
        <q-card-section>
          <div class="row items-center">
            <q-avatar icon="list" color="primary" text-color="white" />
            <span class="q-ml-sm">Are you sure you want to delete this responsibility?</span>
          </div>
          <div class="row justify-center text-center">{{ deleteDialogResponsibilityName }}</div>
        </q-card-section>

        <q-card-actions class="row justify-around">
          <q-btn flat label="Cancel" color="primary" v-close-popup />
          <q-btn flat label="Yes, delete it" color="primary" @click="deleteRow()" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
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

  // private employeeOptions() {
  //   return {...this.employees()}
  // }

  // private employeeOptions = Object.assign([], this.employees())

  ///////////////
  // EMPLOYEES //
  ///////////////
  private employees(): Array<SimpleEmployeeRetrieve> {    
    // TODO: Type to filter; for now just use IS employees
    const employees = this.getters['responsibilityModule/simpleEmployeeList']
    const isEmployees = ['Andrew Smith', 'Daniel Hogue', 'Daniel Wilson', 'Heidi Leyba', 'Jacob Callister', 'Jeannine Bienn', 'Jon Hausmann', 'Kathleen Moore', 'Keith Testerman', 'Kelly Griffin', 'Robert Hamburg', 'Shugo Nakagome']
    return employees.filter((employee) => isEmployees.indexOf(employee.name) != -1)
  }

  private retrieveSimpleEmployeeList(): void {
    this.$store.dispatch('responsibilityModule/getSimpleEmployeeList')
      .catch(e => {
        console.error('Error retrieving simple employee list', e)
      })
  }

  // private filterFn (val, update, abort) {
  //   update(() => {
  //     const needle = val.toLowerCase()
  //     this.employeeOptions = this.employeeOptions.filter(v => v.toLowerCase().indexOf(needle) > -1)
  //   })
  // }

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
        // this.retrieveAllResponsibilites() TODO update tables when create a new one
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

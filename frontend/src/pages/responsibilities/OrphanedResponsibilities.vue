<template>
  <div>
    <!-- PLACEHOLDER -->
    <!-- PLACEHOLDER -->
    <!-- PLACEHOLDER -->
    <!-- PLACEHOLDER -->
    <!-- PLACEHOLDER -->
    <!-------------------------->
    <!-- ALL RESPONSIBILITIES -->
    <!-------------------------->
    <q-table
      v-if="displayAllResponsibilitiesTable"
      title="All Responsibilities"
      :data="allResponsibilities()"
      :columns="allEmployeesTableColumns"
      row-key="pk"
    >
      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td key="name" :props="props" class="cursor-pointer">
            {{ props.row.name }}
            <q-popup-edit :value="props.row.name" persistent>
              <template v-slot="{ initialValue, value, emitValue, validate, set, cancel }">
                <q-input :value="props.row.name" dense autofocus @input="updateName(props.row.pk, $event)" />
                <div class="row justify-center q-mt-sm">
                  <q-btn flat class="text-primary" @click.stop="cancelUpdateName(props.row.pk, initialValue, cancel)">Cancel</q-btn>
                  <q-btn flat class="text-primary" @click.stop="updateResponsibility(props.row, cancel)" :disable="value === '' || initialValue === value">Set</q-btn>
                </div>
              </template>
            </q-popup-edit>
          </q-td>
          <q-td key="primary_employee_name" :props="props">
            <router-link v-if="props.row.primary_employee_pk" :to="{ name: 'employee-responsibilities', params: { pk: props.row.primary_employee_pk} }">
              {{ props.row.primary_employee_name }}
            </router-link>
            <!-- <q-popup-edit v-model="props.row.primary_employee_name" buttons>
              <q-input v-model="props.row.primary_employee_name" dense autofocus />
            </q-popup-edit> -->
          </q-td>
          <q-td key="secondary_employee_name" :props="props">
            <router-link v-if="props.row.secondary_employee_pk" :to="{ name: 'employee-responsibilities', params: { pk: props.row.secondary_employee_pk} }">
              {{ props.row.secondary_employee_name }}
            </router-link>
            <!-- <q-popup-edit v-model="props.row.secondary_employee_name" buttons>
              <q-input v-model="props.row.secondary_employee_name" dense autofocus />
            </q-popup-edit> -->
          </q-td>
          <q-td key="actions" :props="props">
            <q-btn class="col delete-button" dense round flat color="grey" @click="showDeleteDialog(props)" icon="delete"></q-btn>
          </q-td>
        </q-tr>
      </template>
    </q-table>
    
    <!------------------------------->
    <!-- EMPLOYEE RESPONSIBILITIES -->
    <!------------------------------->
    <q-table
      v-if="displayEmployeeResponsibilitiesTable()"
      title="Responsibilities for {EMPLOYEE}"
      :data="employeePrimaryResponsibilities()"
      :columns="primaryEmployeeTableColumns"
      row-key="pk"
    >
      <!-- <template v-slot:body="props">
        <q-tr :props="props">
          <q-td key="name" :props="props" class="cursor-pointer">
            {{ props.row.name }}
            <q-popup-edit :value="props.row.name" persistent>
              <template v-slot="{ initialValue, value, emitValue, validate, set, cancel }">
                <q-input :value="props.row.name" dense autofocus @input="updateName(props.row.pk, $event)" />
                <div class="row justify-center q-mt-sm">
                  <q-btn flat class="text-primary" @click.stop="cancelUpdateName(props.row.pk, initialValue, cancel)">Cancel</q-btn>
                  <q-btn flat class="text-primary" @click.stop="updateResponsibility(props.row, cancel)" :disable="value === '' || initialValue === value">Set</q-btn>
                </div>
              </template>
            </q-popup-edit>
          </q-td>
          <q-td key="primary_employee_name" :props="props">
            {{ props.row.primary_employee_name }}
          </q-td>
          <q-td key="secondary_employee_name" :props="props">
            {{ props.row.secondary_employee_name }}
          </q-td>
          <q-td key="actions" :props="props">
            <q-btn class="col delete-button" dense round flat color="grey" @click="showDeleteDialog(props)" icon="delete"></q-btn>
          </q-td>
        </q-tr>
      </template> -->
    </q-table>
    
    <!------------------------------->
    <!-- ORPHANED RESPONSIBILITIES -->
    <!------------------------------->
    <q-table
      v-if="displayOrphanedResponsibilitiesTable"
      title="Orphaned Responsibilities"
      :data="orphanedResponsibilities()"
      :columns="allEmployeesTableColumns"
      row-key="pk"
    />

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
  </div>
</template>

<style scoped lang="scss">
  // #page-container {
  //   max-width: 300px;
  //   display: none;
  // }
</style>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { EmployeeResponsibilitiesInterface, Responsibility, SimpleEmployeeRetrieve, VuexStoreGetters } from '../../store/types'
import { Notify } from 'quasar'
import ResponsibilityDataService from '../../services/ResponsibilityDataService'

interface QuasarResponsibilityTableRowClickActionProps {
  evt: MouseEvent;
  row: Responsibility;
}

@Component
export default class OrphanedResponsibilities extends Vue {
  private orphaned = this.$route.query.orphaned
  private pk = this.$route.params.pk
  private secondary = this.$route.query.secondary

  private displayAllResponsibilitiesTable = false
  private displayOrphanedResponsibilitiesTable = false
  // private displayEmployeeResponsibilitiesTable = this.pk && this.isNormalInteger(this.pk) && !(this.secondary && this.secondary == 'true')
  private displayEmployeeSecondaryResponsibilitiesTable = false

  private displayEmployeeResponsibilitiesTable() {
    this.pk && this.isNormalInteger(this.pk) && !(this.secondary && this.secondary == 'true')
  }

  private deleteDialogVisible = false
  private deleteDialogResponsibilityName = ''
  private rowPkToDelete = ''

  private formName = ''
  private emptyEmployee = {name: '', pk: -1}
  private formPrimaryEmployee = this.emptyEmployee
  private formSecondaryEmployee = this.emptyEmployee

  // private getters = this.$store.getters
  private getters = this.$store.getters as VuexStoreGetters

  // private employeeOptions() {
  //   return {...this.employees()}
  // }

  // private employeeOptions = Object.assign([], this.employees())

  private employees(): Array<SimpleEmployeeRetrieve> {    
    return this.getters['responsibilityModule/simpleEmployeeList']
  }

  private allResponsibilities(): Array<Responsibility> {
    return this.getters['responsibilityModule/allResponsibilities'].results
  }

  private orphanedResponsibilities(): Array<Responsibility> {
    return this.getters['responsibilityModule/orphanedResponsibilities'].results
  }

  private employeePrimaryResponsibilities(): Array<EmployeeResponsibilitiesInterface> {
    return this.getters['responsibilityModule/employeePrimaryResponsibilities']
  }

  private employeeSecondaryResponsibilities(): Array<EmployeeResponsibilitiesInterface> {
    return this.getters['responsibilityModule/employeeSecondaryResponsibilities']
  }
  
  private allEmployeesTableColumns = [
    { name: 'name', required: true, label: 'Name', field: 'name', sortable: true, align: 'left' },
    { name: 'primary_employee_name', label: 'Primary Employee', field: 'primary_employee_name', sortable: true },
    { name: 'secondary_employee_name', label: 'Secondary Employee', field: 'secondary_employee_name', sortable: true },
    { name: 'actions', label: 'Actions', },
  ]

  private primaryEmployeeTableColumns = [
    { name: 'name', required: true, label: 'Name', field: 'name', sortable: true, align: 'left' },
  ]

  private updateName(pk: number, name: string) {
    this.$store.commit('responsibilityModule/updateResponsibilityName', {pk, name})
  }

  private cancelUpdateName(pk: number, name: string, closePopupMethod: () => any) { // eslint-disable-line @typescript-eslint/no-explicit-any
    this.$store.commit('responsibilityModule/updateResponsibilityName', {pk, name})
    closePopupMethod()
  }

  private createResponsibility() {
    return new Promise((resolve, reject) => {
      ResponsibilityDataService.create({
        name: this.formName,
        primary_employee: this.formPrimaryEmployee.pk,
        secondary_employee: this.formSecondaryEmployee.pk
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

  private updateResponsibility(responsibility: Responsibility, closePopupMethod: () => any) { // eslint-disable-line @typescript-eslint/no-explicit-any
    return new Promise((resolve, reject) => {
      ResponsibilityDataService.update(responsibility.pk.toString(), {
        name: responsibility.name
        // TODO: employees
      })
      .then(() => {
        closePopupMethod()
        Notify.create('Updated responsibility')
        resolve('Updated')
      })
      .catch(e => {
        console.error('Error updating Responsibility:', e)
        reject(e)
      })
    })
  }

  private retrieveSimpleEmployeeList(): void {
    this.$store.dispatch('responsibilityModule/getSimpleEmployeeList')
      .catch(e => {
        console.error('Error retrieving simple employee list', e)
      })
  }

  private retrieveAllResponsibilites(): void {
    this.$store.dispatch('responsibilityModule/getAllResponsibilities')
      .catch(e => {
        console.error('Error retrieving responsibilities', e)
      })
  }

  private retrieveOrphanedResponsibilites(): void {
    this.$store.dispatch('responsibilityModule/getOrphanedResponsibilities')
      .catch(e => {
        console.error('Error retrieving orphaned responsibilities', e)
      })
  }

  private retrieveEmployeeResponsibilites(employeePk: string | (string | null)[]): void {
    this.$store.dispatch('responsibilityModule/getEmployeePrimaryResponsibilities', {pk: employeePk})
      .catch(e => {
        console.error('Error retrieving employee responsibilities', e)
      })
  }

  private retrieveEmployeeSecondaryResponsibilites(employeePk: string | (string | null)[]): void {
    this.$store.dispatch('responsibilityModule/getEmployeeSecondaryResponsibilities', {pk: employeePk})
      .catch(e => {
        console.error('Error retrieving employee secondary responsibilities', e)
      })
  }
  
  private isNormalInteger(str: string | (string | null)[]) {
    var n = Math.floor(Number(str));
    return n !== Infinity && String(n) === str && n >= 0;
  }

  // private filterFn (val, update, abort) {
  //   update(() => {
  //     const needle = val.toLowerCase()
  //     this.employeeOptions = this.employeeOptions.filter(v => v.toLowerCase().indexOf(needle) > -1)
  //   })
  // }

  private navigateToEmployee(pk: string): void {
    debugger
    window.location.href = pk
    // this.$router.push({
    //   name: 'employee-responsibilities',params: { pk }
    // })
  }

  private showDeleteDialog(props: QuasarResponsibilityTableRowClickActionProps): void {
    this.rowPkToDelete = props.row.pk.toString()
    this.deleteDialogResponsibilityName = props.row.name
    this.deleteDialogVisible = true;
  }

  private deleteRow(): void {
    ResponsibilityDataService.delete(this.rowPkToDelete)
      .then(() => {
        Notify.create('Deleted a responsibility.')
        this.retrieveAllResponsibilites()
      })
      .catch(e => {
        console.error('Error deleting responsibility', e)
      })
  }

  private clearForm() {
    this.formName = ''
    this.formPrimaryEmployee = this.emptyEmployee
    this.formSecondaryEmployee = this.emptyEmployee
  }

  private onFormSubmit () {
    this.createResponsibility()
      .then(() => {
        this.retrieveAllResponsibilites()
        Notify.create('Created responsibility')
        this.clearForm()
      })
      .catch(e => {
        console.error('Error creating Responsibility:', e)
      })
  }

  mounted() {
    this.retrieveSimpleEmployeeList()
    if (this.orphaned && this.orphaned == 'true') {
      this.displayOrphanedResponsibilitiesTable = true
      if (this.orphanedResponsibilities() == null) {
        this.retrieveOrphanedResponsibilites()
      }
    } else if (this.pk && this.isNormalInteger(this.pk)) {
      if (this.secondary && this.secondary == 'true') {
        this.displayEmployeeSecondaryResponsibilitiesTable = true
        if (this.employeeSecondaryResponsibilities() == null) {
          this.retrieveEmployeeSecondaryResponsibilites(this.pk)
        }
      } else {
        // this.displayEmployeeResponsibilitiesTable = true
        if (this.employeePrimaryResponsibilities() == null) {
          this.retrieveEmployeeResponsibilites(this.pk)
        }
      }
    } else {
      this.displayAllResponsibilitiesTable = true
      // TODO: Only fetch if doesn't exist
      this.retrieveAllResponsibilites()
      if (this.allResponsibilities() == []) { // <----- THIS DOESN'T WORK
        this.retrieveAllResponsibilites()
      }
    }
  }
}
</script>

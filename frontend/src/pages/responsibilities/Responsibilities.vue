<template>
  <q-page class="q-pa-md">
    <router-link :to="{ name: 'all-responsibilities' }" >All Responsibilites</router-link>
    <router-view :key="$route.path" />

    <div class="q-mt-lg" style="max-width: 400px">
      <q-form
        @submit="onFormSubmit"
        @reset="clearForm"
        class="q-gutter-sm"
      >
        <div class="text-h5">Add a Responsibility</div>
        <q-input
          filled
          v-model="formName"
          label="Name"
        />
        <!-- <q-select v-model="formPrimaryEmployee" :options="employeeOptions" option-value="pk" option-label="name" label="Primary Employee" use-input hide-selected fill-input input-debounce="0" @filter="filterFn"> -->
        <q-select v-model="formPrimaryEmployee" :options="employees()" option-value="pk" option-label="name" label="Primary Employee" use-input hide-selected fill-input input-debounce="0">
          <template v-slot:no-option>
            <q-item>
              <q-item-section class="text-grey">
                No results
              </q-item-section>
            </q-item>
          </template>
          <template v-if="formPrimaryEmployee.name" v-slot:append>
            <q-icon name="cancel" @click.stop="formPrimaryEmployee = emptyEmployee" class="cursor-pointer" />
          </template>
        </q-select>
        <q-select v-model="formSecondaryEmployee" :options="employees()" option-value="pk" option-label="name" label="Secondary Employee"  use-input hide-selected fill-input input-debounce="0">
          <template v-slot:no-option>
            <q-item>
              <q-item-section class="text-grey">
                No results
              </q-item-section>
            </q-item>
          </template>
          <template v-if="formSecondaryEmployee.name" v-slot:append>
            <q-icon name="cancel" @click.stop="formSecondaryEmployee = emptyEmployee" class="cursor-pointer" />
          </template>
        </q-select>
        <div>
          <q-btn label="Submit" type="submit" color="primary" :disable="!formName"/>
          <q-btn label="Reset" type="reset" color="primary" flat class="q-ml-sm" />
        </div>
      </q-form>
    </div>
  </q-page>
</template>

<style scoped lang="scss">
</style>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { Responsibility, SimpleEmployeeRetrieve, VuexStoreGetters } from '../../store/types'
import { Notify } from 'quasar'
import ResponsibilityDataService from '../../services/ResponsibilityDataService'

interface QuasarResponsibilityTableRowClickActionProps {
  evt: MouseEvent;
  row: Responsibility;
}

@Component
export default class TimeOffRequests extends Vue {
  private formName = ''
  private emptyEmployee = {name: '', pk: -1}
  private formPrimaryEmployee = this.emptyEmployee
  private formSecondaryEmployee = this.emptyEmployee

  private getters = this.$store.getters as VuexStoreGetters

  // private employeeOptions() {
  //   return {...this.employees()}
  // }

  // private employeeOptions = Object.assign([], this.employees())

  private employees(): Array<SimpleEmployeeRetrieve> {    
    // TODO: Type to filter; for now just use IS employees
    const employees = this.getters['responsibilityModule/simpleEmployeeList']
    const ISEmployees = ["Andrew Smith", "Daniel Hogue", "Daniel Wilson", "Heidi Leyba", "Jeannine Bienn", "Jon Hausmann", "Kathleen Moore", "Keith Testerman", "Kelly Griffin", "Robert Hamburg", "Shugo Nakagome"]
    return employees.filter((employee) => ISEmployees.indexOf(employee.name) != -1)
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


  private clearForm() {
    this.formName = ''
    this.formPrimaryEmployee = this.emptyEmployee
    this.formSecondaryEmployee = this.emptyEmployee
  }

  private onFormSubmit () {
    this.createResponsibility()
      .then(() => {
        // this.retrieveAllResponsibilites() TODO update tables when create a new one
        this.retrieveAllResponsibilites()
        const pk = this.$route.params.pk
        if (pk) {
          this.retrieveEmployeeResponsibilites(pk)
          this.retrieveEmployeeSecondaryResponsibilites(pk)
        }
        Notify.create('Created responsibility')
        this.clearForm()
      })
      .catch(e => {
        console.error('Error creating Responsibility:', e)
      })
  }

  // Update All Responsibilities Table
  private retrieveAllResponsibilites(): void {
    this.$store.dispatch('responsibilityModule/getAllResponsibilities')
      .catch(e => {
        console.error('Error retrieving responsibilities', e)
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

  mounted() {
    if (!this.employees().length) {
      this.retrieveSimpleEmployeeList()
    }
    
  }
}
</script>

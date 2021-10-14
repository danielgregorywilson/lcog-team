<template>
  <q-page class="q-pa-md">
    <!-- <div class="text-h4">Responsibilities</div> -->
    <q-table
      v-if="displayAllResponsibilitiesTable"
      title="Responsibilities"
      :data="allResponsibilities()"
      :columns="tableColumns"
      row-key="pk"
    >
      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td key="name" :props="props">
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
            <q-popup-edit v-model="props.row.primary_employee_name" buttons>
              <q-input v-model="props.row.primary_employee_name" dense autofocus />
            </q-popup-edit>
          </q-td>
          <q-td key="secondary_employee_name" :props="props">
            {{ props.row.secondary_employee_name }}
            <q-popup-edit v-model="props.row.secondary_employee_name" buttons>
              <q-input v-model="props.row.secondary_employee_name" dense autofocus />
            </q-popup-edit>
          </q-td>
        </q-tr>
      </template>
    </q-table>
    <q-table
      v-if="displayOrphanedResponsibilitiesTable"
      title="Orphaned Responsibilities"
      :data="orphanedResponsibilities()"
      :columns="tableColumns"
      row-key="pk"
    />

    <div class="q-mt-lg" style="max-width: 400px">
      <q-form
        @submit="onFormSubmit"
        @reset="onFormReset"
        class="q-gutter-sm"
      >
        <div class="text-h5">Add a Responsibility</div>
        <q-input
          filled
          v-model="formName"
          label="Name"
          lazy-rules
          :rules="[ val => val && val.length > 0 || 'Required']"
        />
        <q-select v-model="formPrimaryEmployee" :options="employees()" option-value="pk" option-label="name" label="Primary Employee" use-input hide-selected fill-input input-debounce="0" @filter="filterFn">
          <template v-slot:no-option>
            <q-item>
              <q-item-section class="text-grey">
                No results
              </q-item-section>
            </q-item>
          </template>
          <template v-if="formPrimaryEmployee" v-slot:append>
            <q-icon name="cancel" @click.stop="formPrimaryEmployee = null" class="cursor-pointer" />
          </template>
        </q-select>
        <q-select v-model="formSecondaryEmployee" :options="employees()" option-value="pk" option-label="name" label="Secondary Employee" />
        <div>
          <q-btn label="Submit" type="submit" color="primary" :disable="!formName"/>
          <q-btn label="Reset" type="reset" color="primary" flat class="q-ml-sm" />
        </div>
      </q-form>
    </div>
    <!-- <div>
      <div v-for="responsibility of allResponsibilities()" :key="responsibility.pk">{{ responsibility }}</div>
    </div> -->
  </q-page>
</template>

<style scoped lang="scss">
  // #page-container {
  //   max-width: 300px;
  //   display: none;
  // }
</style>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { AxiosResponsibilityUpdateServerResponse, ResponsibilityRetrieve, SimpleEmployeeRetrieve, VuexStoreGetters } from '../../store/types'
import { Notify } from 'quasar'
import ResponsibilityDataService from '../../services/ResponsibilityDataService'

@Component
export default class TimeOffRequests extends Vue {
  private orphaned = this.$route.query.orphaned
  private pk = this.$route.query.pk
  private secondary = this.$route.query.secondary

  private displayAllResponsibilitiesTable = false
  private displayOrphanedResponsibilitiesTable = false
  private displayEmployeeResponsibilitiesTable = false
  private displayEmployeeSecondaryResponsibilitiesTable = false

  private formName = ''
  private formPrimaryEmployee = ''
  private formSecondaryEmployee = ''

  // private getters = this.$store.getters
  private getters = this.$store.getters as VuexStoreGetters
  
  private employeeOptions() {
    return {...this.employees()}
  }

  private employees(): Array<SimpleEmployeeRetrieve> {    
    return this.getters['responsibilityModule/simpleEmployeeList']
  }

  private allResponsibilities(): Array<ResponsibilityRetrieve> {
    return this.getters['responsibilityModule/allResponsibilities'].results
  }

  private orphanedResponsibilities(): Array<ResponsibilityRetrieve> {
    return this.getters['responsibilityModule/orphanedResponsibilities'].results
  }

  private employeePrimaryResponsibilities(): Array<ResponsibilityRetrieve> {
    return this.getters['responsibilityModule/employeePrimaryResponsibilities'].results
  }

  private employeeSecondaryResponsibilities(): Array<ResponsibilityRetrieve> {
    return this.getters['responsibilityModule/employeeSecondaryResponsibilities'].results
  }
  
  private tableColumns = [
    { name: 'name', required: true, label: 'Name', field: 'name', sortable: true, align: 'left' },
    { name: 'primary_employee_name', label: 'Primary Employee', field: 'primary_employee_name', sortable: true },
    { name: 'secondary_employee_name', label: 'Secondary Employee', field: 'secondary_employee_name', sortable: true },
  ]

  private updateName(pk: number, name: string) {
    this.$store.commit('responsibilityModule/updateResponsibilityName', {pk, name})
  }

  private cancelUpdateName(pk: number, name: string, closePopupMethod: () => any) { // eslint-disable-line @typescript-eslint/no-explicit-any
    this.$store.commit('responsibilityModule/updateResponsibilityName', {pk, name})
    closePopupMethod()
  }

  private updateResponsibility(responsibility: ResponsibilityRetrieve, closePopupMethod: () => any) { // eslint-disable-line @typescript-eslint/no-explicit-any
    return new Promise((resolve, reject) => {
      ResponsibilityDataService.update(responsibility.pk.toString(), {
        name: responsibility.name
        // TODO: employees
      })
      .then((response: AxiosResponsibilityUpdateServerResponse) => {
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

  private filterFn (val, update, abort) {
    update(() => {
      const needle = val.toLowerCase()
      this.employees = stringOptions.filter(v => v.toLowerCase().indexOf(needle) > -1)
    })
  }

  private onFormReset () {
    this.formName = ''
  }

  private onFormSubmit () {
  
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
        this.displayEmployeeResponsibilitiesTable = true
        if (this.employeePrimaryResponsibilities() == null) {
          this.retrieveEmployeeResponsibilites(this.pk)
        }
      }
    } else {
      this.displayAllResponsibilitiesTable = true
      if (this.allResponsibilities() == null) {
        this.retrieveAllResponsibilites()
      }
    }
  }
}
</script>

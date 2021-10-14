<template>
  <q-page class="q-pa-md">
    <div class="text-h4">Responsibilities</div>
    <q-table
      v-if="displayAllResponsibilitiesTable"
      title="Responsibilities"
      :data="allResponsibilities()"
      :columns="tableColumns"
      row-key="pk"
    />
    <q-table
      v-if="displayOrphanedResponsibilitiesTable"
      title="Orphaned Responsibilities"
      :data="orphanedResponsibilities()"
      :columns="tableColumns"
      row-key="pk"
    />
    <div>
      <div v-for="responsibility of allResponsibilities()" :key="responsibility.pk">{{ responsibility }}</div>
    </div>
  </q-page>
</template>

<style scoped lang="scss">
  // #page-container {
  //   max-width: 300px;
  //   display: none;
  // }
</style>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import { ResponsibilityModule, ResponsibilityRetrieve } from '../../store/types'

@Component
export default class TimeOffRequests extends Vue {
  private orphaned = this.$route.query.orphaned
  private pk = this.$route.query.pk
  private secondary = this.$route.query.secondary

  private displayAllResponsibilitiesTable = false
  private displayOrphanedResponsibilitiesTable = false
  private displayEmployeeResponsibilitiesTable = false
  private displayEmployeeSecondaryResponsibilitiesTable = false

  private getters = this.$store.getters
  // private getters = this.$store.getters as ResponsibilityModule
  
  private allResponsibilities(): Array<ResponsibilityRetrieve> {
    return this.getters['responsibilityModule/allResponsibilities'].results as Array<ResponsibilityRetrieve>
  }

  private orphanedResponsibilities(): Array<ResponsibilityRetrieve> {
    return this.getters['responsibilityModule/orphanedResponsibilities'].results as Array<ResponsibilityRetrieve>
  }

  private employeePrimaryResponsibilities(): Array<ResponsibilityRetrieve> {
    return this.getters['responsibilityModule/employeePrimaryResponsibilities'].results as Array<ResponsibilityRetrieve>
  }

  private employeeSecondaryResponsibilities(): Array<ResponsibilityRetrieve> {
    return this.getters['responsibilityModule/employeeSecondaryResponsibilities'].results as Array<ResponsibilityRetrieve>
  }
  
  private tableColumns = [
    {
      name: 'name',
      required: true,
      label: 'Name',
      field: row => row.name,
      format: val => `${val}`,
      sortable: true,
      align: 'left'
    },
    { name: 'primary_employee_name', label: 'Primary Employee', field: 'primary_employee_name', sortable: true },
    { name: 'secondary_employee_name', label: 'Secondary Employee', field: 'secondary_employee_name', sortable: true },
    // { name: 'carbs', label: 'Carbs (g)', field: 'carbs' },
    // { name: 'protein', label: 'Protein (g)', field: 'protein' },
    // { name: 'sodium', label: 'Sodium (mg)', field: 'sodium' },
    // { name: 'calcium', label: 'Calcium (%)', field: 'calcium', sortable: true, sort: (a, b) => parseInt(a, 10) - parseInt(b, 10) },
    // { name: 'iron', label: 'Iron (%)', field: 'iron', sortable: true, sort: (a, b) => parseInt(a, 10) - parseInt(b, 10) }
  ]

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

  mounted() {
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

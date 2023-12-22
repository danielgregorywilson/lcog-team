<!-- Not converted from Quasar 1/Vue 2 -->
<template>
  <div class="q-pt-sm">
    <q-form
      @submit="formSubmit"
      class="q-gutter-md"
    >
      
      <table>
        <thead>
          <tr>
            <td colspan="4"></td>
            <td colspan="2" class="rowspan">Odometer</td>
            <td></td>
          </tr>
          <tr>
            <td><q-checkbox :value="allChecked()" @input="checkAll()" /></td>
            <td>Date</td>
            <td>Purpose/Destination</td>
            <td>Subfund & Contract</td>
            <td>Start</td>
            <td>Finish</td>
            <td>Miles</td>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in rows" :key="rows.indexOf(row)">
            <td><q-checkbox v-model="row.checked" /></td>
            <td>{{ row.date }}</td>
            <td>{{ row.purpose }}</td>
            <td>{{ row.subfund }}</td>
            <td>{{ row.start }}</td>
            <td>{{ row.finish }}</td>
            <td>{{ row.finish - row.start }}</td>
          </tr>
        </tbody>

      </table>

      <div>
        <q-btn label="Approve all checked" type="submit" color="primary"/>
      </div>
    </q-form>

    <!-- {{rows}} -->

  </div>
</template>

<style scoped lang="scss">
table {
   border: 1px solid black;
   border-radius: 10px;

  thead {
    font-weight: bold;
  }

  td {
    padding-left: 5px;
    padding-right: 5px;

  &.rowspan {
    text-align: center;
  }
  }
}
</style>

<script lang="ts">
import { Notify } from 'quasar'
import { Component, Vue } from 'vue-property-decorator'
import { bus } from '../../App.vue'
import { Responsibility, VuexStoreGetters } from '../../store/types'

@Component
export default class AllResponsibilities extends Vue {
  private getters = this.$store.getters as VuexStoreGetters

  // private allChecked = false

  private rows = [
    { 'checked': false, 'date': '2022/02/22', 'purpose': 'Portland', 'subfund': 'Fund A', 'start': '1005', 'finish': '1010' },
    { 'checked': false, 'date': '2022/02/23', 'purpose': 'Salem', 'subfund': 'Fund B', 'start': '42', 'finish': '420' }
  ]

  private allResponsibilities(): Array<Responsibility> {
    return this.getters['responsibilityModule/allResponsibilities'].results
  }
  
  private tableColumns = [
    { name: 'name', required: true, label: 'Name', field: 'name', sortable: true, align: 'left' },
    { name: 'primary_employee_name', label: 'Primary Employee', field: 'primary_employee_name', sortable: true },
    { name: 'secondary_employee_name', label: 'Secondary Employee', field: 'secondary_employee_name', sortable: true },
    { name: 'actions', label: 'Actions', },
  ]

  private initialTablePagination = {
    rowsPerPage: 10
  }

  private allChecked(): boolean {
    let falseRows = this.rows.filter(row => {
      if (row.checked == false) {
        return row
      }
    })
    if (falseRows.length) {
      return false
    }
    return true
  }

  private checkAll(): void {
    let setCheckedTo = true
    if (this.allChecked()) {
      setCheckedTo = false
    }
    this.rows.forEach(row => {
      row.checked = setCheckedTo
    })
  }

  private retrieveAllResponsibilites(): void {
    this.$store.dispatch('responsibilityModule/getAllResponsibilities')
      .catch(e => {
        console.error('Error retrieving responsibilities', e)
      })
  }

  private showEditDialog(row: Responsibility): void {
    bus.$emit('emitOpenEditDialog', row) // eslint-disable-line @typescript-eslint/no-unsafe-call, @typescript-eslint/no-unsafe-member-access
  }

  private showDeleteDialog(row: Responsibility): void {
    bus.$emit('emitOpenDeleteDialog', row) // eslint-disable-line @typescript-eslint/no-unsafe-call, @typescript-eslint/no-unsafe-member-access
  }

  private formSubmit (): void {
    Notify.create('Approved')
  }

  mounted() {
    // TODO: Only fetch if doesn't exist, or needs update?
    this.retrieveAllResponsibilites()
    if (this.allResponsibilities() == []) { // <----- THIS DOESN'T WORK
      this.retrieveAllResponsibilites()
    }
  }
}
</script>

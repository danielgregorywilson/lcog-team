<template>
  <div>
    <q-form
      @submit="formSubmit"
      @reset="formReset"
      class="q-gutter-md"
    >
      
      <table>
        <thead>
          <tr>
            <td colspan="3"></td>
            <td colspan="2" class="rowspan">Odometer</td>
            <td></td>
          </tr>
          <tr>
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
            <td>
              <div>
                <q-input filled v-model="row.date" mask="date" :rules="['date']" style="padding-bottom: 0px;">
                  <template v-slot:append>
                    <q-icon name="event" class="cursor-pointer">
                      <q-popup-proxy ref="qDateProxy" cover transition-show="scale" transition-hide="scale">
                        <q-date v-model="row.date">
                          <div class="row items-center justify-end">
                            <q-btn v-close-popup label="Close" color="primary" flat />
                          </div>
                        </q-date>
                      </q-popup-proxy>
                    </q-icon>
                  </template>
                </q-input>
              </div>
            </td>

            <td>
              <q-input outlined v-model="row.purpose" />
            </td>
            <td>
              <q-input outlined v-model="row.subfund" />
            </td>
            <td>
              <q-input outlined v-model="row.start" />
            </td>
            <td>
              <q-input outlined v-model="row.finish" />
            </td>
            <div v-if="row.finish && row.start && row.start < row.finish">{{ (parseInt(row.finish) - parseInt(row.start)).toFixed() }}</div>

          </tr>
          <tr>
            <td colspan="4"></td>
            <td>Total Miles:</td>
            <td>{{ totalMiles() }}</td>
          </tr>
          <tr>
            <td colspan="4"></td>
            <td>x $0.585</td>
            <td>${{ (totalMiles() * 0.585).toFixed(2) }}</td>
          </tr>

        </tbody>

      </table>

      

      <q-btn unelevated rounded color="primary" icon="add" label="Add Row" @click="addRow()" />

      <div>
        <div class="text-subtitle1 q-mb-sm">By clicking "Submit" below, I certify that all the expenses listed above are true and correct and were incurred on official LCOG business.</div>
        <q-btn label="Submit" type="submit" color="primary"/>
        <q-btn label="Reset" type="reset" color="primary" flat class="q-ml-sm" />
      </div>
    </q-form>

    <!-- {{rows}} -->

  </div>
</template>

<style scoped lang="scss">
table {

  thead {
    font-weight: bold;
  }

  td.rowspan {
    text-align: center;
  }

  tfoot {
    font-weight: bold;
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

  private emptyRow = {'date': '', 'purpose': '', 'subfund': '', 'start': '', 'finish': ''}
  private rows = [{'date': '', 'purpose': '', 'subfund': '', 'start': '', 'finish': ''}]

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

  private totalMiles(): number {
    let totalMiles = 0
    this.rows.forEach(row => {
      if (parseInt(row.finish) >= parseInt(row.start)) {
        totalMiles += parseInt(row.finish) - parseInt(row.start)
      }
    })
    return totalMiles
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

  private addRow(): void {
    this.rows.push({...this.emptyRow})
  }

  private formSubmit (): void {
    this.formReset()
    Notify.create('Submitted')
  }

  private formReset (): void {
    this.rows = []
    this.rows.push({...this.emptyRow})
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

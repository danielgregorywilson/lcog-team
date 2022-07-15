<template>
  <div>
    <q-table
      :data="managedTimeOffRequests()"
      :columns="columns"
      row-key="pk"
    >
      <template v-slot:body-cell-acknowledge="props">
        <q-td :props="props">
          <q-btn dense round color="red" icon="close" class="q-mr-sm"></q-btn>
          <q-btn dense round color="green" icon="check"></q-btn>
        </q-td>
      </template>
    </q-table>
  </div>
</template>

<style lang="scss">

</style>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { TimeOffRequestDates, TimeOffRequestRetrieve, VuexStoreGetters } from '../../store/types'

@Component
export default class TimeOffManageRequests extends Vue {
  private getters = this.$store.getters as VuexStoreGetters

  private columns = [
    { name: 'employee', label: 'Employee', field: 'employee_name', sortable: true, align: 'center' },
    { name: 'dates', label: 'Dates', field: 'dates', format: (obj: TimeOffRequestDates) => this.formatDates(obj), sortable: true, align: 'center' },
    { name: 'note', label: 'Note', field: 'note', align: 'center' },
    { name: 'acknowledge', label: 'Acknowledge?', field: 'acknowledged', align: 'center' },
  ]

  private formatDates(datesObj: TimeOffRequestDates) {
    let str = ''
    for (let i=0; i<datesObj.length; i++) {
      if (i >= 1) {
        str += '; '
      }
      if (datesObj[i].from == datesObj[i].to) {
        str += datesObj[i].from
      } else {
        str += `${datesObj[i].from} - ${datesObj[i].to}`
      }
    }
    return str
  }

  private managedTimeOffRequests(): Array<TimeOffRequestRetrieve> {
    return this.getters['timeOffModule/managedTimeOffRequests'].results
  }

  private retrieveManagedTimeOffRequests(): void {
    this.$store.dispatch('timeOffModule/getManagedTimeOffRequests')
      .catch(e => {
        console.error('Error retrieving my upcoming time off requests', e)
      })
  }

  mounted() {
    this.retrieveManagedTimeOffRequests()
  }
}
</script>

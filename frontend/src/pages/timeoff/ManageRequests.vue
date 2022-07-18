<template>
  <div>
    <q-table
      :data="managedTimeOffRequests()"
      :columns="columns"
      row-key="pk"
    >
      <template v-slot:body-cell-acknowledge="props">
        <q-td :props="props">
          <q-btn dense round color="red" icon="close" :outline="props.row.acknowledged == null || props.row.acknowledged == true" class="q-mr-sm" @click="acknowledgeRequest(props.row.pk, false)"></q-btn>
          <q-btn dense round color="green" icon="check" :outline="props.row.acknowledged == null || props.row.acknowledged == false" @click="acknowledgeRequest(props.row.pk, true)"></q-btn>
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
import TimeOffDataService from '../../services/TimeOffDataService'

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

  private acknowledgeRequest(pk: number, approve: boolean): void {
    TimeOffDataService.updatePartial(pk.toString(), {acknowledged: approve})
      .then(() => {
        // TODO: Get just the one we changed, not all of them
        this.retrieveManagedTimeOffRequests()
      })
      .catch(e => {
        console.error('Error acknowledging time off request', e)
      })
  }

  mounted() {
    this.retrieveManagedTimeOffRequests()
  }
}
</script>

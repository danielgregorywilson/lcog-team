<template>
  <div>
    <q-table
      :data="rows"
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
import { TimeOffRequestDates, VuexStoreGetters } from '../../store/types'

@Component
export default class TimeOffManageRequests extends Vue {
  private getters = this.$store.getters as VuexStoreGetters

  private columns = [
    { name: 'employee', label: 'Employee', field: 'employee', sortable: true, align: 'center' },
    { name: 'dates', label: 'Dates', field: 'dates', format: (obj: TimeOffRequestDates) => this.formatDates(obj), sortable: true, align: 'center' },
    { name: 'note', label: 'Note', field: 'note', align: 'center' },
    { name: 'acknowledge', label: 'Acknowledge?', field: 'acknowledged', align: 'center' },
  ]

  private rows = [
    {
      pk: 1,
      employee: 'Dan Wilson',
      dates: [ { 'from': '2022/06/09', 'to': '2022/06/16' }, { 'from': '2022/06/17', 'to': '2022/06/18' } ],
      note: 'Gotta get outta here',
      acknowledged: false
    },
    {
      pk: 2,
      employee: 'Dan Wilson',
      dates: [ { 'from': '2022/07/09', 'to': '2022/07/11' } ],
      note: 'State training',
      acknowledged: true
    },
    {
      pk: 3,
      employee: 'Keith Testerman',
      dates: [ { 'from': '2022/08/01', 'to': '2022/08/5' } ],
      note: 'Skydiving lessons',
      acknowledged: true
    },
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

  // private upcomingTimeOff(): Array<TimeOff> {
  //   return this.getters['timeOffModule/upcomingTimeOff'].results
  // }

  // private retrieveUpcomingTimeOff(): void {
  //   this.$store.dispatch('timeOffModule/getUpcomingTimeOff')
  //     .catch(e => {
  //       console.error('Error retrieving upcoming time off', e)
  //     })
  // }

  mounted() {
    // this.retrieveUpcomingTimeOff()
  }
}
</script>

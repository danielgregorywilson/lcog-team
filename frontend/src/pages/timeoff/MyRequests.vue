<template>
  <div>
    <q-table
      :data="rows"
      :columns="columns"
      row-key="pk"
    />
  </div>
</template>

<style lang="scss">

</style>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { VuexStoreGetters } from '../../store/types'

@Component
export default class TimeOffMyRequests extends Vue {
  private getters = this.$store.getters as VuexStoreGetters

  private columns = [
    { name: 'dates', label: 'Dates', field: 'dates', format: obj => this.formatDates(obj), sortable: true, align: 'center' },
    { name: 'note', label: 'Note', field: 'note', align: 'center' },
    { name: 'approved', label: 'Approved', field: 'approved', align: 'center' },
  ]

  private rows = [
    {
      pk: 1,
      dates: [ { 'from': '2022/06/09', 'to': '2022/06/16' }, { 'from': '2022/06/17', 'to': '2022/06/18' } ],
      note: 'Gotta get outta here',
      approved: false
    },
    {
      pk: 2,
      dates: [ { 'from': '2022/07/09', 'to': '2022/07/11' } ],
      note: 'State training',
      approved: true
    },
  ]

  private formatDates(datesObj) {
    let str = ''
    for (let i=0; i<datesObj.length; i++) {
      if (i >= 1) {
        str += '; '
      }
      str += datesObj[i].from + ' - ' + datesObj[i].to
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

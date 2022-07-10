<template>
  <div>
    <q-table
      :data="myTimeOffRequests()"
      :columns="columns"
      row-key="pk"
    />
  </div>
</template>

<style lang="scss">

</style>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { TimeOffRequestRetrieve, VuexStoreGetters } from '../../store/types'

@Component
export default class TimeOffMyRequests extends Vue {
  private getters = this.$store.getters as VuexStoreGetters

  private columns = [
    { name: 'dates', label: 'Dates', field: 'dates', format: obj => this.formatDates(obj), sortable: true, align: 'center' },
    { name: 'note', label: 'Note', field: 'note', align: 'center' },
    { name: 'approved', label: 'Approved', field: 'approved', align: 'center' },
  ]

  private formatDates(datesObj) {
    let str = ''
    for (let i=0; i<datesObj.length; i++) {
      if (i >= 1) {
        str += '; '
      }
      if (datesObj[i].constructor == String) {
        str += datesObj[i]
      } else {
        str += datesObj[i].from + ' - ' + datesObj[i].to
      }
    }
    return str
  }

  private myTimeOffRequests(): Array<TimeOffRequestRetrieve> {
    return this.getters['timeOffModule/myTimeOffRequests'].results
  }

  private retrieveMyTimeOffRequests(): void {
    this.$store.dispatch('timeOffModule/getMyTimeOffRequests')
      .catch(e => {
        console.error('Error retrieving my upcoming time off requests', e)
      })
  }

  mounted() {
    this.retrieveMyTimeOffRequests()
  }
}
</script>

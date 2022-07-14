<template>
  <div>
    <q-table
      :data="myTimeOffRequests()"
      :columns="columns"
      row-key="pk"
    >
      <template v-slot:body-cell-approved="props">
        <q-td :props="props">
          <q-icon v-if="props.row.acknowledged==null" color="orange" name="help" size="lg" />
          <q-icon v-if="props.row.acknowledged==false" color="red" name="cancel" size="lg" />
          <q-icon v-if="props.row.acknowledged && props.row.acknowledged==true" color="green" name="check_circle" size="lg" />
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
export default class TimeOffMyRequests extends Vue {
  private getters = this.$store.getters as VuexStoreGetters

  private columns = [
    { name: 'dates', label: 'Dates', field: 'dates', format: (obj: TimeOffRequestDates) => this.formatDates(obj), sortable: true, align: 'center' },
    { name: 'note', label: 'Note', field: 'note', align: 'center' },
    { name: 'approved', label: 'Approved', field: 'approved', align: 'center' },
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

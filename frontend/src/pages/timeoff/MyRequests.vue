<template>
  <div>
    <q-table
      :data="myTimeOffRequests()"
      :columns="columns"
      row-key="pk"
    >
      <template v-slot:body-cell-dates="props">
        <q-td key="dates" :props="props">
          {{ props.row.start_date }} - {{ props.row.end_date }}
        </q-td>
      </template>
      <template v-slot:body-cell-acknowledged="props">
        <q-td :props="props" class="row justify-center items-center">
          <q-icon v-if="props.row.acknowledged==null" color="orange" name="help" size="lg">
            <q-tooltip content-style="font-size: 16px">
              Your manager has not responded to this request.
            </q-tooltip>
          </q-icon>
          <q-icon v-if="props.row.acknowledged==false" color="red" name="cancel" size="lg">
            <q-tooltip content-style="font-size: 16px">
              Your manager has indicated an issue with this request.
            </q-tooltip>  
          </q-icon>
          <q-icon v-if="props.row.acknowledged && props.row.acknowledged==true" color="green" name="check_circle" size="lg">
            <q-tooltip content-style="font-size: 16px">
              Your manager has acknowledged this request.
            </q-tooltip>  
          </q-icon>
          <div v-if="props.row.conflicts.length != 0" class="q-ml-sm">
            <q-icon color="orange" name="warning" size="md">
              <q-tooltip content-style="font-size: 16px">
                <div>One or more team members with shared responsibilities will be also be unavailable:</div>
                <ul>
                  <li v-for="employee of props.row.conflicts" :key="employee.pk">
                    {{ employee.name }}: {{ employee.responsibility_names[0] }}<span v-if="employee.responsibility_names.length > 1"> and {{ employee.responsibility_names.length - 1 }} more</span>
                  </li>
                </ul>
              </q-tooltip>
            </q-icon>
          </div>
        </q-td>
      </template>
    </q-table>
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
    { name: 'dates', label: 'Dates', field: 'start_date', sortable: true, align: 'center' },
    { name: 'note', label: 'Note', field: 'note', align: 'center' },
    { name: 'acknowledged', label: 'Acknowledged', field: 'approved', align: 'center' },
  ]

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

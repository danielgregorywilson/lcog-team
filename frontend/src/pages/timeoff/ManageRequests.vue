<template>
  <div>
    <q-table
      :data="managedTimeOffRequests()"
      :columns="columns"
      row-key="pk"
    >
      <template v-slot:body-cell-dates="props">
        <q-td key="dates" :props="props">
          {{ props.row.start_date }} - {{ props.row.end_date }}
        </q-td>
      </template>
      <template v-slot:body-cell-acknowledge="props">
        <q-td :props="props" class="row justify-center items-center">
          <q-btn 
            dense round color="red" icon="close"
            :outline="props.row.acknowledged == null || props.row.acknowledged == true"
            :disable="props.row.acknowledged == false"
            class="q-mr-sm"
            @click="acknowledgeRequest(props.row.pk, false)"
          />
          <q-btn
            dense round color="green" icon="check"
            :outline="props.row.acknowledged == null || props.row.acknowledged == false"
            :disable="props.row.acknowledged == true"
            @click="acknowledgeRequest(props.row.pk, true)"
          />
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
import TimeOffDataService from '../../services/TimeOffDataService'

@Component
export default class TimeOffManageRequests extends Vue {
  private getters = this.$store.getters as VuexStoreGetters

  private columns = [
    { name: 'employee', label: 'Employee', field: 'employee_name', sortable: true, align: 'center' },
    { name: 'dates', label: 'Dates', field: 'start_date', sortable: true, align: 'center' },
    { name: 'note', label: 'Note', field: 'note', align: 'center' },
    { name: 'acknowledge', label: 'Acknowledge?', field: 'acknowledged', align: 'center' },
  ]

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

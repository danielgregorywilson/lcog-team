<template>
  <div>
    <q-table
      :data="managedTimeOffRequests()"
      :columns="columns"
      :pagination="tablePagination"
      row-key="pk"
      :grid="$q.screen.lt.md"
    >
      <template v-slot:body-cell-dates="props">
        <q-td key="dates" :props="props">
          {{ props.row.start_date }} - {{ props.row.end_date }}
        </q-td>
      </template>
      <template v-slot:body-cell-notes="props">
        <q-td key="notes" :props="props">
          <span v-if="props.row.note && !props.row.private_note">{{ props.row.note }}</span>
          <span v-if="!props.row.note && props.row.private_note"><span class="text-bold">Private:</span> {{ props.row.private_note }}</span>
          <span v-if="props.row.note && props.row.private_note"><span class="text-bold">Public:</span> {{ props.row.note }} / <span class="text-bold">Private:</span> {{ props.row.private_note }}</span>
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
      <!-- For grid mode, we need to specify everything in order for our action buttons to render -->
      <template v-slot:item="props">
        <div class="q-pa-xs col-xs-12 col-sm-6 col-md-4 col-lg-3 grid-style-transition">
          <q-card class="q-py-sm">
            <q-list dense>
              <q-item v-for="col in props.cols" :key="col.name">
                <div class="q-table__grid-item-row">
                  <div class="q-table__grid-item-title">{{ col.label }}</div>
                  <div class="q-table__grid-item-value" v-if="col.name != 'acknowledge'">
                    {{ col.value }}
                  </div>
                  <div class="q-table__grid-item-value row q-gutter-sm" v-else>
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
                  </div>
                </div>
              </q-item>
            </q-list>
          </q-card>
        </div>
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
    { name: 'notes', label: 'Notes', field: 'notes', align: 'center' },
    { name: 'acknowledge', label: 'Acknowledge?', field: 'acknowledged', align: 'center' },
  ]

  private tablePagination = {
    sortBy: 'dates',
    descending: true,
    rowsPerPage: 10
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
}
</script>
<template>
  <div>
    <q-table
      :dense="$q.screen.lt.sm"
      :data="myTimeOffRequests()"
      :columns="columns"
      :pagination="tablePagination"
      row-key="pk"
    >
      <template v-slot:header-cell-acknowledged="props">
        <q-th :props="props">
          <div v-if="$q.screen.gt.xs">{{ props.col.label }}</div>
          <div v-if="$q.screen.lt.sm"><q-icon name="thumb_up" size="1.5em" /></div>
        </q-th>
      </template>
      <template v-slot:body-cell-dates="props">
        <q-td key="dates" :props="props">
          <div v-if="$q.screen.gt.xs">{{ props.row.start_date }} - {{ props.row.end_date }}</div>
          <div v-if="$q.screen.xs">
            <div>{{ props.row.start_date }}</div>
            <div>{{ props.row.end_date }}</div>
          </div>
        </q-td>
      </template>
      <template v-slot:body-cell-notes="props">
        <q-td key="notes" :props="props">
          <span v-if="props.row.note && !props.row.private_note">{{ props.row.note }}</span>
          <span v-if="!props.row.note && props.row.private_note"><span class="text-bold">Private:</span> {{ props.row.private_note }}</span>
          <span v-if="props.row.note && props.row.private_note"><span class="text-bold">Public:</span> {{ props.row.note }} / <span class="text-bold">Private:</span> {{ props.row.private_note }}</span>
        </q-td>
      </template>
      <template v-slot:body-cell-acknowledged="props">
        <q-td :props="props">
          <div v-if="props.row.conflicts.length != 0">
            <q-icon color="orange" name="warning" size="md">
              <q-tooltip content-style="font-size: 16px">
                <div v-if="props.row.acknowledged==null" class="q-mb-sm row items-center">
                  <q-icon v-if="props.row.acknowledged==null" color="orange" name="help" size="lg" class="q-mr-sm" />
                  <div>Your manager has not responded to this request.</div>
                </div>
                <div v-if="props.row.acknowledged==false" class="q-mb-sm row items-center">
                  <q-icon v-if="props.row.acknowledged==false" color="red" name="cancel" size="lg" class="q-mr-sm" />
                  <div>Your manager has indicated an issue with this request.</div>
                </div>
                <div v-if="props.row.acknowledged && props.row.acknowledged==true" class="q-mb-sm row items-center">
                  <q-icon v-if="props.row.acknowledged && props.row.acknowledged==true" color="green" name="check_circle" size="lg" class="q-mr-sm" />
                  <div>Your manager has acknowledged this request.</div>
                </div>
                <div>One or more team members with shared responsibilities will be also be unavailable:</div>
                <ul>
                  <li v-for="employee of props.row.conflicts" :key="employee.pk">
                    {{ employee.name }}: {{ employee.responsibility_names[0] }}<span v-if="employee.responsibility_names.length > 1"> and {{ employee.responsibility_names.length - 1 }} more</span>
                  </li>
                </ul>
              </q-tooltip>
            </q-icon>
          </div>
          <div v-else>
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
          </div>
        </q-td>
      </template>
      <template v-slot:body-cell-actions="props">
        <q-td :props="props">
          <q-btn dense round flat color="grey" class="edit-request" @click="editRequest(props)" icon="edit"></q-btn>
          <q-btn dense round flat color="grey" class="delete-request" @click="showDeleteDialog(props)" icon="delete"></q-btn>
        </q-td>
      </template>
      <template v-slot:bottom-row>
        <q-tr @click="clickMakeRequest()" class="cursor-pointer">
          <q-td colspan="100%">
            <q-icon name="add" size="md" class="q-pr-sm"/>Request Time Off
          </q-td>
        </q-tr>
      </template>
    </q-table>

    <q-dialog v-model="deleteDialogVisible">
      <q-card>
        <q-card-section>
          <div class="row items-center">
            <q-avatar icon="insert_chart_outlined" color="primary" text-color="white" />
            <span class="q-ml-sm">Are you sure you want to delete this request?</span>
          </div>
          <div class="row justify-center text-center">{{ deleteDialogDatesText }}</div>
          <div class="row justify-center text-center">{{ deleteDialogNoteText }}</div>
        </q-card-section>

        <q-card-actions class="row justify-around">
          <q-btn flat label="Cancel" color="primary" v-close-popup />
          <q-btn flat label="Yes, delete it" color="primary" @click="deleteRow()" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<style lang="scss">

.q-table {
  .table-note {
    white-space: normal;
  }
}

</style>

<script lang="ts">
import TimeOffDataService from 'src/services/TimeOffDataService'
import { Notify } from 'quasar'
import { Component, Vue } from 'vue-property-decorator'
import { TimeOffRequestRetrieve, VuexStoreGetters } from '../../store/types'

interface QuasarTimeOffRequestTableRowClickActionProps {
  evt: MouseEvent;
  row: TimeOffRequestRetrieve;
}

@Component
export default class TimeOffMyRequests extends Vue {
  private getters = this.$store.getters as VuexStoreGetters

  private columns = [
    { name: 'dates', label: 'Dates', field: 'start_date', sortable: true, align: 'center' },
    { name: 'notes', label: 'Note', field: 'notes', align: 'center', classes: 'table-note' },
    { name: 'acknowledged', label: 'Acknowledged', field: 'approved', align: 'center' },
    { name: 'actions', label: 'Actions' },
  ]

  private tablePagination = {
    sortBy: 'dates',
    descending: true,
    rowsPerPage: 10
  }

  private deleteDialogVisible = false
  private deleteDialogDatesText = ''
  private deleteDialogNoteText = ''
  private rowPkToDelete = ''

  private myTimeOffRequests(): Array<TimeOffRequestRetrieve> {
    return this.getters['timeOffModule/myTimeOffRequests'].results
  }

  private retrieveMyTimeOffRequests(): void {
    this.$store.dispatch('timeOffModule/getMyTimeOffRequests')
      .catch(e => {
        console.error('Error retrieving my upcoming time off requests', e)
      })
  }

  private editRequest(props: QuasarTimeOffRequestTableRowClickActionProps): void {
    const rowPk = props.row.pk.toString()
    this.$router.push({ name: 'timeoff-request-detail', params: { pk: rowPk }})
      .catch(e => {
        console.error('Error navigating to time off request detail:', e)
      })
  }

  private showDeleteDialog(props: QuasarTimeOffRequestTableRowClickActionProps): void {
    this.rowPkToDelete = props.row.pk.toString()
    this.deleteDialogDatesText = `${props.row.start_date.toString()} - ${props.row.end_date.toString()}`
    this.deleteDialogNoteText = props.row.note
    this.deleteDialogVisible = true;
  }

  private deleteRow(): void {
    TimeOffDataService.delete(this.rowPkToDelete)
      .then(() => {
        Notify.create('Deleted a time off request.')
        this.retrieveMyTimeOffRequests()
      })
      .catch(e => {
        console.error('Error deleting time off request', e)
      })
  }

  private clickMakeRequest(): void {
    this.$router.push({'name': 'timeoff-new-request'})
      .catch(e => {
        console.error('Error navigating to new note page', e)
      })
  }

  mounted() {
    this.retrieveMyTimeOffRequests()
  }
}
</script>
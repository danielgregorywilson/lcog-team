<template>
  <div>
    <q-table
      title="All Responsibilities"
      :data="allResponsibilities()"
      :columns="allEmployeesTableColumns"
      row-key="pk"
    >
      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td key="name" :props="props" class="cursor-pointer">
            {{ props.row.name }}
            <q-popup-edit :value="props.row.name" persistent>
              <template v-slot="{ initialValue, value, emitValue, validate, set, cancel }">
                <q-input :value="props.row.name" dense autofocus @input="updateName(props.row.pk, $event)" />
                <div class="row justify-center q-mt-sm">
                  <q-btn flat class="text-primary" @click.stop="cancelUpdateName(props.row.pk, initialValue, cancel)">Cancel</q-btn>
                  <q-btn flat class="text-primary" @click.stop="updateResponsibility(props.row, cancel)" :disable="value === '' || initialValue === value">Set</q-btn>
                </div>
              </template>
            </q-popup-edit>
          </q-td>
          <q-td key="primary_employee_name" :props="props">
            <router-link v-if="props.row.primary_employee_pk" :to="{ name: 'employee-responsibilities', params: { pk: props.row.primary_employee_pk} }">
              {{ props.row.primary_employee_name }}
            </router-link>
            <!-- <q-popup-edit v-model="props.row.primary_employee_name" buttons>
              <q-input v-model="props.row.primary_employee_name" dense autofocus />
            </q-popup-edit> -->
          </q-td>
          <q-td key="secondary_employee_name" :props="props">
            <router-link v-if="props.row.secondary_employee_pk" :to="{ name: 'employee-secondary-responsibilities', params: { pk: props.row.secondary_employee_pk} }">
              {{ props.row.secondary_employee_name }}
            </router-link>
            <!-- <q-popup-edit v-model="props.row.secondary_employee_name" buttons>
              <q-input v-model="props.row.secondary_employee_name" dense autofocus />
            </q-popup-edit> -->
          </q-td>
          <q-td key="actions" :props="props">
            <q-btn class="col delete-button" dense round flat color="grey" @click="showDeleteDialog(props)" icon="delete"></q-btn>
          </q-td>
        </q-tr>
      </template>
    </q-table>

    <q-dialog v-model="deleteDialogVisible">
      <q-card>
        <q-card-section>
          <div class="row items-center">
            <q-avatar icon="list" color="primary" text-color="white" />
            <span class="q-ml-sm">Are you sure you want to delete this responsibility?</span>
          </div>
          <div class="row justify-center text-center">{{ deleteDialogResponsibilityName }}</div>
        </q-card-section>

        <q-card-actions class="row justify-around">
          <q-btn flat label="Cancel" color="primary" v-close-popup />
          <q-btn flat label="Yes, delete it" color="primary" @click="deleteRow()" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<style scoped lang="scss">
</style>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { Notify } from 'quasar'
import ResponsibilityDataService from '../../services/ResponsibilityDataService'
import { Responsibility, VuexStoreGetters } from '../../store/types'

interface QuasarResponsibilityTableRowClickActionProps {
  evt: MouseEvent;
  row: Responsibility;
}

@Component
export default class TimeOffRequests extends Vue {
  private deleteDialogVisible = false
  private deleteDialogResponsibilityName = ''
  private rowPkToDelete = ''

  private getters = this.$store.getters as VuexStoreGetters

  private allResponsibilities(): Array<Responsibility> {
    return this.getters['responsibilityModule/allResponsibilities'].results
  }
  
  private allEmployeesTableColumns = [
    { name: 'name', required: true, label: 'Name', field: 'name', sortable: true, align: 'left' },
    { name: 'primary_employee_name', label: 'Primary Employee', field: 'primary_employee_name', sortable: true },
    { name: 'secondary_employee_name', label: 'Secondary Employee', field: 'secondary_employee_name', sortable: true },
    { name: 'actions', label: 'Actions', },
  ]

  private primaryEmployeeTableColumns = [
    { name: 'name', required: true, label: 'Name', field: 'name', sortable: true, align: 'left' },
  ]

  private updateName(pk: number, name: string) {
    this.$store.commit('responsibilityModule/updateResponsibilityName', {pk, name})
  }

  private cancelUpdateName(pk: number, name: string, closePopupMethod: () => any) { // eslint-disable-line @typescript-eslint/no-explicit-any
    this.$store.commit('responsibilityModule/updateResponsibilityName', {pk, name})
    closePopupMethod()
  }

  private updateResponsibility(responsibility: Responsibility, closePopupMethod: () => any) { // eslint-disable-line @typescript-eslint/no-explicit-any
    return new Promise((resolve, reject) => {
      ResponsibilityDataService.update(responsibility.pk.toString(), {
        name: responsibility.name
        // TODO: employees
      })
      .then(() => {
        closePopupMethod()
        Notify.create('Updated responsibility')
        resolve('Updated')
      })
      .catch(e => {
        console.error('Error updating Responsibility:', e)
        reject(e)
      })
    })
  }

  private retrieveAllResponsibilites(): void {
    this.$store.dispatch('responsibilityModule/getAllResponsibilities')
      .catch(e => {
        console.error('Error retrieving responsibilities', e)
      })
  }

  private showDeleteDialog(props: QuasarResponsibilityTableRowClickActionProps): void {
    this.rowPkToDelete = props.row.pk.toString()
    this.deleteDialogResponsibilityName = props.row.name
    this.deleteDialogVisible = true;
  }

  private deleteRow(): void {
    ResponsibilityDataService.delete(this.rowPkToDelete)
      .then(() => {
        Notify.create('Deleted a responsibility.')
        this.retrieveAllResponsibilites()
      })
      .catch(e => {
        console.error('Error deleting responsibility', e)
      })
  }

  mounted() {
    // TODO: Only fetch if doesn't exist, or needs update?
    this.retrieveAllResponsibilites()
    if (this.allResponsibilities() == []) { // <----- THIS DOESN'T WORK
      this.retrieveAllResponsibilites()
    }
  }
}
</script>

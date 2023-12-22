<!-- Not converted from Quasar 1/Vue 2 -->
<template>
  <div class="q-py-sm">
    <q-table
      :data="teleworkApplications()"
      :columns="columns()"
      :dense="$q.screen.lt.lg"
      :grid="$q.screen.lt.md"
      :no-data-label="noDataLabel()"
      row-key="name"
    >
      <!-- Slots for header cells: Shrink the width when the screen is too small to see the whole table width -->
      <template v-slot:header-cell-employeeName="props">
        <th v-if="$q.screen.lt.lg" style="white-space: normal;">{{props.col.label}}</th>
        <th v-else>{{props.col.label}}</th>
      </template>
      <!-- Slots for body cells: Show dates in a familiar format; make sure status can wrap, and display action buttons -->
      <template v-slot:body-cell-status="props">
        <q-td style="white-space: normal;" :props="props">{{ props.row.status }}</q-td>
      </template>
      <template v-slot:body-cell-actions="props">
        <q-td :props="props">
          <div class="row">
            <q-btn class="col edit-button" dense round flat color="grey" @click="editApplication(props)" icon="edit"></q-btn>
            <q-btn class="col print-button" dense round flat disable color="grey" @click="printApplication(props)" icon="print"></q-btn>
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
                  <div class="q-table__grid-item-value" v-if="col.label != 'Actions'">
                    {{ col.value }}
                  </div>
                  <div class="q-table__grid-item-value row q-gutter-sm" v-else>
                    <q-btn class="col edit-button" dense round flat color="grey" @click="editApplication(props)" icon="edit"></q-btn>
                    <q-btn class="col print-button" dense round flat disable color="grey" @click="printApplication(props)" icon="print"></q-btn>
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

<style scoped>
.q-table tbody td.td-status {
    min-width: 135px;
    white-space: normal;
}
.q-table tbody td.wide-actions {
    min-width: 200px;
    white-space: normal;
}
</style>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import { ReviewNoteRetrieve } from '../store/types'
import { bus } from '../App.vue'
import { PerformanceReviewRetrieve } from '../store/types'
import '../filters'

interface EvaluationColumn {
  name: string;
  required?: boolean;
  label: string;
  align?: string;
  field?: string;
  sortable?: boolean;
  style?: string;
  headerStyle?: string;
}

interface QuasarTeleworkApplicationTableRowClickActionProps {
  evt: MouseEvent;
  row: PerformanceReviewRetrieve;
}

@Component
export default class TeleworkApplicationTable extends Vue {
  @Prop({required: true}) readonly signature!: boolean
  private teleworkApplications(): Array<ReviewNoteRetrieve> {
    if (this.signature) {
      return this.$store.getters['teleworkModule/allTeleworkApplicationsSignatureRequired'].results // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-return
    } else {
      return this.$store.getters['teleworkModule/allTeleworkApplicationsSignatureNotRequired'].results // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-return
    }
  }
  private columns(): Array<EvaluationColumn> {
    return [
        { name: 'employeeName', label: 'Employee', align: 'center', field: 'employee_name', sortable: true },
        { name: 'date', align: 'center', label: 'Date', field: 'date', sortable: true },
        { name: 'status', align: 'center', label: 'Status', field: 'status' },
        { name: 'actions', label: 'Actions', align: 'around', },
      ]
  }

  private noDataLabel(): string {
    return 'Great work! All done here.'
  }

  private retrieveTeleworkApplications(): void {
    if (this.signature) {
      this.$store.dispatch('teleworkModule/getAllTeleworkApplicationsSignatureRequired')
        .catch(e => {
          console.error('Error retrieving getAllTeleworkApplicationsSignatureRequired:', e)
        })
    } else {
      this.$store.dispatch('teleworkModule/getAllTeleworkApplicationsSignatureNotRequired')
        .catch(e => {
          console.error('Error retrieving getAllTeleworkApplicationsSignatureNotRequired:', e)
        })
    }
  }

  private editApplication(props: QuasarTeleworkApplicationTableRowClickActionProps): void {
    this.$router.push(`telework-application/${ props.row.pk }`)
      .catch(e => {
        console.error('Error navigating to application detail:', e)
      })
  }

  private printApplication(props: QuasarTeleworkApplicationTableRowClickActionProps): void {
    this.$router.push(`print/pr/${ props.row.pk }`)
      .catch(e => {
        console.error('Error printing PR:', e)
      })
  }

  created() {
    bus.$on('updateTeleworkApplicationTables', () => { // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-call
      this.retrieveTeleworkApplications()
    })
  }

  mounted() {
    this.retrieveTeleworkApplications();
  }
}
</script>

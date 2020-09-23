<template>
  <div class="q-py-sm">
    <q-table
      :data="reviewNotes.results"
      :columns="columns"
      row-key="name"
    >
      <template v-slot:body-cell-delete="props">
        <q-td :props="props">
          <q-btn dense round flat color="grey" @click="editNote(props)" icon="edit"></q-btn>
          <q-btn dense round flat color="grey" @click="showDeleteDialog(props)" icon="delete"></q-btn>
        </q-td>
      </template>
      <template v-slot:bottom-row>
        <q-tr @click="clickAddNote()" class="cursor-pointer">
          <q-td colspan="100%">
            <q-icon name="addchart" size="md" class="q-pr-sm"/>Add a note
          </q-td>
        </q-tr>
      </template>
    </q-table>


    <q-dialog persistent>
      <q-card>
        <q-card-section class="row items-center">
          <q-avatar icon="signal_wifi_off" color="primary" text-color="white" />
          <span class="q-ml-sm">You are currently not connected to any network.</span>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" color="primary" v-close-popup />
          <q-btn flat label="Turn on Wifi" color="primary" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>


    <q-dialog v-model="deleteDialogVisible" persistent>
      <q-card>
        <q-card-section>
          <div class="row items-center">
            <q-avatar icon="insert_chart_outlined" color="primary" text-color="white" />
            <span class="q-ml-sm">Are you sure you want to delete this note?</span>
          </div>
          <div class="row justify-center text-center">{{ deleteDialogEmployeeName }}</div>
          <div class="row justify-center text-center">{{ deleteDialogNoteText }}</div>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" color="primary" v-close-popup />
          <q-btn flat label="Yes, delete it" color="primary" @click="deleteRow()" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import ReviewNoteDataService from '../services/ReviewNoteDataService';

import ReveiwNoteService from '../services/ReviewNoteDataService';

import { ReviewNoteRetrieve } from '../store/types'

interface ReviewNoteColumn {
  name: string;
  label: string;
  align?: string;
  field?: string;
  sortable?: boolean;
}

interface QuasarReviewNoteTableRowClickActionProps {
  evt: MouseEvent;
  row: ReviewNoteRetrieve;
}

@Component
export default class ReviewNoteTable extends Vue {
  private reviewNotes: Array<ReviewNoteRetrieve> = []
  private columns: Array<ReviewNoteColumn> = [
    { name: 'employeeName', label: 'Employee Name', align: 'left', field: 'employee_name', sortable: true },
    { name: 'date', label: 'Date', field: 'date', sortable: true },
    { name: 'delete', label: 'Delete?'},
  ]
  private deleteDialogVisible = false
  private deleteDialogEmployeeName = ''
  private deleteDialogNoteText = ''
  private rowPkToDelete = ''

  private retrieveReviewNotes(): void {
    ReveiwNoteService.getAll()
      .then(response => {
        this.reviewNotes = response.data; // eslint-disable-line @typescript-eslint/no-unsafe-assignment
      })
      .catch(e => {
        console.log(e);
      });
  }

  private editNote(props: QuasarReviewNoteTableRowClickActionProps): void {
    this.$router.push(`note/${ props.row.pk }`)
      .catch(e => {
        console.log(e)
      })
  }

  private showDeleteDialog(props: QuasarReviewNoteTableRowClickActionProps): void {
    this.rowPkToDelete = props.row.pk.toString()
    this.deleteDialogEmployeeName = props.row.employee_name
    this.deleteDialogNoteText = props.row.note
    this.deleteDialogVisible = true;
  }

  private deleteRow(): void {
    ReviewNoteDataService.delete(this.rowPkToDelete)
      .then(response => {
        // TODO: Show a toast
        console.log(response)
        this.retrieveReviewNotes()
      })
      .catch(e => {
        console.log(e)
      })
  }

  private clickAddNote(): void {
    this.$router.push('note/new')
      .catch(e => {
        console.log(e)
      })
  }

  mounted() {
    this.retrieveReviewNotes();
  }
}
</script>
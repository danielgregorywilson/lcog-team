<template>
  <div class="q-py-sm">
    <q-table
      :data="reviewNotes()"
      :columns="columns"
      row-key="name"
    >
      <template v-slot:body-cell-date="props">
        <q-td key="date" :props="props">
          {{ props.row.date | readableDate }}
        </q-td>
      </template>
      <template v-slot:body-cell-actions="props">
        <q-td :props="props">
          <q-btn dense round flat color="grey" class="edit-note" @click="editNote(props)" icon="edit"></q-btn>
          <q-btn dense round flat color="grey" class="delete-note" @click="showDeleteDialog(props)" icon="delete"></q-btn>
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

    <q-dialog v-model="deleteDialogVisible">
      <q-card>
        <q-card-section>
          <div class="row items-center">
            <q-avatar icon="insert_chart_outlined" color="primary" text-color="white" />
            <span class="q-ml-sm">Are you sure you want to delete this note?</span>
          </div>
          <div class="row justify-center text-center">{{ deleteDialogEmployeeName }}</div>
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

<script lang="ts">
import { Notify } from 'quasar'
import { Component, Vue } from 'vue-property-decorator'
import ReviewNoteDataService from '../services/ReviewNoteDataService';
import { ReviewNoteRetrieve } from '../store/types'
import '../filters'

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
  private reviewNotes(): Array<ReviewNoteRetrieve> {
    return this.$store.getters['performanceReviewModule/allReviewNotes'].results // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-return
  }
  private columns: Array<ReviewNoteColumn> = [
    { name: 'employeeName', label: 'Employee Name', align: 'left', field: 'employee_name', sortable: true },
    { name: 'date', label: 'Date', field: 'date', sortable: true },
    { name: 'actions', label: 'Actions' },
  ]
  private deleteDialogVisible = false
  private deleteDialogEmployeeName = ''
  private deleteDialogNoteText = ''
  private rowPkToDelete = ''

  private retrieveReviewNotes(): void {
    this.$store.dispatch('performanceReviewModule/getAllReviewNotes')
      .catch(e => {
        console.error('Error retrieving review notes', e)
      })
  }

  private editNote(props: QuasarReviewNoteTableRowClickActionProps): void {
    this.$router.push(`note/${ props.row.pk }`)
      .catch(e => {
        console.error('Error navigating to note detail', e)
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
      .then(() => {
        Notify.create('Deleted a review note.')
        this.retrieveReviewNotes()
      })
      .catch(e => {
        console.error('Error deleting review note', e)
      })
  }

  private clickAddNote(): void {
    this.$router.push('note/new')
      .catch(e => {
        console.error('Error navigating to new note page', e)
      })
  }

  mounted() {
    if (this.reviewNotes() == null) {
      this.retrieveReviewNotes();
    }
  }
}
</script>

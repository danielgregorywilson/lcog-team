<template>
  <div class="q-py-sm">
    <q-table
      :data="reviewNotes.results"
      :columns="columns"
      row-key="name"
      @row-click="onRowClick"
    >
      <template v-slot:bottom-row>
        <q-tr>
          <q-td colspan="100%">
            <q-icon name="addchart" size="md" class="q-pr-sm"/>Add a note
          </q-td>
        </q-tr>
      </template>
    </q-table>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

import ReveiwNoteService from '../services/ReviewNoteDataService';

import { ReviewNote } from '../store/types'

interface ReviewNoteColumn {
  name: string,
  label: string,
  align?: string,
  field?: string,
  sortable?: boolean
}

@Component
export default class ReviewNoteTable extends Vue {
  private reviewNotes: Array<ReviewNote> = []
  private columns: Array<ReviewNoteColumn> = [
    { name: 'employeeName', label: 'Employee Name', align: 'left', field: 'employee_name', sortable: true },
    { name: 'date', label: 'Date', field: 'date', sortable: true },
    { name: 'delete', label: 'Delete?' },
  ]
  public retrieveReviewNotes(): void {
    ReveiwNoteService.getAll()
      .then(response => {
        this.reviewNotes = response.data; // eslint-disable-line @typescript-eslint/no-unsafe-assignment
      })
      .catch(e => {
        console.log(e);
      });
  }
  public onRowClick(evt: MouseEvent, row: ReviewNote): void {
    this.$router.push(`note/${ row.pk }`)
      .catch(e => {
        console.log(e)
      })
  }
  mounted() {
    this.retrieveReviewNotes();
  }
}
</script>

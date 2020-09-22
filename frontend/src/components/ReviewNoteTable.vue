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
import { defineComponent } from '@vue/composition-api';
import ReveiwNoteService from '../services/ReviewNoteDataService';
import { ReviewNote } from '../store/types'

export default defineComponent({
  name: 'ReviewNoteTable',
  data() {
    return {
      reviewNotes: [],
      columns: [
        { name: 'employeeName', label: 'Employee Name', align: 'left', field: 'employee_name', sortable: true },
        { name: 'date', label: 'Date', field: 'date', sortable: true },
        { name: 'delete', label: 'Delete?' },
      ],
    };
  },
  methods: {
    retrieveReviewNotes() {
      ReveiwNoteService.getAll()
        .then(response => {
          this.reviewNotes = response.data;
          console.log(response.data);
        })
        .catch(e => {
          console.log(e);
        });
    },
    onRowClick (evt: MouseEvent, row: ReviewNote) {
      debugger
      console.log('clicked on', evt, row)
      this.$router.push('note/' + row.pk)
    }
  },
  mounted() {
    this.retrieveReviewNotes();
  },
});
</script>

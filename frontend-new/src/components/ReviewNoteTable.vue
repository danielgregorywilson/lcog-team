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

<script setup lang="ts">




</script>

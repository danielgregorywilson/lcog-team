<template>
  <q-page>
    <div class="q-px-md">
      <h4 class="q-my-lg">Edit Feedback</h4>
      <p>
        Notes are visible to you when completing an evalutation for the
        employee. They are not visible to anyone else.
      </p>
      <EmployeeSelect
        name="employee"
        label="Employee"
        :employeePk="employeePk"
        :useLegalName="false"
        v-on:input="employeePk = $event.pk"
        :readOnly=false
        :fooBar="100"
      />
      <q-editor
        v-model="note"
        :toolbar="editorToolbar"
        class="q-my-md"
      />
      <q-btn
        color="white"
        id="review-note-update-button"
        text-color="black"
        label="Update"
        :disabled="!valuesAreChanged()"
        @click="updateReviewNote()"
      />
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { useQuasar } from 'quasar'
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

import EmployeeSelect from 'src/components/EmployeeSelect.vue'
import { useReviewStore } from 'src/stores/review'
import { getRoutePk } from 'src/utils'

const $q = useQuasar()
const route = useRoute()
const reviewStore = useReviewStore()

const notePk = ref('')
let employeePk = ref(-1)
let employeePkCurrentVal = ref(-1)
let note = ref('')
let noteCurrentVal = ref('')

let editorToolbar = [
  [
    {
      label: $q.lang.editor.align,
      icon: $q.iconSet.editor.align,
      fixedLabel: true,
      options: ['left', 'center', 'right', 'justify']
    }
  ],
  ['bold', 'italic', 'underline', 'removeFormat'],
  ['hr', 'link'],
  ['fullscreen'],
  ['quote', 'unordered', 'ordered', 'outdent', 'indent'],
  ['undo', 'redo']
]

function valuesAreChanged(): boolean {
  if (
    employeePk.value == employeePkCurrentVal.value &&
      note.value == noteCurrentVal.value
  ) {
    return false
  } else {
    return true
  }
}

function updateReviewNote(): void {
  reviewStore.updateReviewNote({
    pk: parseInt(notePk.value),
    employee_pk: employeePk.value,
    note: note.value
  })
    .then((reviewNote) => {
      employeePkCurrentVal.value = reviewNote.employee_pk
      noteCurrentVal.value = reviewNote.note
    })
}

function retrieveReviewNote(): void {
  const routePk = getRoutePk(route)
  if (routePk) {
    notePk.value = routePk
    reviewStore.getReviewNote(routePk)
      .then((reviewNote) => {
        employeePk.value = reviewNote.employee_pk
        note.value = reviewNote.note
        employeePkCurrentVal.value = employeePk.value
        noteCurrentVal.value = note.value
      })
  }
}

onMounted(() => {
  retrieveReviewNote();
})
</script>

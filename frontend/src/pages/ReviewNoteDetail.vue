<template>
  <q-page>
    <div class="q-px-md">
      <h4>Edit this Note</h4>
      <q-select v-model="employee" :options="options" label="Employee" class="q-pb-md" />
      <q-input
        input-class="review-note"
        v-model="note"
        label="Review Note"
        type="textarea"
        class="q-pb-md"
      />
      <q-btn color="white" id="review-note-update-button" text-color="black" label="Update" :disabled="!valuesAreChanged()" @click="updateReviewNote()" />
    </div>
  </q-page>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { AxiosEmployeeRetrieveManyServerResponse, AxiosReviewNoteRetrieveOneServerResponse, AxiosReviewNoteUpdateServerResponse } from '../store/types'
import EmployeeDataService from '../services/EmployeeDataService'
import ReviewNoteDataService from '../services/ReviewNoteDataService'


@Component
export default class ReviewNoteDetail extends Vue{
  private pk = ''
  private employeeCurrentVal: {label: string, value: number} = {label: '', value: -1}
  private noteCurrentVal = ''
  private employee: {label: string, value: number} = {label: '', value: -1}
  private note = ''
  private options: Array<{label: string; value: string}> = []

  private valuesAreChanged(): boolean {
    if (this.employee.value == this.employeeCurrentVal.value && this.note == this.noteCurrentVal) {
      return false
    } else {
      return true
    }
  }

  private updateReviewNote(): void {
    ReviewNoteDataService.update(this.pk, {
      employee_pk: this.employee.value,
      note: this.note
    })
      .then((response: AxiosReviewNoteUpdateServerResponse) => {
        this.employeeCurrentVal = {label: response.data.employee_name, value: response.data.employee_pk}
        this.noteCurrentVal = response.data.note
        this.$store.dispatch('performanceReviewModule/getAllReviewNotes')
          .catch(e => {
            console.error('Error getting all review notes after updating a review note:', e)
          })
      })
      .catch(e => {
        console.error('Error updating review note:', e)
      })
  }

  private retrieveReviewNote(): void {
    ReviewNoteDataService.get(this.$route.params.pk)
      .then((response: AxiosReviewNoteRetrieveOneServerResponse) => {
        this.pk = response.data.pk.toString()
        this.employee = {label: response.data.employee_name, value: response.data.employee_pk};
        this.note = response.data.note;
        this.employeeCurrentVal = this.employee
        this.noteCurrentVal = this.note
      })
      .catch(e => {
        console.error('Error getting review note:', e);
      });
  }

  private getOptions(): void {
    EmployeeDataService.getDirectReports()
      .then((response: AxiosEmployeeRetrieveManyServerResponse) => {
        this.options = response.data.results.map(obj => {
          return {label: obj.name, value: obj.pk.toString()}
        })
      })
      .catch(e => {
        console.error('Error getting direct reports:', e)
      })
  }

  mounted() {
    this.retrieveReviewNote();
    this.getOptions();
  }
}
</script>

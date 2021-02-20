<template>
  <q-page>
    <div class="q-px-md">
      <h4>Add a New Note</h4>
      <q-select v-model="employee" :options="options" label="Employee" class="q-pb-md" />
      <q-input
        input-class="review-note"
        v-model="note"
        label="Review Note"
        type="textarea"
        class="q-pb-md"
      />
      <q-btn id="review-note-create-button" color="white" text-color="black" label="Create" :disabled="!formIsFilled()" @click="createReviewNote()" />
    </div>
  </q-page>
</template>

<script lang="ts">
import { Notify } from 'quasar'
import { Component, Vue } from 'vue-property-decorator'
import { AxiosEmployeeRetrieveManyServerResponse } from '../store/types'
import EmployeeDataService from '../services/EmployeeDataService'


interface EmployeeOption {
  label: string;
  value: number;
}

@Component
export default class ReviewNoteCreate extends Vue{
  private options: Array<EmployeeOption> = []
  private employee: EmployeeOption = {label: '', value: -1}
  private note = ''

  private getOptions(): void {
    EmployeeDataService.getDirectReports()
      .then((response: AxiosEmployeeRetrieveManyServerResponse) => {
        this.options = response.data.results.map(obj => {
          return {label: obj.name, value: obj.pk}
        })
      })
      .catch(e => {
        console.error('Error getting direct reports:', e)
      })
  }

  private formIsFilled(): boolean {
    if (!!this.employee.value && !!this.note) {
      return true
    } else {
      return false
    }
  }

  private createReviewNote(): void {
    this.$store.dispatch('performanceReviewModule/createReviewNote', {employee_pk: this.employee.value, note: this.note})
      .then(() => {
        Notify.create('Created a review note.')
        this.$router.push('/')
          .then(() => {
            location.reload() // TODO: This seems to be necessary in order to immediately edit a review note after creating it.
          })
          .catch(e => {
            console.error('Error navigating to dashboard after creating review note:', e)
          })
      })
      .catch(e => {
        console.error('Error creating review note:', e)
      })
  }

  mounted() {
    this.getOptions();
  }
}
</script>

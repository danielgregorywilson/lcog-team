<template>
  <q-page>
    <q-btn color="white" text-color="black" icon="west" label="Go Back" class="q-mx-md q-mt-md" @click="goBack()" />
    <div class="q-px-md">
      <h4>Add a New Note</h4>
      <q-select v-model="employee" :options="options" label="Employee" class="q-pb-md" />
      <q-input
        v-model="note"
        label="Review Note"
        type="textarea"
        class="q-pb-md"
      />
      <q-btn color="white" text-color="black" label="Update" :disabled="!formIsFilled()" @click="createReviewNote()" />
    </div>
  </q-page>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

import { EmployeeRetrieve } from '../store/types'

import EmployeeDataService from '../services/EmployeeDataService'
import ReviewNoteDataService from '../services/ReviewNoteDataService'
import ReveiwNoteService from '../services/ReviewNoteDataService'

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
      .then(response => {
        this.options = response.data.results.map((obj: EmployeeRetrieve) => {
          return {label: obj.employee_name, value: obj.pk}
        })
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
    ReviewNoteDataService.create({
      employee_pk: this.employee.value,
      note: this.note
    })
      .then(response => {
        this.$router.push('/')
      })
      .catch(e => {
        console.log(e)
      })
  }

  private goBack(): void {
    this.$router.back()
  }

  mounted() {
    this.getOptions();
  }
}
</script>

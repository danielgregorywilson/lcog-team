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
          return {label: obj.employee_name, value: obj.pk}
        })
      })
      .catch(e => {
        console.log(e)
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
      .then(response => {
        // TODO: Show a toast
        console.log(response)
        this.$router.push('/')
          .catch(e => {
            console.log(e)
          })
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

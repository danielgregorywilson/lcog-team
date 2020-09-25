<template>
  <q-page>
    <q-btn color="white" text-color="black" icon="west" label="Go Back" class="q-mx-md q-mt-md" @click="goBack()" />
    <div class="q-px-md">
      <h4>Performance Review for {{ employeeName }}</h4>
      <div>Scheduled for {{ date | readableDate }}</div>
      <h5>Your Notes for {{ employeeName }}</h5>
      <h5>Current Evaluation</h5>
      <h5>Modify Evaluation</h5>
      <div>
        <div class="row q-mb-md q-gutter-md items-start">
          <q-date v-model="discussionDate" class="col-4" />
          <q-input
            v-model="evaluation"
            label="Evaluation"
            type="textarea"
            class="q-pb-md col"
          />
        </div>
        <q-btn color="white" text-color="black" label="Update" :disabled="!valuesAreChanged()" @click="updateReviewNote()" />
      </div>

    </div>
  </q-page>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import PerformanceReviewDataService from '../services/PerformanceReviewDataService'
import { AxiosPerformanceReviewRetrieveOneServerResponse } from '../store/types'
import '../filters'

@Component
export default class PerformanceReviewDetail extends Vue{
  private employeeName: string = ''
  private date: Date
  private discussionDateCurrentVal: string
  private discussionDate: string
  private evaluationCurrentVal = ''
  private evaluation = ''

  private valuesAreChanged(): boolean {
    if (this.discussionDate == this.discussionDateCurrentVal && this.evaluation == this.evaluationCurrentVal) {
      return false
    } else {
      return true
    }
  }

  // private updateReviewNote(): void {
  //   ReviewNoteDataService.update(this.pk, {
  //     employee_pk: this.employee.value,
  //     note: this.note
  //   })
  //     .then((response: AxiosReviewNoteUpdateServerResponse) => {
  //       this.employeeCurrentVal = {label: response.data.employee_name, value: response.data.employee_pk}
  //       this.noteCurrentVal = response.data.note
  //     })
  //     .catch(e => {
  //       console.log(e)
  //     })
  // }

  private retrievePerformanceReview(): void {
    PerformanceReviewDataService.get(this.$route.params.pk)
      .then((response: AxiosPerformanceReviewRetrieveOneServerResponse) => {
        this.employeeName = response.data.employee_name
        this.date = response.data.date_of_review;
        this.discussionDate = response.data.date_of_discussion.toString()

        this.discussionDateCurrentVal = this.discussionDate
        this.evaluation = '' // TODO
        this.evaluationCurrentVal = this.evaluation
      })
      .catch(e => {
        console.log(e);
      });
  }

  private goBack(): void {
    this.$router.back()
  }

  mounted() {
    this.retrievePerformanceReview();
  }
}
</script>

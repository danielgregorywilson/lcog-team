<template>
  <q-page>
    <q-btn color="white" text-color="black" icon="west" label="Go Back" class="q-mx-md q-mt-md" @click="goBack()" />
    <div class="q-px-md">
      <h4>Performance Review for {{ employeeName }}</h4>
      <div>Scheduled for {{ date | readableDate }}</div>
      <h5>Your Notes for {{ employeeName }}</h5>
      <div class="q-pa-md row items-start q-gutter-md">
        <!-- TODO: Click card to edit note -->
        <!-- TODO: Style cards -->
        <q-card v-for="note in this.reviewNotes" :key="note.pk" class="my-card">
          <q-card-section>
            {{ note.date | readableDate }}
          </q-card-section>
           <q-card-section>
            {{ note.note }}
          </q-card-section>
        </q-card>
      </div>
      <h5>Modify Evaluation</h5>
      <div class="text-weight-bold q-pb-md">Discussion currently scheduled for {{ discussionDateCurrentVal | readableDate }}</div>
      <div>
        <div class="row q-mb-md q-gutter-md items-start">
          <div class="col col-md-auto col-sm-12">
            <div>Date of Discussion</div>
            <q-date v-model="discussionDate" :options="noWeekends" />
          </div>
          <q-input
            v-model="evaluation"
            label="Evaluation"
            type="textarea"
            class="q-pb-md col"
          />
        </div>
        <q-btn color="white" text-color="black" label="Update" :disabled="!valuesAreChanged()" @click="updatePerformanceReview()" />
      </div>

    </div>
  </q-page>
</template>

<script lang="ts">
import { date as quasarDate } from 'quasar'
import { Component, Vue } from 'vue-property-decorator'
import PerformanceReviewDataService from '../services/PerformanceReviewDataService'
import { AxiosPerformanceReviewRetrieveOneServerResponse, AxiosPerformanceReviewUpdateServerResponse, ReviewNoteRetrieve } from '../store/types'
import '../filters'
import ReviewNoteDataService from '../services/ReviewNoteDataService'

@Component
export default class PerformanceReviewDetail extends Vue{
  private pk = ''
  private employeePk = -1
  private employeeName = ''
  private date: Date = new Date()
  private discussionDateCurrentVal = ''
  private discussionDate = ''
  private evaluationCurrentVal = ''
  private evaluation = ''
  private reviewNotes: Array<ReviewNoteRetrieve> = []

  private valuesAreChanged(): boolean {
    if (this.discussionDate == this.discussionDateCurrentVal && this.evaluation == this.evaluationCurrentVal) {
      return false
    } else {
      return true
    }
  }

  private retrievePerformanceReview(): void {
    PerformanceReviewDataService.get(this.$route.params.pk)
      .then((response: AxiosPerformanceReviewRetrieveOneServerResponse) => {
        this.employeePk = response.data.employee_pk
        this.retrieveReviewNotes()
        this.pk = response.data.pk.toString()
        this.employeeName = response.data.employee_name
        this.date = response.data.date_of_review;
        this.discussionDate = response.data.date_of_discussion.toString().split('-').join('/') // TODO: Replace with .replaceAll() - new as of 8/2020 and not in Vetur yet
        this.discussionDateCurrentVal = this.discussionDate
        this.evaluation = response.data.evaluation
        this.evaluationCurrentVal = this.evaluation
      })
      .catch(e => {
        console.log(e)
      });
  }

  private retrieveReviewNotes(): void {
    ReviewNoteDataService.getAllManagerNotesForEmployee(this.employeePk)
      .then((response) => {
        this.reviewNotes = response.data
      })
      .catch(e => {
        console.log(e)
      })
  }

  private updatePerformanceReview(): void {
    PerformanceReviewDataService.update(this.pk, {
      date_of_discussion: this.discussionDate.split('/').join('-'), // TODO: Replace with .replaceAll() - new as of 8/2020 and not in Vetur yet
      evaluation: this.evaluation
    })
      .then((response: AxiosPerformanceReviewUpdateServerResponse) => {
        this.discussionDateCurrentVal = response.data.date_of_discussion.toString().split('-').join('/') // TODO: Replace with .replaceAll() - new as of 8/2020 and not in Vetur yet
        this.evaluationCurrentVal = response.data.evaluation
      })
      .catch(e => {
        console.log(e)
      })
  }

  private noWeekends(date: string): boolean {
    const day = quasarDate.getDayOfWeek(new Date(date))
    return day !== 6 && day !== 7
  }

  private goBack(): void {
    this.$router.back()
  }

  mounted() {
    this.retrievePerformanceReview();
  }
}
</script>

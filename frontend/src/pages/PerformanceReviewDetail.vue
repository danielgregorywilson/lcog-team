<template>
  <q-page>
    <q-btn color="white" text-color="black" icon="west" label="Go Back" class="q-mx-md q-mt-md" @click="goBack()" />
    <!-- {{ performanceReviews() }} -->
    <!-- {{ performanceReview() }} -->
    <div class="q-px-md">
      <h4>Performance Review for {{ employeeName }}</h4>
      <div>Scheduled for {{ date | readableDate }}</div>
      <h5>Your Notes for {{ employeeName }}</h5>
      <div class="q-pa-md row items-start q-gutter-md">
        <q-card v-for="note in this.reviewNotes" :key="note.pk" class="note-card" @click="onClickNoteCard(note.pk)">
          <q-card-section>
            <div class="text-bold">
              {{ note.date | readableDate }}
            </div>
            <div>
              {{ note.note }}
            </div>
          </q-card-section>
        </q-card>
      </div>
      <h5>Modify Evaluation</h5>
      <div v-if="discussionDateCurrentVal" class="text-weight-bold q-pb-md">Discussion currently scheduled for {{ discussionDateCurrentVal | readableDate }}</div>
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

<style scoped>
  .note-card:hover {
    background-color: lightgray;
    cursor: pointer;
  }
</style>

<script lang="ts">
import { date as quasarDate } from 'quasar'
import { Component, Vue } from 'vue-property-decorator'
import PerformanceReviewDataService from '../services/PerformanceReviewDataService'
import { AxiosManagerReviewNotesForEmployeeServerResponse, AxiosPerformanceReviewUpdateServerResponse, PerformanceReviewRetrieve, ReviewNoteRetrieve } from '../store/types'
import '../filters'
import ReviewNoteDataService from '../services/ReviewNoteDataService'

@Component
export default class PerformanceReviewDetail extends Vue {
  private pk = ''
  private employeePk = -1
  private employeeName = ''
  private date: Date = new Date()
  private discussionDateCurrentVal = ''
  private discussionDate = ''
  private evaluationCurrentVal = ''
  private evaluation = ''
  private reviewNotes: Array<ReviewNoteRetrieve> = []

  private performanceReviews(): Array<PerformanceReviewRetrieve> {
    return this.$store.getters['performanceReviewModule/allPerformanceReviews'].results // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-return
  }

  private performanceReview(): PerformanceReviewRetrieve {
    return this.performanceReviews().filter(review => {
      return review.pk.toString() == this.$route.params.pk
    })[0]
  }

  private valuesAreChanged(): boolean {
    if (this.discussionDate == this.discussionDateCurrentVal && this.evaluation == this.evaluationCurrentVal) {
      return false
    } else {
      return true
    }
  }

  private retrievePerformanceReviews(): void {
    this.$store.dispatch('performanceReviewModule/getAllPerformanceReviews')
      .catch(e => {
        console.log(e)
      })
  }

  private retrievePerformanceReview(): void {
    this.$store.dispatch('performanceReviewModule/getAllPerformanceReviews')
      .then(() => {
        // this.retrieveReviewNotes()
        const prs = this.$store.getters['performanceReviewModule/allPerformanceReviews'].results // eslint-disable-line
        const pr: PerformanceReviewRetrieve = prs.filter((pr: PerformanceReviewDetail) => pr.pk == this.$route.params.pk)[0] // eslint-disable-line

        this.employeePk = pr.employee_pk
        this.retrieveReviewNotes()
        this.pk = pr.pk.toString()
        this.employeeName = pr.employee_name
        this.date = pr.date_of_review;
        if (pr.date_of_discussion) {
          this.discussionDate = pr.date_of_discussion.toString().split('-').join('/') // TODO: Replace with .replaceAll() - new as of 8/2020 and not in Vetur yet
        }
        this.discussionDateCurrentVal = this.discussionDate
        this.evaluation = pr.evaluation
        this.evaluationCurrentVal = this.evaluation

      })
      .catch(e => {
        console.log(e)
      })
  }

  private retrieveReviewNotes(): void {
    ReviewNoteDataService.getAllManagerNotesForEmployee(this.employeePk)
      .then((response: AxiosManagerReviewNotesForEmployeeServerResponse) => {
        this.reviewNotes = response.data
      })
      .catch(e => {
        console.log(e)
      })
  }

  private updatePerformanceReview(): void {
    PerformanceReviewDataService.update(this.pk, {
      pk: parseInt(this.pk, 10),
      date_of_discussion: this.discussionDate.split('/').join('-'), // TODO: Replace with .replaceAll() - new as of 8/2020 and not in Vetur yet
      evaluation: this.evaluation
    })
      .then((response: AxiosPerformanceReviewUpdateServerResponse) => {
        this.discussionDateCurrentVal = response.data.date_of_discussion.toString().split('-').join('/') // TODO: Replace with .replaceAll() - new as of 8/2020 and not in Vetur yet
        this.evaluationCurrentVal = response.data.evaluation
        // TODO: This is bad. We should only get the reviews of type that we need
        this.$store.dispatch('performanceReviewModule/getAllPerformanceReviewsActionRequired')
          .catch(e => {
            console.log(e)
          })
        this.$store.dispatch('performanceReviewModule/getAllPerformanceReviewsActionNotRequired')
          .catch(e => {
            console.log(e)
          })
      })
      .catch(e => {
        console.log(e)
      })
  }

  private noWeekends(date: string): boolean {
    const day = quasarDate.getDayOfWeek(new Date(date))
    return day !== 6 && day !== 7
  }

  private onClickNoteCard(pk: number): void {
    this.$router.push(`/note/${ pk }`)
      .catch(e => {
        console.log(e)
      })
  }

  private goBack(): void {
    this.$router.back()
  }

  mounted() {
    this.retrievePerformanceReview()
  }
}
</script>

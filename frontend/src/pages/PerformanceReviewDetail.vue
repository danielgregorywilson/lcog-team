<template>
  <q-page>
    <q-btn color="white" text-color="black" icon="west" label="Go Back" class="q-mx-md q-mt-md" @click="goBack()" />
    <div class="q-px-md">
      <h4>Performance Evaluation Report for {{ employeeName }}</h4>
      <div v-if="currentUserIsManagerOfEmployee()">
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
      </div>
      <div v-if="currentUserIsManagerOfEmployee()">
        <h5>Modify Evaluation</h5>
        <div class="">
          <div class="row">
            <div class="col eval-box">
              <div class="row">Employee:</div>
              <div class="row">{{ employeeName }}</div>
            </div>
            <div class="col eval-box">
              <div class="row">Manager:</div>
              <div class="row">{{ managerName }}</div>
            </div>
            <div class="col eval-box">
              <div class="row">Performance Period:</div>
              <div class="row"></div>
            </div>
            <div class="col eval-box">
              <div class="row">Effective Date:</div>
              <div class="row"></div>
            </div>
          </div>
          <div class="row">
            <div class="col eval-box">
              <div class="row">Division:</div>
              <div class="row"></div>
            </div>
            <div class="col eval-box">
              <div class="row">Unit/Program:</div>
              <div class="row"></div>
            </div>
            <div class="col eval-box">
              <div class="row">Job Title:</div>
              <div class="row"></div>
            </div>
          </div>
          <div class="row eval-box text-uppercase">Evaluation Type:</div>
          <div class="row eval-box text-uppercase">Action:</div>
        </div>

        <h6 class="text-uppercase">Rating Scale</h6>

        <div>
          <div class="row q-mb-md q-gutter-md items-start">
            <div class="col col-md-auto col-sm-12">
              <div>Date of Discussion</div>
              <q-date v-model="discussionDate" :options="noWeekends" />
            </div>
            <q-input
              v-model="evaluationSuccesses"
              label="Evaluation"
              type="textarea"
              class="q-pb-md col"
            />
          </div>
          <q-btn color="white" text-color="black" label="Update" :disabled="!valuesAreChanged()" @click="updatePerformanceReview()" />
        </div>
      </div>
    </div>
  </q-page>
</template>

<style scoped>
  .note-card:hover {
    background-color: lightgray;
    cursor: pointer;
  }
  .eval-box {
    border: black 2px solid;
    padding: 5px;
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
  private managerPk = -1
  private employeeName = ''
  private managerName = ''
  private date: Date = new Date()
  private discussionDateCurrentVal = ''
  private discussionDate = ''
  private evaluationSuccessesCurrentVal = ''
  private evaluationSuccesses = ''
  private reviewNotes: Array<ReviewNoteRetrieve> = []

  private isUpperManager(): boolean {
    return this.$store.getters['userModule/getEmployeeProfile'].is_upper_manager // eslint-disable-line
  }

  private currentUserIsManagerOfEmployee(): boolean {
    return this.managerPk == this.$store.getters['userModule/getEmployeeProfile'].pk // eslint-disable-line
  }

  private valuesAreChanged(): boolean {
    if (this.discussionDate == this.discussionDateCurrentVal && this.evaluationSuccesses == this.evaluationSuccessesCurrentVal) {
      return false
    } else {
      return true
    }
  }

  private retrievePerformanceReview(): void {
    let data = {}
    if (this.isUpperManager()) {
      data = {'isUpperManager': true}
    }
    this.$store.dispatch('performanceReviewModule/getAllPerformanceReviews', data)
      .then(() => {
        // this.retrieveReviewNotes()
        const prs = this.$store.getters['performanceReviewModule/allPerformanceReviews'].results // eslint-disable-line
        const pr: PerformanceReviewRetrieve = prs.filter((pr: PerformanceReviewDetail) => pr.pk == this.$route.params.pk)[0] // eslint-disable-line

        this.employeePk = pr.employee_pk
        this.managerPk = pr.manager_pk
        this.retrieveReviewNotes()
        this.pk = pr.pk.toString()
        this.employeeName = pr.employee_name
        this.managerName = pr.manager_name
        this.date = pr.date_of_review;
        if (pr.date_of_discussion) {
          this.discussionDate = pr.date_of_discussion.toString().split('-').join('/') // TODO: Replace with .replaceAll() - new as of 8/2020 and not in Vetur yet
        }
        this.discussionDateCurrentVal = this.discussionDate
        this.evaluationSuccesses = pr.evaluation_successes
        this.evaluationSuccessesCurrentVal = this.evaluationSuccesses

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
      evaluation: this.evaluationSuccesses
    })
      .then((response: AxiosPerformanceReviewUpdateServerResponse) => {
        // this.discussionDateCurrentVal = response.data.date_of_discussion.toString().split('-').join('/') // TODO: Replace with .replaceAll() - new as of 8/2020 and not in Vetur yet
        this.evaluationSuccessesCurrentVal = response.data.evaluationSuccesses
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

<template>
  <q-page>
    <q-btn color="white" text-color="black" icon="west" label="Go Back" class="q-mx-md q-mt-md" @click="goBack()" />
    <div class="q-px-md">
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
        <h4>Performance Evaluation Report for {{ employeeName }}</h4>
        <div class="eval-grid-container">
            <div class="eval-box eval-box-1">
                <div class="row">Employee:</div>
                <div class="row">{{ employeeName }}</div>
            </div>
            <div class="eval-box eval-box-2">
                <div class="row">Manager:</div>
                <div class="row">{{ managerName }}</div>
            </div>
            <div class="eval-box eval-box-3">
                <div class="row">Performance Period:</div>
                <div class="row"></div>
            </div>
            <div class="eval-box eval-box-4">
                <div class="row">Effective Date:</div>
                <div class="row"></div>
            </div>
            <div class="eval-box eval-box-5">
                <div class="row">Division:</div>
                <div class="row"></div>
            </div>
            <div class="eval-box eval-box-6">
                <div class="row">Unit/Program:</div>
                <div class="row"></div>
            </div>
            <div class="eval-box eval-box-7">
                <div class="row">Job Title:</div>
                <div class="row"></div>
            </div>
            <div class="row eval-box eval-box-full text-uppercase">Evaluation Type:</div>
            <div class="row eval-box eval-box-full text-uppercase">Action:</div>
        </div>

        <h5 class="text-uppercase text-center">Rating Scale</h5>
        <div class="rating-grid-container">
          <div class="rating-box">(1)* Needs Improvement</div>
          <div class="rating-box">The employee’s work performance does not consistently meet the standards of the position. Serious effort is needed to improve performance.</div>
          <div class="rating-box">(2) Meets Job Requirments</div>
          <div class="rating-box">The employee’s work performance consistently meets the standards of the position.</div>
          <div class="rating-box">(3) Exceeds Job Requirments</div>
          <div class="rating-box">The employee’s work performance is frequently or consistently above the level of a satisfactory employee.</div>
          <div class="rating-box">(N/A> Not Applicable</div>
          <div class="rating-box">Does not pertain to the employee’s actual job duties.</div>
        </div>
        <div>*Factors rated (1) Needs improvement must be addressed with a Performance Agreement for improvement.</div>

        <hr />

        <h5 class="text-uppercase">I. Performance Factors Reviewed</h5>
        <div class="factors-grid-container">
          <div class="factors-box">Performance Factors Reviewed</div>
          <div class="factors-box">Needs Improvement</div>
          <div class="factors-box">Meets Job Requirments</div>
          <div class="factors-box">Exceeds Job Requirements</div>
          <div class="factors-box">Not Applicable</div>
          <div class="factors-box">
              <div class="row">Job Knowledge</div>
              <div class="row">Present knowledge of techniques, skills, procedures, technologies, equipment, rules and policies of position.</div>
          </div>
          <div class="factors-box"><q-checkbox /></div>
          <div class="factors-box"><q-checkbox /></div>
          <div class="factors-box"><q-checkbox /></div>
          <div class="factors-box"><q-checkbox /></div>
        </div>

        <h5 class="text-uppercase">II. Employee's Successes</h5>
        <q-input
          v-model="evaluationSuccesses"
          type="textarea"
        />

        <h5 class="text-uppercase">III. Opportunities for Growth</h5>
        <q-input
          v-model="evaluationOpportunities"
          type="textarea"
        />

        <h5 class="text-uppercase">IV. Goals for the Coming Year (to be discussed and determined during the evaluation)</h5>
        <q-input
          v-model="evaluationGoalsManager"
          type="textarea"
        />

        <!-- <h5 class="text-uppercase">V. Goals for the Coming Year (Employee)</h5>
        <q-input
          v-model="evaluationGoalsEmployee"
          type="textarea"
        /> -->

        <h5 class="text-uppercase">V. Employee Comments</h5>
        <q-input
          v-model="evaluationCommentsEmployee"
          type="textarea"
        />

        <h5 class="text-uppercase">VI. Position Description Review</h5>
        <q-checkbox />Position Description has been reviewed with employee.

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
        </div>

        <div id="sticky-footer" >
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
  .eval-grid-container {
    display: grid;
    background-color: black;
    padding: 4px;
    grid-gap: 4px;
  }
  .eval-box {
    background-color: white;
    padding: 5px;
  }
  .eval-box-1 {
    grid-column-start: 1;
    grid-column-end: 4;
  }
  .eval-box-2 {
    grid-column-start: 4;
    grid-column-end: 7;
  }
  .eval-box-3 {
    grid-column-start: 7;
    grid-column-end: 10;
  }
  .eval-box-4 {
    grid-column-start: 10;
    grid-column-end: 13;
  }
  .eval-box-5 {
    grid-column-start: 1;
    grid-column-end: 5;
  }
  .eval-box-6 {
    grid-column-start: 5;
    grid-column-end: 9;
  }
  .eval-box-7 {
    grid-column-start: 9;
    grid-column-end: 13;
  }
  .eval-box-full {
    grid-column-start: 1;
    grid-column-end: 13;
  }
  .eval-box-full {
    grid-column-start: 1;
    grid-column-end: 13;
  }
  .rating-grid-container {
    display: grid;
    background-color: black;
    padding: 2px;
    grid-gap: 2px;
    grid-template-columns: auto auto;
  }
  .rating-box {
    background-color: white;
    padding: 5px;
  }
  .factors-grid-container {
    display: grid;
    background-color: black;
    padding: 2px;
    grid-gap: 2px;
    grid-template-columns: auto auto auto auto auto;
  }
  .factors-box {
    background-color: white;
    padding: 5px;
  }
  #sticky-footer {
    padding: 10px;
    background-color: rgb(25, 118, 210);
    position: fixed;
    bottom: 0;
    width: 100%
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
  private evaluationOpportunitiesCurrentVal = ''
  private evaluationOpportunities = ''
  private evaluationGoalsManagerCurrentVal = ''
  private evaluationGoalsManager = ''
  private evaluationCommentsEmployeeCurrentVal = ''
  private evaluationCommentsEmployee = ''

  private reviewNotes: Array<ReviewNoteRetrieve> = []

  private isUpperManager(): boolean {
    return this.$store.getters['userModule/getEmployeeProfile'].is_upper_manager // eslint-disable-line
  }

  private currentUserIsManagerOfEmployee(): boolean {
    return this.managerPk == this.$store.getters['userModule/getEmployeeProfile'].pk // eslint-disable-line
  }

  private valuesAreChanged(): boolean {
    if (
      // this.discussionDate == this.discussionDateCurrentVal && // TODO: Remove
      this.evaluationSuccesses == this.evaluationSuccessesCurrentVal &&
      this.evaluationOpportunities == this.evaluationOpportunitiesCurrentVal &&
      this.evaluationGoalsManager == this.evaluationGoalsManagerCurrentVal &&
      this.evaluationCommentsEmployee == this.evaluationCommentsEmployeeCurrentVal
    ) {
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
        const pr: PerformanceReviewRetrieve = prs.filter((pr: PerformanceReviewRetrieve) => pr.pk == parseInt(this.$route.params.pk))[0] // eslint-disable-line

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
        this.evaluationOpportunities = pr.evaluation_opportunities
        this.evaluationOpportunitiesCurrentVal = this.evaluationOpportunities
        this.evaluationGoalsManager = pr.evaluation_goals_manager
        this.evaluationGoalsManagerCurrentVal = this.evaluationGoalsManager
        this.evaluationCommentsEmployee = pr.evaluation_comments_employee
        this.evaluationCommentsEmployeeCurrentVal = this.evaluationCommentsEmployee

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
      evaluationSuccesses: this.evaluationSuccesses,
      evaluationOpportunities: this.evaluationOpportunities,
      evaluationGoalsManager: this.evaluationGoalsManager,
      evaluationCommentsEmployee: this.evaluationCommentsEmployee
    })
      .then((response: AxiosPerformanceReviewUpdateServerResponse) => {
        // this.discussionDateCurrentVal = response.data.date_of_discussion.toString().split('-').join('/') // TODO: Replace with .replaceAll() - new as of 8/2020 and not in Vetur yet
        this.evaluationSuccessesCurrentVal = response.data.evaluation_successes
        this.evaluationOpportunitiesCurrentVal = response.data.evaluation_opportunities
        this.evaluationGoalsManagerCurrentVal = response.data.evaluation_goals_manager
        this.evaluationCommentsEmployeeCurrentVal = response.data.evaluation_comments_employee
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

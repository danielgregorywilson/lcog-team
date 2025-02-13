<template>
  <q-page>
    <div class="q-px-md">
      <h4 class="q-my-lg">Performance Review Self-Evaluation</h4>
      <p>
        Responding to these questions can help you prepare for you performance
        evaluation. As you read each question, think about performance; your
        progress; and your plans for future growth.
      </p>
      <ol> 
        <li>
          What were my specific accomplishments during this evaluation period?
          Give examples.
        </li>
        <li>How could my supervisor help me do a better job?</li>
        <li>
          How are my relationships and communications with
          peers/clients/providers? Are there areas for improvement? What
          behaviors or style changes do I need to work on to improve my
          performance?
        </li>
        <li>What abilities does my job require?</li>
        <li>
          Do I need more experience or training in any aspect of my current job?
          How could this be accomplished? What would I like to improve, change,
          or learn to improve my job performance?
        </li>
        <li>What are my goals for the coming year?</li>
        <li>What do I expect to be doing five years from now?</li>
      </ol>
      <div
        v-if="!currentUserIsEmployee() || employeeHasSigned() || props.print"
        class="read-only-text-area" v-html="evaluationCommentsEmployee"
      ></div>
      <q-editor
        v-else
        v-model="evaluationCommentsEmployee"
        :toolbar="editorToolbar"
        class="q-my-md"
      />
      <q-btn
        v-if="currentUserIsEmployee() && !employeeHasSigned()"
        id="save-comments-employee"
        color="white"
        text-color="black"
        label="Save comments"
        @click="updateEmployeeComments()"
        class="q-mt-sm"
        :disable="!employeeCommentsIsChanged()"
      />
    </div>
  </q-page>
</template>

<style scoped lang="scss">
</style>

<script setup lang="ts">
import { useQuasar } from 'quasar'
import { onMounted, ref, Ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { usePerformanceReviewStore } from 'src/stores/performancereview'
import { useUserStore } from 'src/stores/user'
import { PRSignatures } from 'src/types'
import { getRoutePk } from 'src/utils'

const $q = useQuasar()
const route = useRoute()
const router = useRouter()
const performanceReviewStore = usePerformanceReviewStore()
const userStore = useUserStore()

const props = defineProps<{
  print?: boolean,
}>()


let prPk = ref('')
let status = ref('')

let employeePk = ref(-1)
let managerPk = ref(-1)
let employeeName = ref('')
let managerName = ref('')
let periodStartDate = ref(new Date())
let periodEndDate = ref(new Date())
let effectiveDate = ref(new Date())
let division = ref('')
let unitOrProgram = ref('')
let jobTitle = ref('')

let evaluationTypeCurrentVal = ref('')
let evaluationType = ref('')
let probationaryEvaluationTypeCurrentVal = ref('')
let probationaryEvaluationType = ref('')
let stepIncreaseCurrentVal = ref('')
let stepIncrease = ref('')
let topStepBonusCurrentVal = ref('')
let topStepBonus = ref('')
let actionOtherCurrentVal = ref('')
let actionOther = ref('')

let evaluationCommentsEmployeeCurrentVal = ref('')
let evaluationCommentsEmployee = ref('')

let signatures: Ref<PRSignatures> = ref([['', '', new Date(), -1, false]])

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

function currentUserPk(): number {
  return userStore.getEmployeeProfile.employee_pk
}


function employeeHasSigned(): boolean {
  return !!signatures.value[0][2]
}

function currentUserIsEmployee(): boolean {
  return employeePk.value == currentUserPk()
}

function employeeCommentsIsChanged(): boolean {
  if (
    evaluationCommentsEmployee.value ==
      evaluationCommentsEmployeeCurrentVal.value
  ) {
    return false
  } else {
    return true
  }
}

function retrievePerformanceReview() {
  return new Promise((resolve, reject) => {
    const routePk = getRoutePk(route)
    if (routePk) {
      performanceReviewStore.getPerformanceReview(routePk)
        .then((pr) => {
          if (!pr) {
            console.log('PR does not seem to exist. Redirecting...')
            router.push('/')
              .catch(e => {
                console.error(
                  'Error navigating to dashboard upon not finding a matching ' +
                    'PR:',
                  e
                )
                reject(e)
              })
            return
          }
          status.value = pr.status
          employeePk.value = pr.employee_pk
          managerPk.value = pr.manager_pk

          prPk.value = pr.pk.toString()
          employeeName.value = pr.employee_name
          managerName.value = pr.manager_name
          periodStartDate.value = pr.period_start_date
          periodEndDate.value = pr.period_end_date
          effectiveDate.value = pr.effective_date
          division.value = pr.employee_division
          unitOrProgram.value = pr.employee_unit_or_program
          jobTitle.value = pr.employee_job_title

          evaluationType.value = pr.evaluation_type
          evaluationTypeCurrentVal.value = evaluationType.value
          probationaryEvaluationType.value = pr.probationary_evaluation_type
          probationaryEvaluationTypeCurrentVal.value =
            probationaryEvaluationType.value
          stepIncrease.value = pr.step_increase
          stepIncreaseCurrentVal.value = stepIncrease.value
          topStepBonus.value = pr.top_step_bonus
          topStepBonusCurrentVal.value = topStepBonus.value
          actionOther.value = pr.action_other
          actionOtherCurrentVal.value = actionOther.value

          evaluationCommentsEmployee.value = pr.evaluation_comments_employee
          evaluationCommentsEmployeeCurrentVal.value =
            evaluationCommentsEmployee.value

          signatures.value = pr.all_required_signatures

          resolve('Got PR')
        })
        .catch(e => {
          console.error('Error retrieving PR from API:', e)
          reject(e)
        })
    }
  })
}

function updateEmployeeComments(): void {
  performanceReviewStore.updatePerformanceReviewPartial(prPk.value.toString(), {
    evaluation_comments_employee: evaluationCommentsEmployee.value,
  })
    .then((pr) => {
      evaluationCommentsEmployeeCurrentVal.value =
        pr.evaluation_comments_employee
    })
}

onMounted(() => {
  retrievePerformanceReview()
    .catch(e => {
      console.error('Error retrieving PR on PR self evaluation page mount:', e)
    })
})
</script>

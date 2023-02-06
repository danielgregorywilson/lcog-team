<template>
  <div class="q-pt-md">
    <div class="label-radio-triplet">
      <div class="text-bold" id="step-increase">Step Increase:</div>
      <q-radio v-model="type" val="N" />
      <div>New</div>
      <q-radio v-model="type" val="R" />
      <div>Return</div>
      <q-radio v-model="type" val="M" />
      <div>Change/Modify</div>
      <q-radio v-model="type" val="E" />
      <div>Exit</div>
    </div>

    {{currentEmployeeTransition()}}

    <!-- Spacing for footer -->
    <div style="height: 80px;"></div>

    <div id="sticky-footer" class="row justify-between" v-if="true">
      <q-btn id="update-button" class="col-1" color="white" text-color="black" label="Update" :disabled="!valuesAreChanged()" @click="updateTransition()" />
      <!-- <q-btn v-if="this.showErrorButton && this.formErrorItems().length > 0" label="Show missing fields" icon="check" color="warning" @click="openErrorDialog('right')" /> -->
      <!-- <div class="col-3 self-center status">Current Status: {{ status }}</div> -->
    </div>
  </div>
</template>

<style scoped lang="scss">
.label-radio-triplet {
    display: grid;
    justify-content: center;
    align-items: center;
    grid-template-columns: auto auto auto auto auto auto auto auto auto;
  }
</style>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { bus } from '../../App.vue'
import EmployeeTransitionDataService from '../../services/EmployeeTransitionDataService'
import { EmployeeTransition, VuexStoreGetters, WorkflowInstance } from '../../store/types'

@Component
export default class EmployeeTransitionDetail extends Vue {
  private getters = this.$store.getters as VuexStoreGetters

  public currentEmployeeTransition(): EmployeeTransition {
    return this.getters['workflowModule/currentEmployeeTransition']
  }

  private transitionPk = ''

  public typeCurrentVal = ''
  public type = ''

  public retrieveEmployeeTransition() {
    const t = this.currentEmployeeTransition()
    
    this.transitionPk = t.pk.toString()
    
    this.type = t.type
    this.typeCurrentVal = this.type



    
    // return new Promise((resolve, reject) => {
    //   this.$store.dispatch('workflowModule/getCurrentEmployeeTransition', {pk: this.$route.params.pk})
    //     .then(() => {
    //       const wfInstance: WorkflowInstance = this.getters['workflowModule/currentWorkflowInstance'] // eslint-disable-line @typescript-eslint/no-unsafe-member-access
    //       if (!wfInstance) {
    //           console.log('Workflow instance does not seem to exist. Redirecting...')
    //           this.$router.push('/')
    //             .catch(e => {
    //               console.error('Error navigating to dashboard upon not finding a matching Workflow Instance:', e)
    //               reject(e)
    //             })
    //           return
    //         }
    //       if (!wfInstance.process_instances[0].completed_at) {
    //         this.currentStepInstance = wfInstance.process_instances[0].current_step_instance.pk
    //       } else {
    //         // Process Instance is complete
    //         this.currentStepInstance = -1
    //       }
    //       bus.$emit('updateProcessInstances') // Trigger ProcessInstanceDetail to get a new current step
    //       resolve('Got Workflow Instance')
    //     })
    //   .catch(e => {
    //     console.error('Error retrieving workflow instance', e)
    //     reject(e)
    //   })
    // })
  }

  public valuesAreChanged(): boolean {
    return true
    if (
      this.type == this.typeCurrentVal
      // this.probationaryEvaluationType == this.probationaryEvaluationTypeCurrentVal &&
      // this.stepIncrease == this.stepIncreaseCurrentVal &&
      // this.topStepBonus == this.topStepBonusCurrentVal &&
      // this.actionOther == this.actionOtherCurrentVal &&
      // this.factorJobKnowledge == this.factorJobKnowledgeCurrentVal &&
      // this.factorWorkQuality == this.factorWorkQualityCurrentVal &&
      // this.factorWorkQuantity == this.factorWorkQuantityCurrentVal &&
      // this.factorWorkHabits == this.factorWorkHabitsCurrentVal &&
      // this.factorAnalysis == this.factorAnalysisCurrentVal &&
      // this.factorInitiative == this.factorInitiativeCurrentVal &&
      // this.factorInterpersonal == this.factorInterpersonalCurrentVal &&
      // this.factorCommunication == this.factorCommunicationCurrentVal &&
      // this.factorDependability == this.factorDependabilityCurrentVal &&
      // this.factorProfessionalism == this.factorProfessionalismCurrentVal &&
      // this.factorManagement == this.factorManagementCurrentVal &&
      // this.factorSupervision == this.factorSupervisionCurrentVal &&
      // this.evaluationSuccesses == this.evaluationSuccessesCurrentVal &&
      // this.evaluationOpportunities == this.evaluationOpportunitiesCurrentVal &&
      // this.evaluationGoalsManager == this.evaluationGoalsManagerCurrentVal &&
      // this.evaluationCommentsEmployee == this.evaluationCommentsEmployeeCurrentVal &&
      // this.descriptionReviewedEmployee == this.descriptionReviewedEmployeeCurrentVal
    ) {
      return false
    } else {
      return true
    }
  }

  private updateTransition() {
    return new Promise((resolve, reject) => {
      EmployeeTransitionDataService.update(this.transitionPk, {
        type: this.type,
        // probationary_evaluation_type: this.probationaryEvaluationType,
        // step_increase: this.stepIncrease,
        // top_step_bonus: this.topStepBonus,
        // action_other: this.actionOther,
        // factor_job_knowledge: this.factorJobKnowledge,
        // factor_work_quality: this.factorWorkQuality,
        // factor_work_quantity: this.factorWorkQuantity,
        // factor_work_habits: this.factorWorkHabits,
        // factor_analysis: this.factorAnalysis,
        // factor_initiative: this.factorInitiative,
        // factor_interpersonal: this.factorInterpersonal,
        // factor_communication: this.factorCommunication,
        // factor_dependability: this.factorDependability,
        // factor_professionalism: this.factorProfessionalism,
        // factor_management: this.factorManagement,
        // factor_supervision: this.factorSupervision,
        // evaluation_successes: this.evaluationSuccesses,
        // evaluation_opportunities: this.evaluationOpportunities,
        // evaluation_goals_manager: this.evaluationGoalsManager,
        // evaluation_comments_employee: this.evaluationCommentsEmployee,
        // description_reviewed_employee: this.descriptionReviewedEmployee
      })
      .then((response: AxiosPerformanceReviewUpdateServerResponse) => {
        this.typeCurrentVal = response.data.type
        
        // this.status = response.data.status

        // this.evaluationTypeCurrentVal = response.data.evaluation_type
        // this.probationaryEvaluationTypeCurrentVal = response.data.probationary_evaluation_type
        // this.stepIncreaseCurrentVal = response.data.step_increase
        // this.topStepBonusCurrentVal = response.data.top_step_bonus
        // this.actionOtherCurrentVal = response.data.action_other

        // this.factorJobKnowledgeCurrentVal = response.data.factor_job_knowledge
        // this.factorWorkQualityCurrentVal = response.data.factor_work_quality
        // this.factorWorkQuantityCurrentVal = response.data.factor_work_quantity
        // this.factorWorkHabitsCurrentVal = response.data.factor_work_habits
        // this.factorAnalysisCurrentVal = response.data.factor_analysis
        // this.factorInitiativeCurrentVal = response.data.factor_initiative
        // this.factorInterpersonalCurrentVal = response.data.factor_interpersonal
        // this.factorCommunicationCurrentVal = response.data.factor_communication
        // this.factorDependabilityCurrentVal = response.data.factor_dependability
        // this.factorProfessionalismCurrentVal = response.data.factor_professionalism
        // this.factorManagementCurrentVal = response.data.factor_management
        // this.factorSupervisionCurrentVal = response.data.factor_supervision

        // this.evaluationSuccessesCurrentVal = response.data.evaluation_successes
        // this.evaluationOpportunitiesCurrentVal = response.data.evaluation_opportunities
        // this.evaluationGoalsManagerCurrentVal = response.data.evaluation_goals_manager
        // this.evaluationCommentsEmployeeCurrentVal = response.data.evaluation_comments_employee

        // this.descriptionReviewedEmployeeCurrentVal = response.data.description_reviewed_employee

        // this.signatures = response.data.all_required_signatures






        // if (this.formErrorItems().length > 0) {
        //   this.showErrorButton = true
        // }


        resolve('Updated')
      })
      .catch(e => {
        console.error('Error updating Employee Transition', e)
        reject(e)
      })
    })
  }

  created() {
    // TODO: We should only set state once, but when yoyu load /transition this runs twice
    bus.$on('workflowInstanceRetrieved', () => {
      this.retrieveEmployeeTransition()
    })
  }

  mounted() {
    this.retrieveEmployeeTransition()
  }
  
}
</script>

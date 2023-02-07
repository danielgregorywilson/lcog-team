<template>
  <div class="q-pt-md">
    <div class="row items-center">
      <q-radio v-model="type" val="N" />
      <div>New</div>
      <q-radio v-model="type" val="R" />
      <div>Return</div>
      <q-radio v-model="type" val="M" />
      <div>Change/Modify</div>
      <q-radio v-model="type" val="E" />
      <div>Exit</div>
    </div>
    <div class="row">
      <q-input v-model="dateSubmitted" label="Date Submitted" class="q-mr-md" disable />
      <q-input v-model="submitterName" label="Submitter" disable />
    </div>
    <div class="row">
      <q-input v-model="employeeFirstName" label="First" class="q-mr-md" />
      <q-input v-model="employeeMiddleInitial" maxlength="1" label="M" class="q-mr-md" style="width: 1em" />
      <q-input v-model="employeeLastName" label="Last" />
    </div>
    <div class="row">
      <q-input v-model="employeePreferredName" label="Preferred Name, if different" style="width: 25em" />
    </div>
    <div class="row">
      <q-select v-model="employeeID" :options="['CLSD', 'CLID']" label="Employee ID" class="q-mr-sm"/>
      <q-input v-model="employeeNumber" label="Employee Number" />
    </div>
    <div class="row">
      <q-input v-model="employeeEmail" type="email" label="Email" hint="Email" />
    </div>

    {{currentEmployeeTransition()}}

    <!-- Spacing for footer -->
    <div style="height: 80px;"></div>

    <div id="sticky-footer" class="row justify-between" v-if="true">
      <q-btn id="update-button" class="col-1" color="white" text-color="black" label="Submit" :disabled="!valuesAreChanged()" @click="updateTransition()" />
      <!-- <q-btn v-if="this.showErrorButton && this.formErrorItems().length > 0" label="Show missing fields" icon="check" color="warning" @click="openErrorDialog('right')" /> -->
      <!-- <div class="col-3 self-center status">Current Status: {{ status }}</div> -->
    </div>
  </div>
</template>

<style scoped lang="scss">

</style>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { bus } from '../../App.vue'
import EmployeeTransitionDataService from '../../services/EmployeeTransitionDataService'
import {
  AxiosEmployeeTransitionUpdateServerResponse, EmployeeID, EmployeeTransition,
  VuexStoreGetters
} from '../../store/types'

@Component
export default class EmployeeTransitionDetail extends Vue {
  private getters = this.$store.getters as VuexStoreGetters

  public currentEmployeeTransition(): EmployeeTransition {
    return this.getters['workflowModule/currentEmployeeTransition']
  }

  private transitionPk = ''

  public typeCurrentVal = ''
  public type = ''
  public dateSubmitted?: Date = new Date()
  public submitterName = ''
  
  public employeeFirstNameCurrentVal = ''
  public employeeFirstName = ''
  public employeeMiddleInitialCurrentVal = ''
  public employeeMiddleInitial = ''
  public employeeLastNameCurrentVal = ''
  public employeeLastName = ''
  public employeePreferredNameCurrentVal = ''
  public employeePreferredName = ''
  public employeeNumberCurrentVal = ''
  public employeeNumber = ''
  public employeeIDCurrentVal: EmployeeID = ''
  public employeeID: EmployeeID = ''
  public employeeEmailCurrentVal = ''
  public employeeEmail = ''

  public retrieveEmployeeTransition() {
    const t = this.currentEmployeeTransition()
    
    this.transitionPk = t.pk.toString()
    
    this.type = t.type
    this.typeCurrentVal = this.type

    this.dateSubmitted = t.date_submitted
    this.submitterName = t.submitter_name

    this.employeeFirstName = t.employee_first_name
    this.employeeFirstNameCurrentVal = this.employeeFirstName
    this.employeeMiddleInitial = t.employee_middle_initial
    this.employeeMiddleInitialCurrentVal = this.employeeMiddleInitial
    this.employeeLastName = t.employee_last_name
    this.employeeLastNameCurrentVal = this.employeeLastName
    this.employeePreferredName = t.employee_preferred_name
    this.employeePreferredNameCurrentVal = this.employeePreferredName
    this.employeeNumber = t.employee_number
    this.employeeNumberCurrentVal = this.employeeNumber
    this.employeeID = t.employee_id
    this.employeeIDCurrentVal = this.employeeID
    this.employeeEmail = t.employee_email
    this.employeeEmailCurrentVal = this.employeeEmail
    


    
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
    if (
      this.type == this.typeCurrentVal &&
      this.employeeFirstName == this.employeeFirstNameCurrentVal &&
      this.employeeMiddleInitial == this.employeeMiddleInitialCurrentVal &&
      this.employeeLastName == this.employeeLastNameCurrentVal &&
      this.employeePreferredName == this.employeePreferredNameCurrentVal &&
      this.employeeID == this.employeeIDCurrentVal &&
      this.employeeNumber == this.employeeNumberCurrentVal &&
      this.employeeEmail == this.employeeEmailCurrentVal
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
        
        submitter_pk: this.$store.getters['userModule/getEmployeeProfile'].pk,
        
        employee_first_name: this.employeeFirstName,
        employee_middle_initial: this.employeeMiddleInitial,
        employee_last_name: this.employeeLastName,
        employee_preferred_name: this.employeePreferredName,
        employee_id: this.employeeID,
        employee_number: this.employeeNumber,
        employee_email: this.employeeEmail
      })
      .then((response: AxiosEmployeeTransitionUpdateServerResponse) => {
        this.typeCurrentVal = response.data.type
        
        this.dateSubmitted = response.data.date_submitted
        this.submitterName = response.data.submitter.name

        this.employeeFirstNameCurrentVal = response.data.employee_first_name
        this.employeeMiddleInitialCurrentVal = response.data.employee_middle_initial
        this.employeeLastNameCurrentVal = response.data.employee_last_name
        this.employeePreferredNameCurrentVal = response.data.employee_preferred_name
        this.employeeIDCurrentVal = response.data.employee_id
        this.employeeNumberCurrentVal = response.data.employee_number
        this.employeeEmailCurrentVal = response.data.employee_email

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

<template>
  <div class="q-pt-md">
    <div class="row items-center">
      <q-radio v-model="type" val="N" disable />
      <div>New</div>
      <q-radio v-model="type" val="R" disable />
      <div>Return</div>
      <q-radio v-model="type" val="M" disable />
      <div>Change/Modify</div>
      <q-radio v-model="type" val="E" disable />
      <div>Exit</div>
    </div>
    <div class="row">
      <q-input v-model="dateSubmitted" label="Date Submitted" class="q-mr-md" disable />
      <q-input v-model="submitterName" label="Submitter" disable />
    </div>
    <div class="row">
      <q-input v-model="employeeFirstName" label="First" class="q-mr-md" />
      <q-input v-model="employeeMiddleInitial" mask="A" label="M" class="q-mr-md" style="width: 1em" />
      <q-input v-model="employeeLastName" label="Last" />
    </div>
    <div class="row">
      <q-input v-model="employeePreferredName" label="Preferred Name, if different" style="width: 25em" />
    </div>
    <div class="row">
      <q-select v-model="employeeID" :options="['CLSD', 'CLID']" label="Employee ID" class="q-mr-sm" style="width: 126px;"/>
      <q-input v-model="employeeNumber" label="Employee Number" mask="####" />
    </div>
    <div class="row">
      <q-input v-model="employeeEmail" type="email" label="Email" />
    </div>
    <div class="row">
      <q-input v-model="title" label="Title" class="q-mr-sm" />
      <q-input v-model="fte" label="FTE" mask="#.##" />
    </div>
    <div class="row">
      <q-select v-model="salaryRange" :options="Array.from({length: 50}, (x, i) => i+1)" label="Salary Range" class="q-mr-sm" style="width: 131px;"/>
      <q-select v-model="salaryStep" :options="Array.from({length: 10}, (x, i) => i+1)" label="Salary Step" class="q-mr-sm" style="width: 131px;"/>
      <q-checkbox v-model="bilingual" label="Bilingual" />
    </div>
    <div class="row">
      <EmployeeSelect
        label="Manager"
        :employee="manager"
        v-on:input="manager=$event"
        v-on:clear="manager=emptyEmployee"
        class="q-mr-sm"
      />
      <UnitSelect
        label="Unit"
        :unit="unit"
        v-on:input="unit=$event"
        v-on:clear="unit=emptyUnit"
        class="q-mr-sm"
      />
    </div>
    <div class="row q-mt-md"><div v-if="type=='E'">End Date/Time</div><div v-else>Start Date/Time</div></div>
    <div class="row q-my-sm">
      <q-date
        v-model="transitionDate"
        mask="YYYY-MM-DD HH:mm"
        class="q-mr-md"
      />
      <q-time
        v-model="transitionDate"
        mask="YYYY-MM-DD HH:mm"
      />
    </div>

    <hr class="q-my-md" />
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
  AxiosEmployeeTransitionUpdateServerResponse, EmployeeTransition, VuexStoreGetters
} from '../../store/types'
import EmployeeSelect from '../../components/EmployeeSelect.vue'
import UnitSelect from 'src/components/UnitSelect.vue'

@Component({
  components: { EmployeeSelect, UnitSelect }
})
export default class EmployeeTransitionDetail extends Vue {
  private getters = this.$store.getters as VuexStoreGetters
  public emptyEmployee = {name: '', pk: -1}
  public emptyUnit = {name: '', pk: -1}

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
  public employeeIDCurrentVal = '' // TODO This should be EmployeeID
  public employeeID = '' // TODO This should be EmployeeID
  public employeeEmailCurrentVal = ''
  public employeeEmail = ''
  public titleCurrentVal = ''
  public title = ''
  public fteCurrentVal = ''
  public fte = ''
  public salaryRangeCurrentVal = ''
  public salaryRange = ''
  public salaryStepCurrentVal = ''
  public salaryStep = ''
  public bilingualCurrentVal = false
  public bilingual = false
  public managerCurrentVal = this.emptyEmployee
  public manager = this.emptyEmployee
  public unitCurrentVal = this.emptyUnit
  public unit = this.emptyUnit
  public transitionDateCurrentVal?: Date = new Date()
  public transitionDate?: Date = new Date()
  public preliminaryHireCurrentVal = false
  public preliminaryHire = false
  public deleteProfileCurrentVal = false
  public deleteProfile = false
  public officeLocationCurrentVal = ''
  public officeLocation = ''
  public cubicleNumberCurrentVal = ''
  public cubicleNumber = ''
  public unionAffiliationCurrentVal = ''
  public unionAffiliation = ''
  public teleworkingCurrentVal = false
  public teleworking = false
  public deskPhoneCurrentVal = false
  public deskPhone = false
  public currentPhoneCurrentVal = ''
  public currentPhone = ''
  public newPhoneCurrentVal = ''
  public newPhone = ''
  public loadCodeCurrentVal = ''
  public loadCode = ''
  public shouldDeleteCurrentVal = false
  public shouldDelete = false
  public reassignToCurrentVal = ''
  public reassignTo = ''
  public businessCardsCurrentVal = false
  public businessCards = false
  public proxCardNeededCurrentVal = false
  public proxCardNeeded = false
  public proxCardReturnedCurrentVal = false
  public proxCardReturned = false
  public accessEmailsCurrentVal = this.emptyEmployee
  public accessEmails = this.emptyEmployee
  public specialInstructionsCurrentVal = ''
  public specialInstructions = ''

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
    this.employeeID = t.employee_id
    this.employeeNumberCurrentVal = this.employeeNumber
    this.employeeIDCurrentVal = this.employeeID
    this.employeeEmail = t.employee_email
    this.employeeEmailCurrentVal = this.employeeEmail
    this.title = t.title
    this.titleCurrentVal = this.title
    this.fte = t.fte
    this.fteCurrentVal = this.fte
    this.salaryRange = t.salary_range
    this.salaryRangeCurrentVal = this.salaryRange
    this.salaryStep = t.salary_step
    this.salaryStepCurrentVal = this.salaryStep
    this.bilingual = t.bilingual
    this.bilingualCurrentVal = this.bilingual
    this.manager = {pk: t.manager_pk, name: t.manager_name}
    this.managerCurrentVal = this.manager
    this.unit = {pk: t.unit_pk, name: t.unit_name}
    this.unitCurrentVal = this.unit
    this.transitionDate = t.transition_date
    this.transitionDateCurrentVal = this.transitionDate
    this.preliminaryHire = t.preliminary_hire
    this.preliminaryHireCurrentVal = this.preliminaryHire
    this.deleteProfile = t.delete_profile
    this.deleteProfileCurrentVal = this.deleteProfile
    this.officeLocation = t.office_location
    this.officeLocationCurrentVal = this.officeLocation
    this.cubicleNumber = t.cubicle_number
    this.cubicleNumberCurrentVal = this.cubicleNumber
    this.unionAffiliation = t.union_affiliation
    this.unionAffiliationCurrentVal = this.unionAffiliation
    this.teleworking = t.teleworking
    this.teleworkingCurrentVal = this.teleworking
    this.deskPhone = t.desk_phone
    this.deskPhoneCurrentVal = this.deskPhone
    this.currentPhone = t.current_phone
    this.currentPhoneCurrentVal = this.currentPhone
    this.newPhone = t.new_phone
    this.newPhoneCurrentVal = this.newPhone
    this.loadCode = t.load_code
    this.loadCodeCurrentVal = this.loadCode
    this.shouldDelete = t.should_delete
    this.shouldDeleteCurrentVal = this.shouldDelete
    this.reassignTo = t.reassign_to
    this.reassignToCurrentVal = this.reassignTo
    this.businessCards = t.business_cards
    this.businessCardsCurrentVal = this.businessCards
    this.proxCardNeeded = t.prox_card_needed
    this.proxCardNeededCurrentVal = this.proxCardNeeded
    this.proxCardReturned = t.prox_card_returned
    this.proxCardReturnedCurrentVal = this.proxCardReturned
    this.accessEmails = {pk: t.access_emails_pk, name: t.access_emails_name}
    this.accessEmailsCurrentVal = this.accessEmails
    this.specialInstructions = t.special_instructions
    this.specialInstructionsCurrentVal = this.specialInstructions
    


    
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
      this.employeeEmail == this.employeeEmailCurrentVal &&
      this.title == this.titleCurrentVal &&
      this.fte == this.fteCurrentVal &&
      this.salaryRange == this.salaryRangeCurrentVal &&
      this.salaryStep == this.salaryStepCurrentVal &&
      this.bilingual == this.bilingualCurrentVal &&
      this.manager.pk == this.managerCurrentVal.pk &&
      this.unit.pk == this.unitCurrentVal.pk &&
      this.transitionDate == this.transitionDateCurrentVal &&
      this.preliminaryHire == this.preliminaryHireCurrentVal &&
      this.deleteProfile == this.deleteProfileCurrentVal &&
      this.officeLocation == this.officeLocationCurrentVal &&
      this.cubicleNumber == this.cubicleNumberCurrentVal &&
      this.unionAffiliation == this.unionAffiliationCurrentVal &&
      this.teleworking == this.teleworkingCurrentVal &&
      this.deskPhone == this.deskPhoneCurrentVal &&
      this.currentPhone == this.currentPhoneCurrentVal &&
      this.newPhone == this.newPhoneCurrentVal &&
      this.loadCode == this.loadCodeCurrentVal &&
      this.shouldDelete == this.shouldDeleteCurrentVal &&
      this.reassignTo == this.reassignToCurrentVal &&
      this.businessCards == this.businessCardsCurrentVal &&
      this.proxCardNeeded == this.proxCardNeededCurrentVal &&
      this.proxCardReturned == this.proxCardReturnedCurrentVal &&
      this.accessEmails == this.accessEmailsCurrentVal &&
      this.specialInstructions == this.specialInstructionsCurrentVal
    ) {
      return false
    } else {
      return true
    }
  }

  public updateTransition() {
    return new Promise((resolve, reject) => {
      EmployeeTransitionDataService.update(this.transitionPk, {
        type: this.type,
        
        submitter_pk: this.getters['userModule/getEmployeeProfile'].pk,
        
        employee_first_name: this.employeeFirstName,
        employee_middle_initial: this.employeeMiddleInitial,
        employee_last_name: this.employeeLastName,
        employee_preferred_name: this.employeePreferredName,
        employee_id: this.employeeID,
        employee_number: this.employeeNumber,
        employee_email: this.employeeEmail,
        title: this.title,
        fte: this.fte,
        salary_range: this.salaryRange,
        salary_step: this.salaryStep,
        bilingual: this.bilingual,
        manager_pk: this.manager.pk,
        unit_pk: this.unit.pk,
        transition_date: this.transitionDate,
        preliminary_hire: this.preliminaryHire,
        delete_profile: this.deleteProfile,
        office_location: this.officeLocation,
        cubicle_number: this.cubicleNumber,
        union_affiliation: this.unionAffiliation,
        teleworking: this.teleworking,
        desk_phone: this.deskPhone,
        current_phone: this.currentPhone,
        new_phone: this.newPhone,
        load_code: this.loadCode,
        should_delete: this.shouldDelete,
        reassign_to: this.reassignTo,
        business_cards: this.businessCards,
        prox_card_needed: this.proxCardNeeded,
        prox_card_returned: this.proxCardReturned,
        access_emails_pk: this.accessEmails.pk,
        special_instructions: this.specialInstructions
      })
      .then((response: AxiosEmployeeTransitionUpdateServerResponse) => {
        this.typeCurrentVal = response.data.type
        
        this.dateSubmitted = response.data.date_submitted
        this.submitterName = response.data.submitter_name

        this.employeeFirstNameCurrentVal = response.data.employee_first_name
        this.employeeMiddleInitialCurrentVal = response.data.employee_middle_initial
        this.employeeLastNameCurrentVal = response.data.employee_last_name
        this.employeePreferredNameCurrentVal = response.data.employee_preferred_name
        this.employeeIDCurrentVal = response.data.employee_id
        this.employeeNumberCurrentVal = response.data.employee_number
        this.employeeEmailCurrentVal = response.data.employee_email
        this.titleCurrentVal = response.data.title
        this.fteCurrentVal = response.data.fte
        this.salaryRangeCurrentVal = response.data.salary_range
        this.salaryStepCurrentVal = response.data.salary_step
        this.bilingualCurrentVal = response.data.bilingual
        this.managerCurrentVal = {pk: response.data.manager_pk, name: response.data.manager_name}
        this.unitCurrentVal = {pk: response.data.unit_pk, name: response.data.unit_name}
        this.transitionDateCurrentVal = response.data.transition_date
        this.preliminaryHireCurrentVal = response.data.preliminary_hire
        this.deleteProfileCurrentVal = response.data.delete_profile
        this.officeLocationCurrentVal = response.data.office_location
        this.cubicleNumberCurrentVal = response.data.cubicle_number
        this.unionAffiliationCurrentVal = response.data.union_affiliation
        this.teleworkingCurrentVal = response.data.teleworking
        this.deskPhoneCurrentVal = response.data.desk_phone
        this.currentPhoneCurrentVal = response.data.current_phone
        this.newPhoneCurrentVal = response.data.new_phone
        this.loadCodeCurrentVal = response.data.load_code
        this.shouldDeleteCurrentVal = response.data.should_delete
        this.reassignToCurrentVal = response.data.reassign_to
        this.businessCardsCurrentVal = response.data.business_cards
        this.proxCardNeededCurrentVal = response.data.prox_card_needed
        this.proxCardReturnedCurrentVal = response.data.prox_card_returned
        this.accessEmailsCurrentVal = {pk: response.data.access_emails_pk, name: response.data.access_emails_name}
        this.specialInstructionsCurrentVal = response.data.special_instructions

        // if (this.formErrorItems().length > 0) {
        //   this.showErrorButton = true
        // }

        this.$store.dispatch('workflowModule/getCurrentWorkflowInstance', {pk: this.$route.params.pk})
          .catch(e => {
            console.error('Error getting getCurrentWorkflowInstance after updaing EmployeeTransition:', e)
            reject(e)
          })

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

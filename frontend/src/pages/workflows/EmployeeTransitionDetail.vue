<template>
  <div class="q-pt-md">
    <div class="text-h6 transition-form-section-heading">Type</div>
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
    <div class="text-h6 transition-form-section-heading">Submission Info</div>
    <div class="row">
      <q-input v-model="dateSubmitted" label="Date Submitted" class="q-mr-md" disable />
      <q-input v-model="submitterName" label="Submitter" disable />
    </div>
    <div class="text-h6 transition-form-section-heading">Employee</div>
    <div class="row">
      <q-input v-model="employeeFirstName" label="First" class="q-mr-md" />
      <q-input v-model="employeeMiddleInitial" mask="A" label="M" class="q-mr-md" style="width: 1em" />
      <q-input v-model="employeeLastName" label="Last" class="q-mr-md" />
      <q-input v-model="employeePreferredName" label="Preferred Name, if different" style="width: 25em" />
    </div>
    <div class="row">
      <q-select
        v-model="employeeID"
        :options="['CLSD', 'CLID']"
        label="Employee ID"
        class="q-mr-sm"
        style="width: 130px;"
      >
        <template v-if="employeeID" v-slot:append>
          <q-icon name="cancel" @click.stop="employeeID=''" class="cursor-pointer" />
        </template>
      </q-select>
      <q-input v-model="employeeNumber" type="number" label="Employee Number" mask="####" class="q-mr-md" />
      <q-input v-model="employeeEmail" type="email" label="Email" />
    </div>
    <div class="text-h6 transition-form-section-heading">Position</div>
    <div class="row">
      <q-input v-model="title" label="Title" class="q-mr-md" />
      <q-input v-model="fte" label="FTE" mask="#.##" class="q-mr-md" />
      <q-checkbox v-model="bilingual" label="Bilingual" />
    </div>
    <div class="row">
      <q-select
        v-model="salaryRange"
        :options="Array.from({length: 50}, (x, i) => i+1)"
        label="Salary Range"
        class="q-mr-md"
        style="width: 133px;"
        clearable
      />
      <q-select
        v-model="salaryStep"
        :options="Array.from({length:10}, (x, i) => i+1)"
        label="Salary Step"
        class="q-mr-md"
        style="width: 131px;"
        clearable
      />
      <q-select
        v-model="unionAffiliation"
        :options="['Non-Represented','EA', 'SEIU', 'Management']"
        label="Union Affiliation"
        style="width: 172px;"
      >
        <template v-if="unionAffiliation" v-slot:append>
          <q-icon name="cancel" @click.stop="unionAffiliation=''" class="cursor-pointer" />
        </template>
      </q-select>
    </div>
    <div class="row">
      <EmployeeSelect
        label="Manager"
        :employee="manager"
        v-on:input="manager=$event"
        v-on:clear="manager=emptyEmployee"
        class="q-mr-md"
      />
      <UnitSelect
        label="Unit"
        :unit="unit"
        v-on:input="unit=$event"
        v-on:clear="unit=emptyUnit"
      />
    </div>
    <div class="text-h6 transition-form-section-heading">Work Details</div>
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
    <div class="row q-my-sm">
      <q-checkbox v-model="preliminaryHire" v-if="employeeID == 'CLSD'" label="Preliminary Hire" />
      <q-checkbox v-model="deleteProfile" label="Delete Profile" />
    </div>
    <div class="row">
      <q-select
        v-model="officeLocation"
        :options="[
          'Cottage Grove', 'Florence', 'Junction City', 'Oakridge', 'PPB - 4th Floor', 'PPB - 5th Floor',
          'Schaefers - Basement', 'Schaefers - 1st Floor', 'Schaefers - 2nd Floor', 'Schaefers - 3rd Floor',
          'Senior Meals Site', 'Veneta']"
        label="Office Location"
        class="q-mr-md"
        style="width: 193px;"
      >
        <template v-if="officeLocation" v-slot:append>
          <q-icon name="cancel" @click.stop="officeLocation=''" class="cursor-pointer" />
        </template>
      </q-select>
      <q-input v-model="cubicleNumber" type="number" label="Cubicle Number" mask="###" class="q-mr-md" />
      <q-checkbox v-model="teleworking" label="Teleworking" />
    </div>
    <div class="text-h6 transition-form-section-heading">Phone</div>
    <div class="row">
      <q-input
        v-model="currentPhone"
        type="tel"
        label="Phone Number"
        mask="(###) ###-####"
        fill-mask
        class="q-mr-md"
      />
      <q-checkbox v-model="deskPhone" label="Desk Phone Needed" class="q-mr-md" />
      <q-select
        v-model="phoneRequest"
        :options="[
          'New number needed', 'Remove phone', 'Delete number', 'Reassign to:',
          'Change name display to:', 'Delete voicemail box'
        ]"
        label="Phone Update"
        style="width: 218px;"
        class="q-mr-md"
      >
        <template v-if="phoneRequest" v-slot:append>
          <q-icon name="cancel" @click.stop="phoneRequest=''" class="cursor-pointer" />
        </template>
      </q-select>
      <q-input
        v-model="phoneRequestData"
        v-if="['Reassign to:', 'Change name display to:'].indexOf(phoneRequest) != -1"
        label="To whom?"
      />
    </div>
    <div class="row">
      <q-input
        v-model="loadCode"
        v-if="employeeID == 'CLSD'"
        label="Load Code"
      />
    </div>
    <div class="row">
      <q-checkbox v-model="shouldDelete" label="Delete?" />
    </div>
    <div class="row">
      <q-input
        v-model="reassignTo"
        label="Reassign to"
      />
    </div>
    <div class="row">
      <q-checkbox v-model="businessCards" label="Order Business Cards" />
    </div>
    <div class="text-h6 transition-form-section-heading">Proxy Card/Photo ID</div>
    <div class="row">
      <q-checkbox v-model="proxCardNeeded" label="Needed" />
      <q-checkbox v-model="proxCardReturned" label="Turned In" />
    </div>
    <div class="text-h6 transition-form-section-heading">Computer Profile</div>
    <div class="row">
      <div>
        Email account will be disabled (no incoming or outgoing emails) on End Date
        <span class="text-underline">unless otherwise specified in special instructions</span>.
      </div>
    </div>
    <div class="row">
      <q-checkbox
        v-model="showAccessEmails"
        label="Does someone need to access current emails?"
        class="q-mr-md" />
      <EmployeeSelect
        v-if="showAccessEmails"
        label="Who?"
        :employee="accessEmails"
        v-on:input="accessEmails=$event"
        v-on:clear="accessEmails=emptyEmployee"
        class="q-mr-md"
      />
    </div>
    <div class="text-h6 transition-form-section-heading">Special Instructions</div>
    <div class="row">
      <q-input v-model="specialInstructions" autogrow style="width:100%" />
    </div>

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
.text-underline {
  text-decoration: underline;
}
.transition-form-section-heading {
  border-bottom: 2px solid black;
  margin: 10px 0;
}
#sticky-footer {
  padding: 10px;
  background-color: rgb(25, 118, 210);
  position: fixed;
  bottom: 0;
  right: 0;
  left: 0;
  z-index: 2;

  .status {
    color: white;
  }
}
@media only screen and (min-width: 1024px) {
  #sticky-footer {
    left: 209px;
  }
}
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
  public salaryRangeCurrentVal: number | null = null
  public salaryRange: number | null = null
  public salaryStepCurrentVal: number | null = null
  public salaryStep: number | null = null
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
  public cubicleNumberCurrentVal: number | null = null
  public cubicleNumber: number | null = null
  public unionAffiliationCurrentVal = ''
  public unionAffiliation = ''
  public teleworkingCurrentVal = false
  public teleworking = false
  public currentPhoneCurrentVal = ''
  public currentPhone = ''
  public deskPhoneCurrentVal = false
  public deskPhone = false
  public phoneRequestCurrentVal = ''
  public phoneRequest = ''
  public phoneRequestDataCurrentVal = ''
  public phoneRequestData = ''
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
  public showAccessEmailsCurrentVal = false
  public showAccessEmails = false
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
    this.currentPhone = t.current_phone
    this.currentPhoneCurrentVal = this.currentPhone
    this.deskPhone = t.desk_phone
    this.deskPhoneCurrentVal = this.deskPhone
    this.phoneRequest = t.phone_request
    this.phoneRequestCurrentVal = this.phoneRequest
    this.phoneRequestData = t.phone_request_data
    this.phoneRequestDataCurrentVal = this.phoneRequestData
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
    if (t.access_emails_pk != -1) {
      this.showAccessEmails = true
      this.showAccessEmailsCurrentVal = true
    } 
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
      this.currentPhone == this.currentPhoneCurrentVal &&
      this.deskPhone == this.deskPhoneCurrentVal &&
      this.phoneRequest == this.phoneRequestCurrentVal &&
      this.phoneRequestData == this.phoneRequestDataCurrentVal &&
      this.loadCode == this.loadCodeCurrentVal &&
      this.shouldDelete == this.shouldDeleteCurrentVal &&
      this.reassignTo == this.reassignToCurrentVal &&
      this.businessCards == this.businessCardsCurrentVal &&
      this.proxCardNeeded == this.proxCardNeededCurrentVal &&
      this.proxCardReturned == this.proxCardReturnedCurrentVal &&
      this.showAccessEmails == this.showAccessEmailsCurrentVal &&
      this.accessEmails.pk == this.accessEmailsCurrentVal.pk &&
      this.specialInstructions == this.specialInstructionsCurrentVal
    ) {
      return false
    } else {
      return true
    }
  }

  public updateTransition() {
    return new Promise((resolve, reject) => {
      const currentPhoneVal = this.currentPhone == '(___) ___-____' ? '' : this.currentPhone
      if (['Reassign to:', 'Change name display to:'].indexOf(this.phoneRequest) == -1) {
        this.phoneRequestData = ''
      }
      if (!this.showAccessEmails) {
        this.accessEmails = this.emptyEmployee
      }
      
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
        current_phone: currentPhoneVal,
        desk_phone: this.deskPhone,
        phone_request: this.phoneRequest,
        phone_request_data: this.phoneRequestData,
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
        this.currentPhoneCurrentVal = response.data.current_phone
        this.deskPhoneCurrentVal = response.data.desk_phone
        this.phoneRequestCurrentVal = response.data.phone_request
        this.phoneRequestDataCurrentVal = response.data.phone_request_data
        this.loadCodeCurrentVal = response.data.load_code
        this.shouldDeleteCurrentVal = response.data.should_delete
        this.reassignToCurrentVal = response.data.reassign_to
        this.businessCardsCurrentVal = response.data.business_cards
        this.proxCardNeededCurrentVal = response.data.prox_card_needed
        this.proxCardReturnedCurrentVal = response.data.prox_card_returned
        this.showAccessEmailsCurrentVal = this.showAccessEmails
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

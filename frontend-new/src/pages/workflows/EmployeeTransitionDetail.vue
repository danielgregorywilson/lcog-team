<template>
  <div class="q-pt-md">
    <div class="text-h6 transition-form-section-heading">Type</div>
    <div class="row items-center">
      <q-radio v-model="type" val="New" disable />
      <div>New</div>
      <q-radio v-model="type" val="Return" disable />
      <div>Return</div>
      <q-radio v-model="type" val="Change/Modify" disable />
      <div>Change/Modify</div>
      <q-radio v-model="type" val="Exit" disable />
      <div>Exit</div>
    </div>
    <div class="text-h6 transition-form-section-heading">Submission Info</div>
    <div class="row">
      <q-input v-model="dateSubmitted" label="Date Submitted" class="q-mr-md" disable />
      <q-input v-model="submitterName" label="Submitter" disable />
    </div>
    <div class="text-h6 transition-form-section-heading">Employee</div>
    <div class="row">
      <q-input v-model="employeeFirstName" label="First" class="q-mr-md" @blur="suggestEmail()" />
      <q-input v-model="employeeMiddleInitial" maxlength=5 label="M" class="q-mr-md" style="width: 4em" />
      <q-input v-model="employeeLastName" label="Last" class="q-mr-md" @blur="suggestEmail()" />
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
      <JobTitleSelect
        label="Title"
        :title="title"
        v-on:input="title=$event"
        v-on:clear="title=emptyTitle"
        class="q-mr-md"
      />
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
    <div class="row q-mt-md"><div v-if="type=='Exit'">End Date/Time</div><div v-else>Start Date/Time</div></div>
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
      <q-checkbox v-if="type=='Exit'" v-model="deleteProfile" label="Delete Profile" />
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
    <div v-if="['New', 'Return'].indexOf(type) != -1">
      <div class="text-h6 transition-form-section-heading">Computer</div>
      <div class="row items-center" id="computer-type">
        <div class="q-gutter-sm q-mr-md">
          <q-radio v-model="computerType" val="New" label="New" />
          <q-radio v-model="computerType" val="Repurposed" label="Repurposed" />
        </div>
        <q-input v-if="computerType == 'New'" v-model="computerGL" label="GL Code" style="width: 250px;" />
        <q-input v-else v-model="computerDescription" label="Description of existing computer" style="width: 350px;" />
      </div>
      <div v-if="computerType == 'New'" class="row q-mt-sm" style="color: red">Note that new PCs take 2-4 weeks to order.</div>
    </div>
    <div class="text-h6 transition-form-section-heading">Phone</div>
    <div class="row">
      <q-input
        v-model="phoneNumber"
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
    <div v-if="type=='Exit'" class="row">
      <q-checkbox v-model="shouldDelete" label="Delete?" />
    </div>
    <div v-if="type=='Exit'" class="row">
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
      <q-checkbox v-if="type!='Exit'" v-model="proxCardNeeded" label="Needed" />
      <q-checkbox v-if="type=='Exit'" v-model="proxCardReturned" label="Turned In" />
    </div>
    <div v-if="type=='Exit'">
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
    </div>
    <div class="text-h6 transition-form-section-heading">Special Instructions</div>
    <div class="row">
      <q-input v-model="specialInstructions" autogrow style="width:100%" />
    </div>

    <!-- Dialog of all error items -->
    <q-dialog v-model="showErrorDialog" :position="errorDialogPosition">
      <q-card style="width: 350px">
        <q-list bordered separator>
          <q-item v-for="(item, index) in formErrorItems()" :key="index" clickable @click="clickedErrorItem(item)">
            <q-item-label>{{item[1]}}</q-item-label>
          </q-item>
        </q-list>
      </q-card>
    </q-dialog>

    <!-- Spacing for footer -->
    <div style="height: 80px;"></div>

    <div id="sticky-footer" class="row justify-between" v-if="true">
      <q-btn id="update-button" class="col-1" color="white" text-color="black" label="Submit" :disabled="!valuesAreChanged()" @click="updateTransitionAndClose()" />
      <q-btn v-if="showErrorButton && formErrorItems().length > 0" label="Show errors" icon="check" color="warning" @click="openErrorDialog('right')" />
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

<script setup lang="ts">
import { QDialogProps, scroll, useQuasar } from 'quasar'
import { useRoute, useRouter } from 'vue-router'
import { onMounted, ref, Ref, watch } from 'vue'

import useEventBus from 'src/eventBus'
import { EmployeeTransition } from 'src/types'
import EmployeeSelect from 'src/components/EmployeeSelect.vue'
import JobTitleSelect from 'src/components/JobTitleSelect.vue'
import UnitSelect from 'src/components/UnitSelect.vue'
import { useUserStore } from 'src/stores/user'
import { useWorkflowsStore } from 'src/stores/workflows'
import { getRoutePk } from 'src/utils'

const quasar = useQuasar()
const { getScrollTarget, setVerticalScrollPosition  } = scroll
const route = useRoute()
const router = useRouter()
const { bus } = useEventBus()
const userStore = useUserStore()
const workflowsStore = useWorkflowsStore()

const emptyEmployee = {name: '', pk: -1}
const emptyTitle = {name: '', pk: -1}
const emptyUnit = {name: '', pk: -1}

function currentEmployeeTransition(): EmployeeTransition {
  return workflowsStore.currentEmployeeTransition
}

let transitionPk = ref('')

let typeCurrentVal = ref('')
let type = ref('')
let dateSubmitted = ref(new Date())
let submitterName = ref('')
let employeeFirstNameCurrentVal = ref('')
let employeeFirstName = ref('')
let employeeMiddleInitialCurrentVal = ref('')
let employeeMiddleInitial = ref('')
let employeeLastNameCurrentVal = ref('')
let employeeLastName = ref('')
let employeePreferredNameCurrentVal = ref('')
let employeePreferredName = ref('')
let employeeNumberCurrentVal = ref('')
let employeeNumber = ref('')
let employeeIDCurrentVal = ref('') // TODO This should be EmployeeID
let employeeID = ref('') // TODO This should be EmployeeID
let employeeEmailCurrentVal = ref('')
let employeeEmail = ref('')
let titleCurrentVal = ref(emptyTitle)
let title = ref(emptyTitle)
let fteCurrentVal = ref('')
let fte = ref('')
let salaryRangeCurrentVal = ref(null) as Ref<number | null>
let salaryRange = ref(null) as Ref<number | null>
let salaryStepCurrentVal = ref(null) as Ref<number | null>
let salaryStep = ref(null) as Ref<number | null>
let bilingualCurrentVal = ref(false)
let bilingual = ref(false)
let managerCurrentVal = ref(emptyEmployee)
let manager = ref(emptyEmployee)
let unitCurrentVal = ref(emptyUnit)
let unit = ref(emptyUnit)
let transitionDateCurrentVal = ref(null) as Ref<string | null>
let transitionDate = ref(null) as Ref<string | null>
let preliminaryHireCurrentVal = ref(false)
let preliminaryHire = ref(false)
let deleteProfileCurrentVal = ref(false)
let deleteProfile = ref(false)
let officeLocationCurrentVal = ref('')
let officeLocation = ref('')
let cubicleNumberCurrentVal = ref(null) as Ref<number | null>
let cubicleNumber = ref(null) as Ref<number | null>
let unionAffiliationCurrentVal = ref('')
let unionAffiliation = ref('')
let teleworkingCurrentVal = ref(false)
let teleworking = ref(false)
let computerTypeCurrentVal = ref('')
let computerType = ref('')
let computerGLCurrentVal = ref('')
let computerGL = ref('')
let computerDescriptionCurrentVal = ref('')
let computerDescription = ref('')
let phoneNumberCurrentVal = ref('')
let phoneNumber = ref('')
let deskPhoneCurrentVal = ref(false)
let deskPhone = ref(false)
let phoneRequestCurrentVal = ref('')
let phoneRequest = ref('')
let phoneRequestDataCurrentVal = ref('')
let phoneRequestData = ref('')
let loadCodeCurrentVal = ref('')
let loadCode = ref('')
let shouldDeleteCurrentVal = ref(false)
let shouldDelete = ref(false)
let reassignToCurrentVal = ref('')
let reassignTo = ref('')
let businessCardsCurrentVal = ref(false)
let businessCards = ref(false)
let proxCardNeededCurrentVal = ref(false)
let proxCardNeeded = ref(false)
let proxCardReturnedCurrentVal = ref(false)
let proxCardReturned = ref(false)
let showAccessEmailsCurrentVal = ref(false)
let showAccessEmails = ref(false)
let accessEmailsCurrentVal = ref(emptyEmployee)
let accessEmails = ref(emptyEmployee)
let specialInstructionsCurrentVal = ref('')
let specialInstructions = ref('')

let showErrorButton = ref(false)
let showErrorDialog = ref(false)
let errorDialogPosition = ref('top') as Ref<QDialogProps['position']>

function retrieveEmployeeTransition() {
  const t = currentEmployeeTransition()
  transitionPk.value = t.pk.toString()
  
  type.value = t.type
  typeCurrentVal.value = type.value

  dateSubmitted.value = t.date_submitted
  submitterName.value = t.submitter_name

  employeeFirstName.value = t.employee_first_name
  employeeFirstNameCurrentVal.value = employeeFirstName.value
  employeeMiddleInitial.value = t.employee_middle_initial
  employeeMiddleInitialCurrentVal.value = employeeMiddleInitial.value
  employeeLastName.value = t.employee_last_name
  employeeLastNameCurrentVal.value = employeeLastName.value
  employeePreferredName.value = t.employee_preferred_name
  employeePreferredNameCurrentVal.value = employeePreferredName.value
  employeeNumber.value = t.employee_number
  employeeID.value = t.employee_id
  employeeNumberCurrentVal.value = employeeNumber.value
  employeeIDCurrentVal.value = employeeID.value
  employeeEmail.value = t.employee_email
  employeeEmailCurrentVal.value = employeeEmail.value
  title.value = {pk: t.title_pk, name: t.title_name}
  titleCurrentVal.value = title.value
  fte.value = t.fte
  fteCurrentVal.value = fte.value
  salaryRange.value = t.salary_range
  salaryRangeCurrentVal.value = salaryRange.value
  salaryStep.value = t.salary_step
  salaryStepCurrentVal.value = salaryStep.value
  bilingual.value = t.bilingual
  bilingualCurrentVal.value = bilingual.value
  manager.value = {pk: t.manager_pk, name: t.manager_name}
  managerCurrentVal.value = manager.value
  unit.value = {pk: t.unit_pk, name: t.unit_name}
  unitCurrentVal.value = unit.value
  if (t.transition_date === null) {
    transitionDate.value = null
  } else {
    transitionDate.value = t.transition_date.replace('T', ' ')
  }
  transitionDateCurrentVal.value = transitionDate.value
  preliminaryHire.value = t.preliminary_hire
  preliminaryHireCurrentVal.value = preliminaryHire.value
  deleteProfile.value = t.delete_profile
  deleteProfileCurrentVal.value = deleteProfile.value
  officeLocation.value = t.office_location
  officeLocationCurrentVal.value = officeLocation.value
  cubicleNumber.value = t.cubicle_number
  cubicleNumberCurrentVal.value = cubicleNumber.value
  unionAffiliation.value = t.union_affiliation
  unionAffiliationCurrentVal.value = unionAffiliation.value
  teleworking.value = t.teleworking
  teleworkingCurrentVal.value = teleworking.value
  computerType.value = t.computer_type
  computerTypeCurrentVal.value = computerType.value
  computerGL.value = t.computer_gl
  computerGLCurrentVal.value = computerGL.value
  computerDescription.value = t.computer_description
  computerDescriptionCurrentVal.value = computerDescription.value
  phoneNumber.value = t.phone_number
  phoneNumberCurrentVal.value = phoneNumber.value
  deskPhone.value = t.desk_phone
  deskPhoneCurrentVal.value = deskPhone.value
  phoneRequest.value = t.phone_request
  phoneRequestCurrentVal.value = phoneRequest.value
  phoneRequestData.value = t.phone_request_data
  phoneRequestDataCurrentVal.value = phoneRequestData.value
  loadCode.value = t.load_code
  loadCodeCurrentVal.value = loadCode.value
  shouldDelete.value = t.should_delete
  shouldDeleteCurrentVal.value = shouldDelete.value
  reassignTo.value = t.reassign_to
  reassignToCurrentVal.value = reassignTo.value
  businessCards.value = t.business_cards
  businessCardsCurrentVal.value = businessCards.value
  proxCardNeeded.value = t.prox_card_needed
  proxCardNeededCurrentVal.value = proxCardNeeded.value
  proxCardReturned.value = t.prox_card_returned
  proxCardReturnedCurrentVal.value = proxCardReturned.value
  if (t.access_emails_pk != -1) {
    showAccessEmails.value = true
    showAccessEmailsCurrentVal.value = true
  } 
  accessEmails.value = {pk: t.access_emails_pk, name: t.access_emails_name}
  accessEmailsCurrentVal.value = accessEmails.value
  specialInstructions.value = t.special_instructions
  specialInstructionsCurrentVal.value = specialInstructions.value
  
  if (formErrorItems().length > 0) {
    showErrorButton.value = true
  }

  
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

function suggestEmail(): void {
  if (employeeFirstName.value && employeeLastName.value && !employeeEmail.value) {
    employeeEmail.value = `${employeeFirstName.value.charAt(0).toLowerCase()}${employeeLastName.value.toLowerCase()}@lcog.org`
  }
}

function valuesAreChanged(): boolean { 
  if (
    type.value == typeCurrentVal.value &&
    employeeFirstName.value == employeeFirstNameCurrentVal.value &&
    employeeMiddleInitial.value == employeeMiddleInitialCurrentVal.value &&
    employeeLastName.value == employeeLastNameCurrentVal.value &&
    employeePreferredName.value == employeePreferredNameCurrentVal.value &&
    employeeID.value == employeeIDCurrentVal.value &&
    employeeNumber.value == employeeNumberCurrentVal.value &&
    employeeEmail.value == employeeEmailCurrentVal.value &&
    title.value.pk == titleCurrentVal.value.pk &&
    fte.value == fteCurrentVal.value &&
    salaryRange.value == salaryRangeCurrentVal.value &&
    salaryStep.value == salaryStepCurrentVal.value &&
    bilingual.value == bilingualCurrentVal.value &&
    manager.value.pk == managerCurrentVal.value.pk &&
    unit.value.pk == unitCurrentVal.value.pk &&
    transitionDate.value == transitionDateCurrentVal.value &&
    preliminaryHire.value == preliminaryHireCurrentVal.value &&
    deleteProfile.value == deleteProfileCurrentVal.value &&
    officeLocation.value == officeLocationCurrentVal.value &&
    cubicleNumber.value == cubicleNumberCurrentVal.value &&
    unionAffiliation.value == unionAffiliationCurrentVal.value &&
    teleworking.value == teleworkingCurrentVal.value &&
    computerType.value == computerTypeCurrentVal.value &&
    computerGL.value == computerGLCurrentVal.value &&
    computerDescription.value == computerDescriptionCurrentVal.value &&
    phoneNumber.value == phoneNumberCurrentVal.value &&
    deskPhone.value == deskPhoneCurrentVal.value &&
    phoneRequest.value == phoneRequestCurrentVal.value &&
    phoneRequestData.value == phoneRequestDataCurrentVal.value &&
    loadCode.value == loadCodeCurrentVal.value &&
    shouldDelete.value == shouldDeleteCurrentVal.value &&
    reassignTo.value == reassignToCurrentVal.value &&
    businessCards.value == businessCardsCurrentVal.value &&
    proxCardNeeded.value == proxCardNeededCurrentVal.value &&
    proxCardReturned.value == proxCardReturnedCurrentVal.value &&
    showAccessEmails.value == showAccessEmailsCurrentVal.value &&
    accessEmails.value.pk == accessEmailsCurrentVal.value.pk &&
    specialInstructions.value == specialInstructionsCurrentVal.value
  ) {
    return false
  } else {
    return true
  }
}

function formErrorItems(): Array<[string, string]> {
  let errorItems: Array<[string, string]> = []
  if (computerTypeCurrentVal.value == 'New' && !computerGLCurrentVal.value) {
    errorItems.push(['computer-type', 'Provide a valid GL code for computer purchase'])
  }
  if (computerTypeCurrentVal.value == 'Repurposed' && !computerDescriptionCurrentVal.value) {
    errorItems.push(['computer-type', 'Provide a description of existing computer'])
  }
  
  // if (!this.stepIncreaseCurrentVal) {
  //   errorItems.push(['step-increase', 'Select Step Increase'])
  // }
  // if (this.descriptionReviewedEmployeeCurrentVal && !this.uploadedPositionDescriptionUrl) {
  //   errorItems.push(['position-description-review', 'Upload Signed Position Description'])
  // }
  return errorItems
}

function updateTransitionAndClose() {
  return new Promise((resolve, reject) => {
    const phoneNumberVal = phoneNumber.value == '(___) ___-____' ? '' : phoneNumber.value
    if (['Reassign to:', 'Change name display to:'].indexOf(phoneRequest.value) == -1) {
      phoneRequestData.value = ''
    }
    if (!showAccessEmails.value) {
      accessEmails.value = emptyEmployee
    }
    let transitionDateSubmission = new Date()
    if (transitionDate.value) {
      transitionDateSubmission = new Date(transitionDate.value)
    }
    workflowsStore.updateEmployeeTransition(transitionPk.value, {
      type: type.value,
      submitter_pk: userStore.getEmployeeProfile.employee_pk,
      employee_first_name: employeeFirstName.value,
      employee_middle_initial: employeeMiddleInitial.value,
      employee_last_name: employeeLastName.value,
      employee_preferred_name: employeePreferredName.value,
      employee_id: employeeID.value,
      employee_number: employeeNumber.value,
      employee_email: employeeEmail.value,
      title_pk: title.value.pk,
      fte: fte.value,
      salary_range: salaryRange.value,
      salary_step: salaryStep.value,
      bilingual: bilingual.value,
      manager_pk: manager.value.pk,
      unit_pk: unit.value.pk,
      transition_date: transitionDateSubmission,
      preliminary_hire: preliminaryHire.value,
      delete_profile: deleteProfile.value,
      office_location: officeLocation.value,
      cubicle_number: cubicleNumber.value,
      union_affiliation: unionAffiliation.value,
      teleworking: teleworking.value,
      computer_type: computerType.value,
      computer_gl: computerGL.value,
      computer_description: computerDescription.value,
      phone_number: phoneNumberVal,
      desk_phone: deskPhone.value,
      phone_request: phoneRequest.value,
      phone_request_data: phoneRequestData.value,
      load_code: loadCode.value,
      should_delete: shouldDelete.value,
      reassign_to: reassignTo.value,
      business_cards: businessCards.value,
      prox_card_needed: proxCardNeeded.value,
      prox_card_returned: proxCardReturned.value,
      access_emails_pk: accessEmails.value.pk,
      special_instructions: specialInstructions.value
    })
    .then((t) => {
      typeCurrentVal.value = t.type
      
      dateSubmitted.value = t.date_submitted
      submitterName.value = t.submitter_name

      employeeFirstNameCurrentVal.value = t.employee_first_name
      employeeMiddleInitialCurrentVal.value = t.employee_middle_initial
      employeeLastNameCurrentVal.value = t.employee_last_name
      employeePreferredNameCurrentVal.value = t.employee_preferred_name
      employeeIDCurrentVal.value = t.employee_id
      employeeNumberCurrentVal.value = t.employee_number
      employeeEmailCurrentVal.value = t.employee_email
      titleCurrentVal.value = {pk: t.title_pk, name: t.title_name}
      fteCurrentVal.value = t.fte
      salaryRangeCurrentVal.value = t.salary_range
      salaryStepCurrentVal.value = t.salary_step
      bilingualCurrentVal.value = t.bilingual
      managerCurrentVal.value = {pk: t.manager_pk, name: t.manager_name}
      unitCurrentVal.value = {pk: t.unit_pk, name: t.unit_name}
      transitionDateCurrentVal.value = t.transition_date
      preliminaryHireCurrentVal.value = t.preliminary_hire
      deleteProfileCurrentVal.value = t.delete_profile
      officeLocationCurrentVal.value = t.office_location
      cubicleNumberCurrentVal.value = t.cubicle_number
      unionAffiliationCurrentVal.value = t.union_affiliation
      teleworkingCurrentVal.value = t.teleworking
      computerTypeCurrentVal.value = t.computer_type
      computerGLCurrentVal.value = t.computer_gl
      computerDescriptionCurrentVal.value = t.computer_description
      phoneNumberCurrentVal.value = t.phone_number
      deskPhoneCurrentVal.value = t.desk_phone
      phoneRequestCurrentVal.value = t.phone_request
      phoneRequestDataCurrentVal.value = t.phone_request_data
      loadCodeCurrentVal.value = t.load_code
      shouldDeleteCurrentVal.value = t.should_delete
      reassignToCurrentVal.value = t.reassign_to
      businessCardsCurrentVal.value = t.business_cards
      proxCardNeededCurrentVal.value = t.prox_card_needed
      proxCardReturnedCurrentVal.value = t.prox_card_returned
      showAccessEmailsCurrentVal.value = showAccessEmails.value
      accessEmailsCurrentVal.value = {pk: t.access_emails_pk, name: t.access_emails_name}
      specialInstructionsCurrentVal.value = t.special_instructions

      const routePk = getRoutePk(route)
      if (routePk) {
        workflowsStore.getCurrentWorkflowInstance(routePk)
          .catch(e => {
            console.error('Error getting getCurrentWorkflowInstance after updaing EmployeeTransition:', e)
            reject(e)
          })
      }

      if (formErrorItems().length > 0) {
        showErrorButton.value = true
      } else {
        router.push({ name: 'workflow-dashboard' })
      }

      // TODO: If a new computer is required, send an email to the IT department

      if (!!t.title_name) {
        quasar.notify(`Updated Employee Transition for ${t.title_name} Position`)
      } else {
        quasar.notify('Updated Employee Transition')
      }
      resolve('Updated')
    })
    .catch(e => {
      console.error('Error updating Employee Transition', e)
      quasar.notify({
        message: 'Error updating Employee Transition',
        color: 'negative',
        icon: 'report_problem'
      })
      reject(e)
    })
  })
}

function openErrorDialog(position: QDialogProps['position']) {
  errorDialogPosition.value = position
  showErrorDialog.value = true
}

function clickedErrorItem(item: [string, string]) {
  showErrorDialog.value = false
  const element = document.getElementById(item[0])
  if (!!element) {
    const target = getScrollTarget(element)
    const offset = element.offsetTop - 50
    const duration = 500
    setVerticalScrollPosition(target, offset, duration)
  }
}

watch(() => bus.value.get('workflowInstanceRetrieved'), () => {
  // TODO: We should only set state once, but when yoyu load /transition this runs twice
  retrieveEmployeeTransition()
})

onMounted(() => {
  retrieveEmployeeTransition()
})
</script>

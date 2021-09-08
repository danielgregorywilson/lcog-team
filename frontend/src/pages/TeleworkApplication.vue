<template>
  <q-page>
    <div class="q-pa-xl">
      <form>
        <div class="text-h4 text-center">APPLICATION FOR PROPOSED TELEWORK</div>
        <div class="row items-center q-gutter-md q-mt-sm">
          <div>Date:</div>
          <div style="max-width: 300px">
            <q-input filled v-model="date" mask="date" :rules="['date']">
              <template v-slot:append>
                <q-icon name="event" class="cursor-pointer">
                  <q-popup-proxy ref="qDateProxy" transition-show="scale" transition-hide="scale">
                    <q-date v-model="date">
                      <div class="row items-center justify-end">
                        <q-btn v-close-popup label="Close" color="primary" flat />
                      </div>
                    </q-date>
                  </q-popup-proxy>
                </q-icon>
              </template>
            </q-input>
          </div>
        </div>
        <div>
          As per LCOG’s Telework Policy, <strong>{{ employeeName }}</strong> (“employee”) and <strong>{{ managerName }}</strong> (“manager”) have discussed the suitability of a Telework arrangement.  The manager has considered, among other issues, LCOG’s operational needs; that the employee has demonstrated satisfactory working habits; the employee’s needs and work habits; whether the job performed by the employee is appropriate for Telework; equipment and technology needs (including the manager consulting with Information Services); workspace considerations; and scheduling issues.  The employee and manager have completed the attached proposed Telework Agreement.
        </div>
        <div class="q-mt-sm">This Application now is forwarded to <strong>{{ programManagerName }}</strong> (“Program Manager”).</div>
        <div class="q-mt-lg">
          Program Manager:
          <div class="q-gutter-sm">
            <q-radio v-model="programManagerApprove" val="approve" label="Approve" />
            <q-radio v-model="programManagerApprove" val="not-approve" label="Does not approve" />
          </div>
        </div>
        <div>Signature and date ___________________________________</div>
        <div class="q-mt-lg">If the Program Manager approves this Application, the proposed Telework Agreement then will be signed by the employee, manager, Program Manager, and Division Director.  The manager then will set a date for the employee to begin Telework that meets operational needs.</div>
        <div class="q-mt-sm">If the Program Manager does not approve this application, they will explain their reasoning in writing to the employee and the manager.  The employee then may present a written request appealing that decision to the Division Director, who will make their decision within ten working days.  If the Division Director does not approve this application, they will explain their reasoning in writing to the employee, manager, and Program Manager.  The employee then may present a written request appealing that decision to the Executive Director, who will make their decision within ten working days.  If the Executive Director does not approve this application, they will explain their reasoning in writing to the employee, manager, Program Manager, and Division Director.  The final decision cannot be grieved.</div>
        <div class="q-mt-sm">If at each succeeding level of management (Division Director or Executive Director), the application is approved, then the proposed Telework Agreement will be signed by the employee, manager, Program Manager, and Division Director.  The manager then will set a date for the employee to begin Telework that meets operational needs.</div>

  
        <div class="text-h4 text-center q-mt-xl">TELEWORK AGREEMENT</div>
        <div class="text-h5 text-center">FOR THE LANE COUNCIL OF GOVERNMENTS (LCOG)</div>
        <div class="q-mt-md">This Agreement is entered into between LCOG and <strong>{{ employeeName }}</strong> (“Employee”). This Agreement takes effect only upon the signature of the Program Manager and Division Director.</div>
        <div class="q-mt-sm">This Telework Agreement starts on __________________ and will remain in effect for three months unless LCOG or Employee determines that the Telework Agreement should end earlier, for any reason.  If the Agreement remains in effect for three months, and if employee has performed to their manager’s satisfaction as a teleworker, this Agreement may be extended until and when either LCOG or employee decides to end the Agreement.  The availability of Telework can be discontinued at any time at LCOG’s discretion.</div>

        <div class="text-h6 q-mt-md">Location and Schedule</div>
        <ul>
          <li>
            <div>Days and hours when Employee is expected to be onsite at LCOG’s regular place of business:</div>
            <q-input
              filled
              input-class="hours-onsite"
              v-model="hoursOnsite"
              type="textarea"
            />
          </li>
          <li>
            <div>Description about Employee’s primary Telework work site location:</div>
            <q-input
              filled
              input-class="telework-location"
              v-model="teleworkLocation"
              type="textarea"
            />
          </li>
          <li>
            <div>Days and hours when Employee will normally work at their Telework work site, along with break times (if applicable, for FLSA non-exempt employees):</div>
            <q-input
              filled
              input-class="hours-working"
              v-model="hoursWorking"
              type="textarea"
            />
          </li>
        </ul>
        
        <div class="text-h6 q-mt-md">Duties</div>
        <div class="q-mt-sm">
          <div>The duties and assignments authorized to be performed at this alternate work site include:</div>
          <q-input
            filled
            input-class="duties"
            v-model="duties"
            type="textarea"
          />
        </div>
        <div class="q-mt-sm text-italic">Note: Management reserves the right to assign work as necessary at any work site at any time as long as doing so is in line with any applicable collective bargaining agreement and state and federal laws.</div>
        <div class="q-mt-sm">Employee understands that they are required to accurately record all hours they work on their time sheets on a daily basis. <strong>Employee further understands and agrees that they may not work any overtime hours without first getting permission to do so from their manager.</strong></div>

        <div class="text-h6 q-mt-md">Communication</div>
        <div class="q-mt-sm">Specify the appropriate methods and times of communications including:</div>
        <ul>
          <li class="row items-center">
            <div class="col-md-1 col-xs-2 text-center">When:</div>
            <q-input filled v-model="communicationWhen" class="col" />
          </li>
          <li class="row items-center q-mt-xs">
            <div class="col-md-1 col-xs-2 text-center">Time:</div>
            <q-input filled v-model="communicationTime" class="col q-mt-xs" />
          </li>
          <li class="row items-center q-mt-xs">
            <div class="col-md-1 col-xs-2 text-center">How:</div>
            <q-input filled v-model="communicationHow" class="col q-mt-xs" label="e.g. phone, text, face-to-face, etc." />  
          </li>
        </ul>
        <div class="q-mt-sm text-italic"><strong>Employee agrees to remain accessible during all designated work hours.</strong></div>

        <div class="text-h6 q-mt-md">Computer Equipment and Security</div>
        <ul>
          <li>The manager has consulted with the Information Services Department (“IS”) to ensure that the employee has the technology capability to Telework.</li>
          <li>Employee will use the LCOG-provided equipment checked off below, plus IS services as needed, to perform job functions from the Telework site.</li>
          <li>Employee will be responsible for any other equipment required to perform their work. LCOG reserves the right to make determinations as to appropriate equipment, subject to change at any time.</li>
          <li>Employee may be held liable for damage caused by negligence, intentional damage, or damage resulting from a power surge if no surge protector is used.</li>
          <li>Employee shall promptly notify their manager when unable to perform work assignments due to the equipment failure or other unforeseen circumstances.</li>
          <li>Employee is expected to work with their manager and IS to ensure that LCOG information will be safeguarded on the computer, including how the information is stored and secured and the use of necessary virus protection software.</li>
          <li>For all LCOG-provided equipment, LCOG will be responsible for all maintenance, repairs, and replacement of the equipment.  However, the IS department will not make house calls.  If employee has an issue with the computer, software, or any other equipment or service provided by LCOG, employee will need to bring it to the main office for diagnosis and repair.</li>
          <li>The security of LCOG property at the Telework site is as important as it is in the office.  Telework employees are expected to take reasonable precautions to protect LCOG equipment from theft, damage, or misuse.</li>
          <li>LCOG accepts no responsibility for damage or repairs to employee-owned equipment.  Employee will be responsible for taking all necessary action to protect LCOG’s equipment against damage or theft.</li>
          <li>Employee may not use the computer equipment, software, or other technology provided to employee for Telework for personal use or allow non-LCOG employees to use the equipment.</li>
        </ul>

        <div class="q-mt-sm text-italic">LCOG Equipment to be provided to employee:</div>

        <div class="q-mt-sm">This is based on the employee’s manager’s determination of what is needed at the telework location (check all that apply):</div>
        <q-checkbox v-model="equipmentProvidedPhone" val="cell-phone" label="Cell Phone" />
        <q-checkbox v-model="equipmentProvidedLaptop" val="laptop" label="Laptop" />
        <q-checkbox v-model="equipmentProvidedDesktop" val="desktop" label="Desktop Computer" />
        <q-checkbox v-model="equipmentProvidedMonitor" val="monitor" label="Monitor" />
        <q-checkbox v-model="equipmentProvidedAccess" val="remote-access" label="Remote Network Access" />
        <q-checkbox v-model="equipmentProvidedOther" val="other" label="Other" />
        <q-input dense filled v-if="equipmentProvidedOther" v-model="equipmentProvidedOtherValue" class="q-pl-sm"/>

        <div class="text-h6 q-mt-md">Safety and Accidents</div>
        <ul>
          <li>Employee will immediately report all accidents using the Incident Report form, located on the Intranet under “Forms.”  If medical attention is sought, employee will contact Human Resources (HR) as soon as possible and complete a Workers’ Compensation form.</li>
          <li>Employee agrees to maintain a safe and secure work environment. To ensure that safe working conditions exist, LCOG has the right to visit an employee’s telework site during normal work hours to ensure that it meets LCOG safety standards; such visits will be scheduled with at least twenty-four (24) hours advance notice, if possible.</li>
          <li>The following Safety Checklist must be completed prior to any Telework activity governed by this policy.  Any questions about the safety of a telework site should be referred to Human Resources.</li>
        </ul>

        <div class="text-h5 text-center q-mt-md">TELEWORK SAFETY CHECKLIST</div>
        <div class="q-mt-sm">This checklist is used to assess the overall safety of the Telework location.</div>

        <div class="text-h6 q-mt-sm">THE DESIGNATED WORK SPACE:</div>
        <ol>
          <li>Are LCOG computers and other equipment plugged into surge protectors?
            <q-option-group
              :options="yesNoOptions"
              type="radio"
              v-model="workspaceChecklist1"
              inline
            />
          </li>
          <li class="q-mt-md">Are temperature, noise, ventilation, and lighting levels adequate for maintaining your normal level of performance?
            <q-option-group
              :options="yesNoOptions"
              type="radio"
              v-model="workspaceChecklist2"
              inline
            />
          </li>
          <li class="q-mt-md">Are all supplies and equipment (both LCOG and employee-owned) in good condition and can be safely used as intended?
            <q-option-group
              :options="yesNoOptions"
              type="radio"
              v-model="workspaceChecklist3"
              inline
            />
          </li>
          <li class="q-mt-md">Is storage organized to minimize risks of fires and spontaneous combustion?
            <q-option-group
              :options="yesNoOptions"
              type="radio"
              v-model="workspaceChecklist4"
              inline
            />
          </li>
          <li class="q-mt-md">Do all electrical enclosures (switches, outlets, receptacles, junction boxes) affecting the designated work area have tight fitting covers or plates?
            <q-option-group
              :options="yesNoOptions"
              type="radio"
              v-model="workspaceChecklist5"
              inline
            />
          </li>
          <li class="q-mt-md">Is all electrical equipment free of recognized hazards that would cause physical harm (frayed wires, bare conductors, loose wires or fixtures, exposed wiring on the ceiling or walls)?
            <q-option-group
              :options="yesNoOptions"
              type="radio"
              v-model="workspaceChecklist6"
              inline
            />
          </li>
          <li class="q-mt-md">Will the building’s electrical system permit the grounding of electrical equipment (a three-prong receptacle)?
            <q-option-group
              :options="yesNoOptions"
              type="radio"
              v-model="workspaceChecklist7"
              inline
            />
          </li>
          <li class="q-mt-md">Are aisles, doorways, and corners free from obstructions to permit visibility and movement?
            <q-option-group
              :options="yesNoOptions"
              type="radio"
              v-model="workspaceChecklist8"
              inline
            />
          </li>
          <li class="q-mt-md">Are the file cabinets and storage closets arranged so drawers and doors do not enter walkways?
            <q-option-group
              :options="yesNoOptions"
              type="radio"
              v-model="workspaceChecklist9"
              inline
            />
          </li>
          <li class="q-mt-md">Are heavy items, such as computer monitors and printers, securely placed on sturdy stands close to walls?
            <q-option-group
              :options="yesNoOptions"
              type="radio"
              v-model="workspaceChecklist10"
              inline
            />
          </li>
          <li class="q-mt-md">Are phone lines, electrical cords, and surge protectors secured under a desk or along a baseboard?
            <q-option-group
              :options="yesNoOptions"
              type="radio"
              v-model="workspaceChecklist11"
              inline
            />
          </li>
          <li class="q-mt-md">Are computer components kept out of direct sunlight and away from heaters?
            <q-option-group
              :options="yesNoOptions"
              type="radio"
              v-model="workspaceChecklist12"
              inline
            />
          </li>
        </ol>

        <div class="text-h6">EMERGENCY PREPAREDNESS:</div>
        <ol>
          <li>Are emergency phone numbers (911, nearest hospital, fire department, police department, etc.) posted in the telework work space?
            <q-option-group
                :options="yesNoOptions"
                type="radio"
                v-model="emergencyChecklist1"
                inline
              />
          </li>
          <li class="q-mt-md">Is a first aid kit accessible and periodically inspected and replenished as needed?
            <q-option-group
                :options="yesNoOptions"
                type="radio"
                v-model="emergencyChecklist2"
                inline
              />
          </li>
          <li class="q-mt-md">In case of fire, is there a primary exit free of obstruction and easy to use?
            <q-option-group
                :options="yesNoOptions"
                type="radio"
                v-model="emergencyChecklist3"
                inline
              />
          </li>
        </ol>

        <div class="text-h6">ERGONOMICS:</div>
        <ol>
          <li>Are your desk, chair, computer, and other equipment of appropriate design and arranged so that:
            <ol type="a" class="q-mt-md">
              <li>Neck and shoulders are not stooped to view the task?
                <q-option-group
                  :options="yesNoOptions"
                  type="radio"
                  v-model="ergonomicsChecklist1"
                  inline
                />
              </li>
              <li>There are not pressure points on any part of the body (wrists, forearms, back of legs)?
                <q-option-group
                  :options="yesNoOptions"
                  type="radio"
                  v-model="ergonomicsChecklist2"
                  inline
                />
              </li>
              <li>There is no glare on the computer screen?
                <q-option-group
                  :options="yesNoOptions"
                  type="radio"
                  v-model="ergonomicsChecklist3"
                  inline
                />
              </li>
              <li>Work can be performed without eye strain?
                <q-option-group
                  :options="yesNoOptions"
                  type="radio"
                  v-model="ergonomicsChecklist4"
                  inline
                />
              </li>
              <li>There is no strain on any part of the body for static tasks over 20 minutes?
                <q-option-group
                  :options="yesNoOptions"
                  type="radio"
                  v-model="ergonomicsChecklist5"
                  inline
                />
              </li>
            </ol>
          </li>
        </ol>

        <div class="q-mt-sm">
          <div>Teleworker comments after the inspection (if any):</div>
          <q-input
            filled
            input-class="teleworker-comments"
            v-model="teleworkerComments"
            type="textarea"
          />  
        </div>
        <div class="q-mt-sm">
          <div>Manager comments regarding the Safety Checklist (if any):</div>
          <q-input
            filled
            input-class="manager-comments"
            v-model="managerComments"
            type="textarea"
          />  
        </div>

        <div class="text-h6 q-mt-lg">ACKNOWLEDGEMENT:</div>
        <div class="text-italic q-mt-sm">I have completed the checklist accurately and honestly to the best of my knowledge.  I understand that I have the right to ask questions, or to have additional training provided.</div>
        <div class="text-italic q-mt-sm">I agree to abide by and operate in accordance with the terms and conditions described in this document.  I agree that the sole purpose of this Agreement is to regulate Telework and that it constitutes neither an employment contract nor an amendment to any existing contract or LCOG policy.</div>
        <div class="q-mt-sm">Employee __________________________________________		Date ___________________</div>


        <div class="text-h6 q-mt-lg">Reimbursable Expenses</div>
        <div class="q-mt-sm">LCOG will reimburse the employee for the following expenses:</div>
        <ul>
          <li>Business telephone calls, unless other arrangements, such as a cell phone stipend, have been provided.</li>
          <li>Other expenses pre-authorized by the employee’s manager.</li>
        </ul>
        <div class="q-mt-sm">LCOG will not reimburse for the following:</div>
        <ul>
          <li>Basic office supplies, such as paper, pens, and fax or computer paper.</li>
          <li>Any costs related to remodeling and furnishing the Telework space.</li>
          <li>Costs related to internet access, including equipment.</li>
          <li>Telework site expenses and utility costs.</li>
          <li>Costs related to commuting to the primary business location from a Telework site.</li>
        </ul>

        <div class="text-h6 q-mt-md">Privacy</div>
        <div class="q-mt-sm">Employee understands that usage of their personal property is subject to public records law, as well as other state and federal laws, such as Health Insurance Portability and Accountability Act (HIPAA), that may require the employee to grant LCOG full access to their personal property for inspection and duplication of the information contained in the property.</div>
        <div class="q-mt-sm">Employee agrees to use LCOG-owned equipment, records, and materials for purposes of LCOG business only, and to protect them against unauthorized or accidental access, use, modification, destruction, or disclosure. Employee agrees to report to the manager instances of loss, damage, or unauthorized access at the earliest reasonable opportunity.</div>
        <div class="q-mt-sm">LCOG records and documents must be disposed of at an LCOG office.</div>

        <div class="text-h6 q-mt-md">Dependent Care</div>
        <div class="q-mt-sm">Employee will not undertake to provide primary care for any dependents who would require the care of a caregiver during at-home working hours. If temporarily care for a dependent during scheduled Telework hours is necessary, employee will notify their manager and sick or vacation leave, as appropriate, should be used for dependent care time for that time.</div>
        <div class="q-mt-sm">For employees who have dependents requiring care during Telework hours, they must attach documentation of dependent care arrangements.</div>
        <div class="q-mt-sm">Does the employee have dependents requiring care during Telework hours?</div>
          <q-option-group
              :options="yesNoOptions"
              type="radio"
              v-model="dependentCareChecklist1"
              inline
            />
        <div class="q-mt-sm">If yes, attach documentation of dependent care arrangements.</div>
        <div><strong>DOCUMENTATION</strong></div>

        <div class="text-h6 q-mt-md">Employment Relationship</div>
        <div class="q-mt-sm">Employee understands that all obligations, responsibilities, terms, and conditions of employment with LCOG remain unchanged, except those obligations and responsibilities specifically addressed in this agreement. Nothing in this agreement changes the nature of the employment relationship Employee has with LCOG.</div>

        <div class="text-h6 q-mt-md">Termination of Telework Agreement</div>
        <div class="q-mt-sm">The employee understands that Telework is a privilege rather than a universal benefit or employee right.  LCOG or the employee may discontinue or suspend this Telework Agreement at any time.</div>

        <div class="text-h6 q-mt-md">Return of LCOG property</div>
        <div class="q-mt-sm">Employee agrees to return LCOG equipment, records, materials, and other property within three (3) days of termination of this agreement or within three (3) days of written notice of request for return of the equipment by LCOG.</div>

        <div class="q-mt-lg"><strong>I have read the Telework Policy and this Agreement and agree to all terms.  I understand that LCOG’s policies, as described in LCOG Policy Manual, remain in effect while I am a Teleworker, and that I agree to abide by them.  I also agree that the sole purpose of this agreement is to regulate Telework and that it constitutes neither an employment contract not an amendment to any existing contract or LCOG policy.</strong></div>

        <div class="q-mt-lg"><strong>Employee Signature______________________________ Date _____________________</strong></div>
        <div class="q-mt-lg"><strong>Manager Signature _______________________________ Date _____________________</strong></div>

        <hr class="q-mt-lg" />
        <div class="q-mt-sm">This Agreement takes effect only upon the signature of the Program Manager and Division Director.</div>

        <div class="q-mt-lg"><strong>Program Manager	____________________________ Date _____________________</strong></div>
        <div class="q-mt-lg"><strong>Division Director 	____________________________ Date _____________________</strong></div>
      </form>

      <!-- Spacing for footer -->
      <div style="height: 80px;"></div>

      <div id="sticky-footer" class="row justify-between" v-if="currentUserIsEmployee()">
        <q-btn id="update-button" class="col-1" color="white" text-color="black" label="Update" :disabled="!valuesAreChanged()" @click="updateTeleworkApplication()" />
        <q-btn v-if="this.showErrorButton && this.formErrorItems().length > 0" label="Show missing fields" icon="check" color="warning" @click="openErrorDialog('right')" />
        <div class="col-3 self-center status">Current Status: {{ status }}</div>
      </div>

    </div>
  </q-page>
</template>

<style scoped>
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
@media print {
  /* Ask the browser nicely to display table borders and images */
  * {
    -webkit-print-color-adjust: exact !important;   /* Chrome, Safari */
    color-adjust: exact !important;                 /*Firefox*/
  }
  #sticky-footer {
    display: none;
  }
}

.thanks {
    color: green;
}
</style>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import TeleworkApplicationDataService from '../services/TeleworkApplicationDataService'
import { AxiosTeleworkApplicationUpdateServerResponse, TeleworkApplicationRetrieve } from '../store/types'

@Component
export default class TeleworkApplication extends Vue {
  private applicationPk = ''
  private status = ''
  private employeePk = -1
  private employeeName = ''
  private managerName = ''
  private programManagerName = ''

  private date = ''
  private programManagerApprove = ''
  private hoursOnsite = ''
  private teleworkLocation = ''
  private hoursWorking = ''
  private duties = ''
  private communicationWhen = ''
  private communicationTime = ''
  private communicationHow = ''

  private equipmentProvidedPhone = false
  private equipmentProvidedLaptop = false
  private equipmentProvidedDesktop = false
  private equipmentProvidedMonitor = false
  private equipmentProvidedAccess = false
  private equipmentProvidedOther = false
  private equipmentProvidedOtherValue = ''
  private workspaceChecklist1 = ''
  private workspaceChecklist2 = ''
  private workspaceChecklist3 = ''
  private workspaceChecklist4 = ''
  private workspaceChecklist5 = ''
  private workspaceChecklist6 = ''
  private workspaceChecklist7 = ''
  private workspaceChecklist8 = ''
  private workspaceChecklist9 = ''
  private workspaceChecklist10 = ''
  private workspaceChecklist11 = ''
  private workspaceChecklist12 = ''
  private emergencyChecklist1 = ''
  private emergencyChecklist2 = ''
  private emergencyChecklist3 = ''
  private ergonomicsChecklist1 = ''
  private ergonomicsChecklist2 = ''
  private ergonomicsChecklist3 = ''
  private ergonomicsChecklist4 = ''
  private ergonomicsChecklist5 = ''
  private teleworkerComments = ''
  private managerComments = ''
  private dependentCareChecklist1 = ''

  private showErrorButton = false
  private showErrorDialog = false
  private errorDialogPosition = 'top'

  yesNoOptions = [
    { label: 'Yes', value: 'Y' },
    { label: 'No', value: 'N' }
  ]

  private currentUserPk(): number {
    return this.$store.getters['userModule/getEmployeeProfile'].pk // eslint-disable-line @typescript-eslint/no-unsafe-return, @typescript-eslint/no-unsafe-member-access
  }

  private currentUserIsEmployee(): boolean {
    return this.employeePk == this.$store.getters['userModule/getEmployeeProfile'].pk // eslint-disable-line @typescript-eslint/no-unsafe-return, @typescript-eslint/no-unsafe-member-access
  }

  private formErrorItems(): Array<[string, string]> {
    let errorItems: Array<[string, string]> = []
    // if (!this.stepIncreaseCurrentVal) {
    //   errorItems.push(['step-increase', 'Select Step Increase'])
    // }
    // if (!this.topStepBonusCurrentVal) {
    //   errorItems.push(['top-step-bonus', 'Select Top Step Bonus'])
    // }
    // if (!this.factorJobKnowledgeCurrentVal) {
    //   errorItems.push(['factor-job-knowledge', 'Evaluate Job Knowledge'])
    // }
    // if (!this.factorWorkQualityCurrentVal) {
    //   errorItems.push(['factor-work-quality', 'Evaluate Quality of Work'])
    // }
    // if (!this.factorWorkQuantityCurrentVal) {
    //   errorItems.push(['factor-work-quantity', 'Evaluate Quantity of Work'])
    // }
    // if (!this.factorWorkHabitsCurrentVal) {
    //   errorItems.push(['factor-work-habits', 'Evaluate Work Habits'])
    // }
    // if (!this.factorAnalysisCurrentVal) {
    //   errorItems.push(['factor-analysis', 'Evaluate Analysis and Decision-Making'])
    // }
    // if (!this.factorInitiativeCurrentVal) {
    //   errorItems.push(['factor-initiative', 'Evaluate Initiative and Creativity'])
    // }
    // if (!this.factorInterpersonalCurrentVal) {
    //   errorItems.push(['factor-interpersonal', 'Evaluate Interpersonal Relations'])
    // }
    // if (!this.factorCommunicationCurrentVal) {
    //   errorItems.push(['factor-communication', 'Evaluate Communication'])
    // }
    // if (!this.factorDependabilityCurrentVal) {
    //   errorItems.push(['factor-dependability', 'Evaluate Dependability and Responsibility'])
    // }
    // if (!this.factorProfessionalismCurrentVal) {
    //   errorItems.push(['factor-professionalism', 'Evaluate Professionalism and Customer Service'])
    // }
    // if (!this.factorManagementCurrentVal) {
    //   errorItems.push(['factor-management', 'Evaluate Project Management'])
    // }
    // if (!this.factorSupervisionCurrentVal) {
    //   errorItems.push(['factor-supervision', 'Evaluate Supervision'])
    // }
    // if (!this.evaluationSuccessesCurrentVal) {
    //   errorItems.push(['evaluation-successes', 'Write Employee Successes'])
    // }
    // if (!this.evaluationOpportunitiesCurrentVal) {
    //   errorItems.push(['evaluation-opportunities', 'Write Opportunities for Growth'])
    // }
    // if (!this.evaluationGoalsManagerCurrentVal) {
    //   errorItems.push(['evaluation-goals', 'Write Goals for the Coming Year'])
    // }
    // if (!this.descriptionReviewedEmployeeCurrentVal) {
    //   errorItems.push(['position-description-review', 'Review and Sign Position Description with Employee'])
    // }
    // if (this.descriptionReviewedEmployeeCurrentVal && !this.uploadedPositionDescriptionUrl) {
    //   errorItems.push(['position-description-review', 'Upload Signed Position Description'])
    // }
    return errorItems
  }

  private getOrCreateTeleworkApplication(employeePk: number) {
    return new Promise((resolve, reject) => {
      console.log('EPK', employeePk)
      this.$store.dispatch('teleworkModule/getOrCreateTeleworkApplication', {employeePk: employeePk})
        .then((response) => {
          this.setTeleworkApplicationData()
          resolve(response)
        })
        .catch(e => {
          console.error('Error getting or creating Telework Application from API:', e)
          reject(e)
        })
    })
  }

  private retrieveTeleworkApplication(applicationPk: string) {
    return new Promise((resolve, reject) => {
      this.$store.dispatch('teleworkModule/getTeleworkApplication', {applicationPk: applicationPk})
        .then(() => {
          this.setTeleworkApplicationData()
          resolve('Got Telework Application')
        })
        .catch(e => {
          console.error('Error retrieving Telework Application from API:', e)
          this.$router.push('/')
            .catch((e) => {
              console.error('Error navigating to dashboard upon not finding a matching Telework Application:', e)
            })
          reject(e)
        })
    })
  }

  private setTeleworkApplicationData() {
    const application: TeleworkApplicationRetrieve = this.$store.getters['teleworkModule/teleworkApplication'] // eslint-disable-line
    if (!application) {
      console.log('Application does not seem to exist. Redirecting...')
      this.$router.push('/')
        .catch((e) => {
          console.error('Error navigating to dashboard upon not finding a matching Telework Application:', e)
        })
      return
    }
    this.status = application.status
    this.employeePk = application.employee_pk
    this.employeeName = application.employee_name
    this.managerName = application.manager_name
    this.programManagerName = application.program_manager_name

    if (application.date) {
      this.date = application.date.toString()
    } else {
      const today = new Date()
      const dd = String(today.getDate()).padStart(2, '0');
      const mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
      const yyyy = today.getFullYear();
      this.date = `${yyyy}/${mm}/${dd}`
    }

    this.programManagerApprove = application.program_manager_approve
    this.hoursOnsite = application.hours_onsite
    this.teleworkLocation = application.telework_location
    this.hoursWorking = application.hours_working
    this.duties = application.duties
    this.communicationWhen = application.communication_when
    this.communicationTime = application.communication_time
    this.communicationHow = application.communication_how
    this.equipmentProvidedPhone = application.equipment_provided_phone
    this.equipmentProvidedLaptop = application.equipment_provided_laptop
    this.equipmentProvidedDesktop = application.equipment_provided_desktop
    this.equipmentProvidedMonitor = application.equipment_provided_monitor
    this.equipmentProvidedAccess = application.equipment_provided_access
    this.equipmentProvidedOther = application.equipment_provided_other
    this.equipmentProvidedOtherValue = application.equipment_provided_other_value
    this.workspaceChecklist1 = application.workspace_checklist_1
    this.workspaceChecklist2 = application.workspace_checklist_2
    this.workspaceChecklist3 = application.workspace_checklist_3
    this.workspaceChecklist4 = application.workspace_checklist_4
    this.workspaceChecklist5 = application.workspace_checklist_5
    this.workspaceChecklist6 = application.workspace_checklist_6
    this.workspaceChecklist7 = application.workspace_checklist_7
    this.workspaceChecklist8 = application.workspace_checklist_8
    this.workspaceChecklist9 = application.workspace_checklist_9
    this.workspaceChecklist10 = application.workspace_checklist_10
    this.workspaceChecklist11 = application.workspace_checklist_11
    this.workspaceChecklist12 = application.workspace_checklist_12
    this.emergencyChecklist1 = application.emergency_checklist_1
    this.emergencyChecklist2 = application.emergency_checklist_2
    this.emergencyChecklist3 = application.emergency_checklist_3
    this.ergonomicsChecklist1 = application.ergonomics_checklist_1
    this.ergonomicsChecklist2 = application.ergonomics_checklist_2
    this.ergonomicsChecklist3 = application.ergonomics_checklist_3
    this.ergonomicsChecklist4 = application.ergonomics_checklist_4
    this.ergonomicsChecklist5 = application.ergonomics_checklist_5
    this.teleworkerComments = application.teleworker_comments
    this.managerComments = application.manager_comments
    this.dependentCareChecklist1 = application.dependent_care_checklist_1
    // this.dependentCareDocumentation = application.dependent_care_documentation
    
    // this.periodStartDate = pr.period_start_date
    // this.periodEndDate = pr.period_end_date
    // this.effectiveDate = pr.effective_date
    // this.division = pr.employee_division
    // this.unitOrProgram = pr.employee_unit_or_program
    // this.jobTitle = pr.employee_job_title

    // this.evaluationType = pr.evaluation_type
    // this.evaluationTypeCurrentVal = this.evaluationType
    // this.probationaryEvaluationType = pr.probationary_evaluation_type
    // this.probationaryEvaluationTypeCurrentVal = this.probationaryEvaluationType
    // this.stepIncrease = pr.step_increase
    // this.stepIncreaseCurrentVal = this.stepIncrease
    // this.topStepBonus = pr.top_step_bonus
    // this.topStepBonusCurrentVal = this.topStepBonus
    // this.actionOther = pr.action_other
    // this.actionOtherCurrentVal = this.actionOther

    // this.factorJobKnowledge = pr.factor_job_knowledge
    // this.factorJobKnowledgeCurrentVal = this.factorJobKnowledge
    // this.factorWorkQuality = pr.factor_work_quality
    // this.factorWorkQualityCurrentVal = this.factorWorkQuality
    // this.factorWorkQuantity = pr.factor_work_quantity
    // this.factorWorkQuantityCurrentVal = this.factorWorkQuantity
    // this.factorWorkHabits = pr.factor_work_habits
    // this.factorWorkHabitsCurrentVal = this.factorWorkHabits
    // this.factorAnalysis = pr.factor_analysis
    // this.factorAnalysisCurrentVal = this.factorAnalysis
    // this.factorInitiative = pr.factor_initiative
    // this.factorInitiativeCurrentVal = this.factorInitiative
    // this.factorInterpersonal = pr.factor_interpersonal
    // this.factorInterpersonalCurrentVal = this.factorInterpersonal
    // this.factorCommunication = pr.factor_communication
    // this.factorCommunicationCurrentVal = this.factorCommunication
    // this.factorDependability = pr.factor_dependability
    // this.factorDependabilityCurrentVal = this.factorDependability
    // this.factorProfessionalism = pr.factor_professionalism
    // this.factorProfessionalismCurrentVal = this.factorProfessionalism
    // this.factorManagement = pr.factor_management
    // this.factorManagementCurrentVal = this.factorManagement
    // this.factorSupervision = pr.factor_supervision
    // this.factorSupervisionCurrentVal = this.factorSupervision

    // this.evaluationSuccesses = pr.evaluation_successes
    // this.evaluationSuccessesCurrentVal = this.evaluationSuccesses
    // this.evaluationOpportunities = pr.evaluation_opportunities
    // this.evaluationOpportunitiesCurrentVal = this.evaluationOpportunities
    // this.evaluationGoalsManager = pr.evaluation_goals_manager
    // this.evaluationGoalsManagerCurrentVal = this.evaluationGoalsManager
    // this.evaluationCommentsEmployee = pr.evaluation_comments_employee
    // this.evaluationCommentsEmployeeCurrentVal = this.evaluationCommentsEmployee

    // this.positionDescriptionLink = pr.position_description_link
    // this.descriptionReviewedEmployee = pr.description_reviewed_employee
    // this.descriptionReviewedEmployeeCurrentVal = this.descriptionReviewedEmployee
    // this.uploadedPositionDescriptionUrl = pr.signed_position_description

    // this.signatures = pr.all_required_signatures
  }

  private valuesAreChanged(): boolean {
    return true
    // if (
    //   // this.evaluationType == this.evaluationTypeCurrentVal &&
    //   // this.probationaryEvaluationType == this.probationaryEvaluationTypeCurrentVal &&
    //   // this.stepIncrease == this.stepIncreaseCurrentVal &&
    //   // this.topStepBonus == this.topStepBonusCurrentVal &&
    //   // this.actionOther == this.actionOtherCurrentVal &&
    //   // this.factorJobKnowledge == this.factorJobKnowledgeCurrentVal &&
    //   // this.factorWorkQuality == this.factorWorkQualityCurrentVal &&
    //   // this.factorWorkQuantity == this.factorWorkQuantityCurrentVal &&
    //   // this.factorWorkHabits == this.factorWorkHabitsCurrentVal &&
    //   // this.factorAnalysis == this.factorAnalysisCurrentVal &&
    //   // this.factorInitiative == this.factorInitiativeCurrentVal &&
    //   // this.factorInterpersonal == this.factorInterpersonalCurrentVal &&
    //   // this.factorCommunication == this.factorCommunicationCurrentVal &&
    //   // this.factorDependability == this.factorDependabilityCurrentVal &&
    //   // this.factorProfessionalism == this.factorProfessionalismCurrentVal &&
    //   // this.factorManagement == this.factorManagementCurrentVal &&
    //   // this.factorSupervision == this.factorSupervisionCurrentVal &&
    //   // this.evaluationSuccesses == this.evaluationSuccessesCurrentVal &&
    //   // this.evaluationOpportunities == this.evaluationOpportunitiesCurrentVal &&
    //   // this.evaluationGoalsManager == this.evaluationGoalsManagerCurrentVal &&
    //   // this.evaluationCommentsEmployee == this.evaluationCommentsEmployeeCurrentVal &&
    //   // this.descriptionReviewedEmployee == this.descriptionReviewedEmployeeCurrentVal
    // ) {
    //   return false
    // } else {
    //   return true
    // }
  }

  private updateTeleworkApplication() {
    return new Promise((resolve, reject) => {
      if (!this.equipmentProvidedOther) {
        this.equipmentProvidedOtherValue = ''
      }
      TeleworkApplicationDataService.update(this.applicationPk, {
        date: this.date.toString().split('/').join('-'),
        program_manager_approve: this.programManagerApprove,
        hours_onsite: this.hoursOnsite,
        telework_location: this.teleworkLocation,
        hours_working: this.hoursWorking,
        duties: this.duties,
        communication_when: this.communicationWhen,
        communication_time: this.communicationTime,
        communication_how: this.communicationHow,
        equipment_provided_phone: this.equipmentProvidedPhone,
        equipment_provided_laptop: this.equipmentProvidedLaptop,
        equipment_provided_desktop: this.equipmentProvidedDesktop,
        equipment_provided_monitor: this.equipmentProvidedMonitor,
        equipment_provided_access: this.equipmentProvidedAccess,
        equipment_provided_other: this.equipmentProvidedOther,
        equipment_provided_other_value: this.equipmentProvidedOtherValue,
        workspace_checklist_1: this.workspaceChecklist1,
        workspace_checklist_2: this.workspaceChecklist2,
        workspace_checklist_3: this.workspaceChecklist3,
        workspace_checklist_4: this.workspaceChecklist4,
        workspace_checklist_5: this.workspaceChecklist5,
        workspace_checklist_6: this.workspaceChecklist6,
        workspace_checklist_7: this.workspaceChecklist7,
        workspace_checklist_8: this.workspaceChecklist8,
        workspace_checklist_9: this.workspaceChecklist9,
        workspace_checklist_10: this.workspaceChecklist10,
        workspace_checklist_11: this.workspaceChecklist11,
        workspace_checklist_12: this.workspaceChecklist12,
        emergency_checklist_1: this.emergencyChecklist1,
        emergency_checklist_2: this.emergencyChecklist2,
        emergency_checklist_3: this.emergencyChecklist3,
        ergonomics_checklist_1: this.ergonomicsChecklist1,
        ergonomics_checklist_2: this.ergonomicsChecklist2,
        ergonomics_checklist_3: this.ergonomicsChecklist3,
        ergonomics_checklist_4: this.ergonomicsChecklist4,
        ergonomics_checklist_5: this.ergonomicsChecklist5,
        teleworker_comments: this.teleworkerComments,
        manager_comments: this.managerComments,
        dependent_care_checklist_1: this.dependentCareChecklist1,
        // dependent_care_documentation: this.dependentCareDocumentation

        // evaluation_type: this.evaluationType,
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
      .then((response: AxiosTeleworkApplicationUpdateServerResponse) => {
        this.status = response.data.status

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

        // this.$store.dispatch('performanceReviewModule/getAllPerformanceReviewsActionRequired')
        //   .catch(e => {
        //     console.error('Error getting getAllPerformanceReviewsActionRequired after updaing PR:', e)
        //     reject(e)
        //   })
        // this.$store.dispatch('performanceReviewModule/getAllPerformanceReviewsActionNotRequired')
        //   .catch(e => {
        //     console.error('Error getting getAllPerformanceReviewsActionNotRequired after updaing PR:', e)
        //     reject(e)
        //   })

        resolve('Updated Telework Application')
      })
      .catch(e => {
        console.error('Error updating Telework Application', e)
        reject(e)
      })
    })
  }

  private openErrorDialog(position: string) {
    this.errorDialogPosition = position
    this.showErrorDialog = true
  }

  mounted() {
    this.applicationPk = this.$route.params.pk
    this.retrieveTeleworkApplication(this.applicationPk)
      .catch(e => {
        console.error('Error retrieving Telework Application on Telework Application page mount:', e)
      })
  }

};
</script>

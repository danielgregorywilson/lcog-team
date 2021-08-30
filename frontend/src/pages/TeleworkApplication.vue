<template>
  <q-page class="q-pa-xl">
    <!-- <div v-html="message"></div> -->
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
        As per LCOG’s Telework Policy, <strong>{{ employeeName() }}</strong> (“employee”) and <strong>MANAGER NAME</strong> (“manager”) have discussed the suitability of a Telework arrangement.  The manager has considered, among other issues, LCOG’s operational needs; that the employee has demonstrated satisfactory working habits; the employee’s needs and work habits; whether the job performed by the employee is appropriate for Telework; equipment and technology needs (including the manager consulting with Information Services); workspace considerations; and scheduling issues.  The employee and manager have completed the attached proposed Telework Agreement.
      </div>
      <div class="q-mt-sm">This Application now is forwarded to <strong>PROGRAM MANAGER NAME</strong> (“Program Manager”).</div>
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
      <div class="q-mt-md">This Agreement is entered into between LCOG and <strong>{{ employeeName() }}</strong> (“Employee”). This Agreement takes effect only upon the signature of the Program Manager and Division Director.</div>
      <div class="q-mt-sm">This Telework Agreement starts on __________________ and will remain in effect for three months unless LCOG or Employee determines that the Telework Agreement should end earlier, for any reason.  If the Agreement remains in effect for three months, and if employee has performed to their manager’s satisfaction as a teleworker, this Agreement may be extended until and when either LCOG or employee decides to end the Agreement.  The availability of Telework can be discontinued at any time at LCOG’s discretion.</div>

      <div class="text-h6 q-mt-md">Location and Schedule</div>
      <ul>
        <li>Days and hours when Employee is expected to be onsite at LCOG’s regular place of business: ___________________________________________________________________________________</li>
        <li>Description about Employee’s primary Telework work site location: ___________________________________________________________________________________</li>
        <li>Days and hours when Employee will normally work at their Telework work site, along with break times (if applicable, for FLSA non-exempt employees):</li>
      </ul>
      
      <div class="text-h6 q-mt-md">Duties</div>
      <div class="q-mt-sm">The duties and assignments authorized to be performed at this alternate work site include:______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________</div>
      <div class="q-mt-sm text-italic">Note: Management reserves the right to assign work as necessary at any work site at any time as long as doing so is in line with any applicable collective bargaining agreement and state and federal laws.</div>
      <div class="q-mt-sm">Employee understands that they are required to accurately record all hours they work on their time sheets on a daily basis. <strong>Employee further understands and agrees that they may not work any overtime hours without first getting permission to do so from their manager.</strong></div>

      <div class="text-h6 q-mt-md">Communication</div>
      <div class="q-mt-sm">Specify the appropriate methods and times of communications including:</div>
      <ul>
        <li>When: ____________________________________________________________________________</li>
        <li>Time: ____________________________________________________________________________</li>
        <li>How (phone, text, face-to-face, etc.): _________________________________________</li>
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
      <q-checkbox v-model="lcogEquipmentProvided" val="cell-phone" label="Cell Phone" />
      <q-checkbox v-model="lcogEquipmentProvided" val="laptop" label="Laptop" />
      <q-checkbox v-model="lcogEquipmentProvided" val="desktop" label="Desktop Computer" />
      <q-checkbox v-model="lcogEquipmentProvided" val="monitor" label="Monitor" />
      <q-checkbox v-model="lcogEquipmentProvided" val="remote-access" label="Remote Network Access" />
      <q-checkbox v-model="lcogEquipmentProvided" val="other" label="Other" />
      <q-input dense filled v-if="lcogEquipmentProvided.indexOf('other')!=-1" v-model="otherLcogEquipmentProvided" class="q-pl-sm"/>

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

      <div class="q-mt-sm">Teleworker comments after the inspection (if any): ________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________</div>
      <div class="q-mt-sm">Manager comments regarding the Safety Checklist (if any): ______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________</div>

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
  </q-page>
</template>

<style scoped>
.thanks {
    color: green;
}
</style>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import SecurityMessageDataService from '../services/SecurityMessageDataService'

@Component
export default class SecurityMessage extends Vue {
  private date = ''
  private programManagerApprove = ''
  lcogEquipmentProvided = []
  otherLcogEquipmentProvided = ''
  workspaceChecklist1 = ''
  workspaceChecklist2 = ''
  workspaceChecklist3 = ''
  workspaceChecklist4 = ''
  workspaceChecklist5 = ''
  workspaceChecklist6 = ''
  workspaceChecklist7 = ''
  workspaceChecklist8 = ''
  workspaceChecklist9 = ''
  workspaceChecklist10 = ''
  workspaceChecklist11 = ''
  workspaceChecklist12 = ''
  emergencyChecklist1 = ''
  emergencyChecklist2 = ''
  emergencyChecklist3 = ''
  ergonomicsChecklist1 = ''
  ergonomicsChecklist2 = ''
  ergonomicsChecklist3 = ''
  ergonomicsChecklist4 = ''
  ergonomicsChecklist5 = ''
  dependentCareChecklist1 = ''

  yesNoOptions = [
    {
          label: 'Yes',
          value: 'yes'
        },
        {
          label: 'No',
          value: 'no'
        }
  ]

  private employeeName() {
    return this.$store.getters['userModule/getEmployeeProfile'].name // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-return
  }

  // private managerName() {
  //   const profile = this.$store.getters['userModule/getEmployeeProfile']
  //   return this.$store.getters['userModule/getEmployeeProfile'].manager // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-return
  // }




  
  private message = ''
  private securityMessagePk = -1
  private acknowledge = false
  
  private currentUserPk(): number {
    return this.$store.getters['userModule/getEmployeeProfile'].pk // eslint-disable-line @typescript-eslint/no-unsafe-return, @typescript-eslint/no-unsafe-member-access
  }

  private hasViewedCurrentSecurityMessage(): boolean {
    return this.$store.getters['securityMessageModule/viewedLatestSecurityMessage'] // eslint-disable-line @typescript-eslint/no-unsafe-return, @typescript-eslint/no-unsafe-member-access
  }

  private retrieveLatestSecurityMessage(): void {
    SecurityMessageDataService.getLatestSecurityMessage()
      .then(response => {
        this.message = response.data.content // eslint-disable-line @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-member-access
      })
      .catch(e => {
        console.error('Error retrieving latest security message from API:', e)
      })
  }

  private submitAcknowledgement(): void {
    this.$store.dispatch('securityMessageModule/setViewedSecurityMessage', {employee_pk: this.currentUserPk(), security_message_pk: this.securityMessagePk})
      .then(() => {
        this.$store.dispatch('securityMessageModule/getViewedLatestSecurityMessage')
        .catch(e => {
          console.error('Error getting viewed security message from store:', e)
        })
      })
      .catch(e => {
        console.error('Error marking security message as viewed:', e)
      })
  }

  mounted() {
    this.retrieveLatestSecurityMessage()
  }

};
</script>

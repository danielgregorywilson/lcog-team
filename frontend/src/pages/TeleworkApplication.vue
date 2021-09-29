<template>
  <q-page>
    <div class="q-pa-xl">
      <form>
        <div class="text-h4 text-center text-uppercase">Application For Proposed Telework</div>
        <div class="row items-center q-gutter-md q-mt-sm">
          <div>Date:</div>
          <div style="max-width: 300px">
            <q-input filled v-model="date" mask="date" :rules="['date']" :disable="!currentUserIsEmployeeOrManager()">
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
            <q-radio v-model="programManagerApprove" val="approve" label="Approve" :disable="!currentUserIsProgramManager()" />
            <q-radio v-model="programManagerApprove" val="not-approve" label="Does not approve" :disable="!currentUserIsProgramManager()" />
          </div>
        </div>
        <telework-application-signature :signature="programManagerSignature0" :currentUserPk="currentUserPk()" @clicked-sign-button="signApplication" />
        <div class="q-mt-lg">If the Program Manager approves this Application, the proposed Telework Agreement then will be signed by the employee, manager, Program Manager, and Division Director.  The manager then will set a date for the employee to begin Telework that meets operational needs.</div>
        <div class="q-mt-sm">If the Program Manager does not approve this application, they will explain their reasoning in writing to the employee and the manager.  The employee then may present a written request appealing that decision to the Division Director, who will make their decision within ten working days.  If the Division Director does not approve this application, they will explain their reasoning in writing to the employee, manager, and Program Manager.  The employee then may present a written request appealing that decision to the Executive Director, who will make their decision within ten working days.  If the Executive Director does not approve this application, they will explain their reasoning in writing to the employee, manager, Program Manager, and Division Director.  The final decision cannot be grieved.</div>
        <div class="q-mt-sm">If at each succeeding level of management (Division Director or Executive Director), the application is approved, then the proposed Telework Agreement will be signed by the employee, manager, Program Manager, and Division Director.  The manager then will set a date for the employee to begin Telework that meets operational needs.</div>

  
        <div class="text-h4 text-center text-uppercase q-mt-xl">Telework Agreement</div>
        <div class="text-h5 text-center text-uppercase">for the Lane Council of Governments (LCOG)</div>
        <div class="q-mt-md">This Agreement is entered into between LCOG and <strong>{{ employeeName }}</strong> (“Employee”). This Agreement takes effect only upon the signature of the Program Manager and Division Director.</div>
        <div class="q-mt-sm">This Telework Agreement starts on <span class="text-bold">{{ approvalDate }}</span> and will remain in effect for three months unless LCOG or Employee determines that the Telework Agreement should end earlier, for any reason.  If the Agreement remains in effect for three months, and if employee has performed to their manager’s satisfaction as a teleworker, this Agreement may be extended until and when either LCOG or employee decides to end the Agreement.  The availability of Telework can be discontinued at any time at LCOG’s discretion.</div>

        <div class="text-h6 q-mt-md">Location and Schedule</div>
        <ul>
          <li>
            <div id="hours-onsite">Days and hours when Employee is expected to be onsite at LCOG’s regular place of business:</div>
            <q-input
              filled
              input-class="hours-onsite"
              v-model="hoursOnsite"
              type="textarea"
              :disable="!currentUserIsEmployeeOrManager()"
            />
          </li>
          <li>
            <div id="telework-location">Description about Employee’s primary Telework work site location:</div>
            <q-input
              filled
              input-class="telework-location"
              v-model="teleworkLocation"
              type="textarea"
              :disable="!currentUserIsEmployeeOrManager()"
            />
          </li>
          <li>
            <div id="hours-working">Days and hours when Employee will normally work at their Telework work site, along with break times (if applicable, for FLSA non-exempt employees):</div>
            <q-input
              filled
              input-class="hours-working"
              v-model="hoursWorking"
              type="textarea"
              :disable="!currentUserIsEmployeeOrManager()"
            />
          </li>
        </ul>
        
        <div class="text-h6 q-mt-md">Duties</div>
        <div class="q-mt-sm">
          <div id="duties">The duties and assignments authorized to be performed at this alternate work site include:</div>
          <q-input
            filled
            input-class="duties"
            v-model="duties"
            type="textarea"
            :disable="!currentUserIsEmployeeOrManager()"
          />
        </div>
        <div class="q-mt-sm text-italic">Note: Management reserves the right to assign work as necessary at any work site at any time as long as doing so is in line with any applicable collective bargaining agreement and state and federal laws.</div>
        <div class="q-mt-sm">Employee understands that they are required to accurately record all hours they work on their time sheets on a daily basis. <strong>Employee further understands and agrees that they may not work any overtime hours without first getting permission to do so from their manager.</strong></div>

        <div class="text-h6 q-mt-md">Communication</div>
        <div class="q-mt-sm">Specify the appropriate methods and times of communications including:</div>
        <ul>
          <li class="row items-center">
            <div id="communication-when" class="col-md-1 col-xs-2 text-center">When:</div>
            <q-input filled v-model="communicationWhen" class="col" :disable="!currentUserIsEmployeeOrManager()" />
          </li>
          <li class="row items-center q-mt-xs">
            <div id="communication-time" class="col-md-1 col-xs-2 text-center">Time:</div>
            <q-input filled v-model="communicationTime" class="col q-mt-xs" :disable="!currentUserIsEmployeeOrManager()" />
          </li>
          <li class="row items-center q-mt-xs">
            <div id="communication-how" class="col-md-1 col-xs-2 text-center">How:</div>
            <q-input filled v-model="communicationHow" class="col q-mt-xs" label="e.g. phone, text, face-to-face, etc." :disable="!currentUserIsEmployeeOrManager()" />
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

        <div class="q-mt-sm" id="equipment-provided">This is based on the employee’s manager’s determination of what is needed at the telework location (check all that apply):</div>
        <q-checkbox v-model="equipmentProvidedPhone" val="cell-phone" label="Cell Phone" :disable="!currentUserIsEmployeeOrManager()" />
        <q-checkbox v-model="equipmentProvidedLaptop" val="laptop" label="Laptop" :disable="!currentUserIsEmployeeOrManager()" />
        <q-checkbox v-model="equipmentProvidedDesktop" val="desktop" label="Desktop Computer" :disable="!currentUserIsEmployeeOrManager()" />
        <q-checkbox v-model="equipmentProvidedMonitor" val="monitor" label="Monitor" :disable="!currentUserIsEmployeeOrManager()" />
        <q-checkbox v-model="equipmentProvidedAccess" val="remote-access" label="Remote Network Access" :disable="!currentUserIsEmployeeOrManager()" />
        <q-checkbox v-model="equipmentProvidedOther" val="other" label="Other" :disable="!currentUserIsEmployeeOrManager()" />
        <q-input dense filled v-if="equipmentProvidedOther" v-model="equipmentProvidedOtherValue" class="q-pl-sm" :disable="!currentUserIsEmployeeOrManager()"/>

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
          <li id="workspace-checklist-1">Are LCOG computers and other equipment plugged into surge protectors?
            <q-option-group
              :options="yesNoOptions"
              type="radio"
              v-model="workspaceChecklist1"
              inline
              :disable="!currentUserIsEmployeeOrManager()"
            />
          </li>
          <li id="workspace-checklist-2" class="q-mt-md">Are temperature, noise, ventilation, and lighting levels adequate for maintaining your normal level of performance?
            <q-option-group
              :options="yesNoOptions"
              type="radio"
              v-model="workspaceChecklist2"
              inline
              :disable="!currentUserIsEmployeeOrManager()"
            />
          </li>
          <li id="workspace-checklist-3" class="q-mt-md">Are all supplies and equipment (both LCOG and employee-owned) in good condition and can be safely used as intended?
            <q-option-group
              :options="yesNoOptions"
              type="radio"
              v-model="workspaceChecklist3"
              inline
              :disable="!currentUserIsEmployeeOrManager()"
            />
          </li>
          <li id="workspace-checklist-4" class="q-mt-md">Is storage organized to minimize risks of fires and spontaneous combustion?
            <q-option-group
              :options="yesNoOptions"
              type="radio"
              v-model="workspaceChecklist4"
              inline
              :disable="!currentUserIsEmployeeOrManager()"
            />
          </li>
          <li id="workspace-checklist-5" class="q-mt-md">Do all electrical enclosures (switches, outlets, receptacles, junction boxes) affecting the designated work area have tight fitting covers or plates?
            <q-option-group
              :options="yesNoOptions"
              type="radio"
              v-model="workspaceChecklist5"
              inline
              :disable="!currentUserIsEmployeeOrManager()"
            />
          </li>
          <li id="workspace-checklist-6" class="q-mt-md">Is all electrical equipment free of recognized hazards that would cause physical harm (frayed wires, bare conductors, loose wires or fixtures, exposed wiring on the ceiling or walls)?
            <q-option-group
              :options="yesNoOptions"
              type="radio"
              v-model="workspaceChecklist6"
              inline
              :disable="!currentUserIsEmployeeOrManager()"
            />
          </li>
          <li id="workspace-checklist-7" class="q-mt-md">Will the building’s electrical system permit the grounding of electrical equipment (a three-prong receptacle)?
            <q-option-group
              :options="yesNoOptions"
              type="radio"
              v-model="workspaceChecklist7"
              inline
              :disable="!currentUserIsEmployeeOrManager()"
            />
          </li>
          <li id="workspace-checklist-8" class="q-mt-md">Are aisles, doorways, and corners free from obstructions to permit visibility and movement?
            <q-option-group
              :options="yesNoOptions"
              type="radio"
              v-model="workspaceChecklist8"
              inline
              :disable="!currentUserIsEmployeeOrManager()"
            />
          </li>
          <li id="workspace-checklist-9" class="q-mt-md">Are the file cabinets and storage closets arranged so drawers and doors do not enter walkways?
            <q-option-group
              :options="yesNoOptions"
              type="radio"
              v-model="workspaceChecklist9"
              inline
              :disable="!currentUserIsEmployeeOrManager()"
            />
          </li>
          <li id="workspace-checklist-10" class="q-mt-md">Are heavy items, such as computer monitors and printers, securely placed on sturdy stands close to walls?
            <q-option-group
              :options="yesNoOptions"
              type="radio"
              v-model="workspaceChecklist10"
              inline
              :disable="!currentUserIsEmployeeOrManager()"
            />
          </li>
          <li id="workspace-checklist-11" class="q-mt-md">Are phone lines, electrical cords, and surge protectors secured under a desk or along a baseboard?
            <q-option-group
              :options="yesNoOptions"
              type="radio"
              v-model="workspaceChecklist11"
              inline
              :disable="!currentUserIsEmployeeOrManager()"
            />
          </li>
          <li id="workspace-checklist-12" class="q-mt-md">Are computer components kept out of direct sunlight and away from heaters?
            <q-option-group
              :options="yesNoOptions"
              type="radio"
              v-model="workspaceChecklist12"
              inline
              :disable="!currentUserIsEmployeeOrManager()"
            />
          </li>
        </ol>

        <div class="text-h6">EMERGENCY PREPAREDNESS:</div>
        <ol>
          <li id="emergency-checklist-1">Are emergency phone numbers (911, nearest hospital, fire department, police department, etc.) posted in the telework work space?
            <q-option-group
                :options="yesNoOptions"
                type="radio"
                v-model="emergencyChecklist1"
                inline
                :disable="!currentUserIsEmployeeOrManager()"
              />
          </li>
          <li id="emergency-checklist-2" class="q-mt-md">Is a first aid kit accessible and periodically inspected and replenished as needed?
            <q-option-group
                :options="yesNoOptions"
                type="radio"
                v-model="emergencyChecklist2"
                inline
                :disable="!currentUserIsEmployeeOrManager()"
              />
          </li>
          <li id="emergency-checklist-3" class="q-mt-md">In case of fire, is there a primary exit free of obstruction and easy to use?
            <q-option-group
                :options="yesNoOptions"
                type="radio"
                v-model="emergencyChecklist3"
                inline
                :disable="!currentUserIsEmployeeOrManager()"
              />
          </li>
        </ol>

        <div class="text-h6">ERGONOMICS:</div>
        <ol>
          <li>Are your desk, chair, computer, and other equipment of appropriate design and arranged so that:
            <ol type="a" class="q-mt-md">
              <li id="ergonomics-checklist-1">Neck and shoulders are not stooped to view the task?
                <q-option-group
                  :options="yesNoOptions"
                  type="radio"
                  v-model="ergonomicsChecklist1"
                  inline
                  :disable="!currentUserIsEmployeeOrManager()"
                />
              </li>
              <li id="ergonomics-checklist-2">There are not pressure points on any part of the body (wrists, forearms, back of legs)?
                <q-option-group
                  :options="yesNoOptions"
                  type="radio"
                  v-model="ergonomicsChecklist2"
                  inline
                  :disable="!currentUserIsEmployeeOrManager()"
                />
              </li>
              <li id="ergonomics-checklist-3">There is no glare on the computer screen?
                <q-option-group
                  :options="yesNoOptions"
                  type="radio"
                  v-model="ergonomicsChecklist3"
                  inline
                  :disable="!currentUserIsEmployeeOrManager()"
                />
              </li>
              <li id="ergonomics-checklist-4">Work can be performed without eye strain?
                <q-option-group
                  :options="yesNoOptions"
                  type="radio"
                  v-model="ergonomicsChecklist4"
                  inline
                  :disable="!currentUserIsEmployeeOrManager()"
                />
              </li>
              <li id="ergonomics-checklist-5">There is no strain on any part of the body for static tasks over 20 minutes?
                <q-option-group
                  :options="yesNoOptions"
                  type="radio"
                  v-model="ergonomicsChecklist5"
                  inline
                  :disable="!currentUserIsEmployeeOrManager()"
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
            :disable="!currentUserIsEmployee()"
          />  
        </div>
        <div class="q-mt-sm">
          <div>Manager comments regarding the Safety Checklist (if any):</div>
          <q-input
            filled
            input-class="manager-comments"
            v-model="managerComments"
            type="textarea"
            :disable="!currentUserIsManagerOfEmployee()"
          />  
        </div>

        <div class="text-h6 q-mt-lg">ACKNOWLEDGEMENT:</div>
        <div class="text-italic q-mt-sm">I have completed the checklist accurately and honestly to the best of my knowledge.  I understand that I have the right to ask questions, or to have additional training provided.</div>
        <div class="text-italic q-mt-sm">I agree to abide by and operate in accordance with the terms and conditions described in this document.  I agree that the sole purpose of this Agreement is to regulate Telework and that it constitutes neither an employment contract nor an amendment to any existing contract or LCOG policy.</div>
        <telework-application-signature :signature="employeeSignature0" :currentUserPk="currentUserPk()" @clicked-sign-button="signApplication" />


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

        <div id="dependent-care" class="text-h6 q-mt-md">Dependent Care</div>
        <div class="q-mt-sm">Employee will not undertake to provide primary care for any dependents who would require the care of a caregiver during at-home working hours. If temporarily care for a dependent during scheduled Telework hours is necessary, employee will notify their manager and sick or vacation leave, as appropriate, should be used for dependent care time for that time.</div>
        <div class="q-mt-sm">For employees who have dependents requiring care during Telework hours, they must attach documentation of dependent care arrangements.</div>
        <div class="q-mt-sm">Does the employee have dependents requiring care during Telework hours?</div>
        <q-option-group
            :options="yesNoOptions"
            type="radio"
            v-model="dependentCareChecklist1"
            inline
            :disable="!currentUserIsEmployeeOrManager()"
          />
        <div v-if="currentUserIsEmployeeOrManager() && dependentCareChecklist1 == 'Y'">
          <div class="q-mt-sm">If yes, attach documentation of dependent care arrangements.</div>
          <q-uploader
            ref="fileuploader"
            url=""
            @added="file_selected"
            style="max-width: 300px"
          >
            <template v-slot:header="scope">
              <div class="row no-wrap items-center q-pa-sm q-gutter-xs">
                <div class="col">
                  <div class="q-uploader__title">Upload dependent care documentation</div>
                </div>
                <q-btn v-if="scope.canAddFiles" type="a" icon="add_box" round dense flat>
                  <q-uploader-add-trigger />
                  <q-tooltip>Pick File</q-tooltip>
                </q-btn>
                <q-btn v-if="scope.canUpload" icon="cloud_upload" @click="uploadFile()" round dense flat >
                  <q-tooltip>Upload File</q-tooltip>
                </q-btn>

                <q-btn v-if="scope.isUploading" icon="clear" @click="scope.abort" round dense flat >
                  <q-tooltip>Abort Upload</q-tooltip>
                </q-btn>
              </div>
            </template>
            <template v-slot:list="scope">
              <q-list separator>
                <q-item v-for="file in scope.files" :key="file.name">
                  <q-item-section>
                    <q-item-label class="full-width ellipsis">
                      {{ file.name }}
                    </q-item-label>
                    <q-item-label caption>
                      {{ file.__sizeLabel }}
                    </q-item-label>
                  </q-item-section>
                  <q-item-section top side>
                    <q-btn
                      class="gt-xs"
                      size="12px"
                      flat
                      dense
                      round
                      icon="delete"
                      @click="scope.removeFile(file)"
                    />
                  </q-item-section>
                </q-item>
              </q-list>
            </template>
          </q-uploader>
          <div v-if="this.fileSuccessfullyUploaded" class="text-green">Successfully uploaded</div>
          <div v-if="uploadedDependentCareDocumentationUrl"> <a :href="uploadedDependentCareDocumentationUrl" target="_blank">Current uploaded documentation</a></div>
        </div>

        <div class="text-h6 q-mt-md">Employment Relationship</div>
        <div class="q-mt-sm">Employee understands that all obligations, responsibilities, terms, and conditions of employment with LCOG remain unchanged, except those obligations and responsibilities specifically addressed in this agreement. Nothing in this agreement changes the nature of the employment relationship Employee has with LCOG.</div>

        <div class="text-h6 q-mt-md">Termination of Telework Agreement</div>
        <div class="q-mt-sm">The employee understands that Telework is a privilege rather than a universal benefit or employee right.  LCOG or the employee may discontinue or suspend this Telework Agreement at any time.</div>

        <div class="text-h6 q-mt-md">Return of LCOG property</div>
        <div class="q-mt-sm">Employee agrees to return LCOG equipment, records, materials, and other property within three (3) days of termination of this agreement or within three (3) days of written notice of request for return of the equipment by LCOG.</div>

        <div class="q-mt-lg"><strong>I have read the Telework Policy and this Agreement and agree to all terms.  I understand that LCOG’s policies, as described in LCOG Policy Manual, remain in effect while I am a Teleworker, and that I agree to abide by them.  I also agree that the sole purpose of this agreement is to regulate Telework and that it constitutes neither an employment contract not an amendment to any existing contract or LCOG policy.</strong></div>

        <telework-application-signature :signature="employeeSignature1" :currentUserPk="currentUserPk()" @clicked-sign-button="signApplication" />
        <telework-application-signature :signature="managerSignature" :currentUserPk="currentUserPk()" @clicked-sign-button="signApplication" />

        <hr class="q-mt-lg" />
        <div class="q-mt-sm">This Agreement takes effect only upon the signature of the Program Manager and Division Director.</div>

        <telework-application-signature :signature="programManagerSignature1" :currentUserPk="currentUserPk()" @clicked-sign-button="signApplication" />
        <telework-application-signature :signature="divisionDirectorSignature" :currentUserPk="currentUserPk()" @clicked-sign-button="signApplication" />
      </form>

      <!-- Dialog of all error items -->
      <q-dialog v-model="showErrorDialog" :position="errorDialogPosition">
        <q-card style="width: 350px">
          <q-list bordered separator>
            <q-item v-for="(item, index) in this.formErrorItems()" :key="index" clickable @click="clickedErrorItem(item)">
              <q-item-label>{{item[1]}}</q-item-label>
            </q-item>
          </q-list>
        </q-card>
      </q-dialog>

      <!-- Dialog for when you are done and have signed the PR -->
      <q-dialog v-model="showApplicationSignedAndCompleteDialog">
        <q-card>
          <q-card-section class="row items-center">
            <q-avatar icon="check" color="primary" text-color="white" />
            <div class="col">
              <span class="q-ml-sm row">Your signature has been recorded, and you're all done!</span>
            </div>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Cancel" color="primary" v-close-popup />
            <q-btn flat label="Return to Dashboard" color="primary" @click="returnToDashboard()" />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Spacing for footer -->
      <div style="height: 80px;"></div>

      <div id="sticky-footer" class="row justify-between" v-if="currentUserIsEmployeeOrManager()">
        <q-btn id="update-button" class="col-1" color="white" text-color="black" label="Update" :disabled="!valuesAreChanged()" @click="updateTeleworkApplication()" />
        <q-btn v-if="this.showErrorButton && this.formErrorItems().length > 0" label="Show missing fields" icon="check" color="warning" @click="openErrorDialog('right')" />
        <div class="col-3 self-center status">Current Status: {{ status }}</div>
      </div>

    </div>
  </q-page>
</template>

<style scoped lang="scss">
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
import { scroll } from 'quasar'
const { getScrollTarget, setScrollPosition } = scroll
import TeleworkApplicationSignature from 'components/TeleworkApplicationSignature.vue'
import { Component, Vue } from 'vue-property-decorator'
import TeleworkApplicationDataService from '../services/TeleworkApplicationDataService'
import { AxiosTeleworkApplicationUpdateServerResponse, FileUploadDescriptionUploadServerResponse, TeleworkApplicationRetrieve } from '../store/types'

@Component({
  components: { TeleworkApplicationSignature }
})
export default class TeleworkApplication extends Vue {
  private applicationPk = ''
  private status = ''
  private approvalDate = ''
  private employeePk = -1
  private employeeName = ''
  private managerPk = -1
  private managerName = ''
  private programManagerPk = -1
  private programManagerName = ''

  private date = ''
  private dateCurrentVal = ''
  private programManagerApprove = ''
  private programManagerApproveCurrentVal = ''
  private hoursOnsite = ''
  private hoursOnsiteCurrentVal = ''
  private teleworkLocation = ''
  private teleworkLocationCurrentVal = ''
  private hoursWorking = ''
  private hoursWorkingCurrentVal = ''
  private duties = ''
  private dutiesCurrentVal = ''
  private communicationWhen = ''
  private communicationWhenCurrentVal = ''
  private communicationTime = ''
  private communicationTimeCurrentVal = ''
  private communicationHow = ''
  private communicationHowCurrentVal = ''

  private equipmentProvidedPhone = false
  private equipmentProvidedPhoneCurrentVal = false
  private equipmentProvidedLaptop = false
  private equipmentProvidedLaptopCurrentVal = false
  private equipmentProvidedDesktop = false
  private equipmentProvidedDesktopCurrentVal = false
  private equipmentProvidedMonitor = false
  private equipmentProvidedMonitorCurrentVal = false
  private equipmentProvidedAccess = false
  private equipmentProvidedAccessCurrentVal = false
  private equipmentProvidedOther = false
  private equipmentProvidedOtherCurrentVal = false
  private equipmentProvidedOtherValue = ''
  private equipmentProvidedOtherValueCurrentVal = ''
  private workspaceChecklist1 = ''
  private workspaceChecklist1CurrentVal = ''
  private workspaceChecklist2 = ''
  private workspaceChecklist2CurrentVal = ''
  private workspaceChecklist3 = ''
  private workspaceChecklist3CurrentVal = ''
  private workspaceChecklist4 = ''
  private workspaceChecklist4CurrentVal = ''
  private workspaceChecklist5 = ''
  private workspaceChecklist5CurrentVal = ''
  private workspaceChecklist6 = ''
  private workspaceChecklist6CurrentVal = ''
  private workspaceChecklist7 = ''
  private workspaceChecklist7CurrentVal = ''
  private workspaceChecklist8 = ''
  private workspaceChecklist8CurrentVal = ''
  private workspaceChecklist9 = ''
  private workspaceChecklist9CurrentVal = ''
  private workspaceChecklist10 = ''
  private workspaceChecklist10CurrentVal = ''
  private workspaceChecklist11 = ''
  private workspaceChecklist11CurrentVal = ''
  private workspaceChecklist12 = ''
  private workspaceChecklist12CurrentVal = ''
  private emergencyChecklist1 = ''
  private emergencyChecklist1CurrentVal = ''
  private emergencyChecklist2 = ''
  private emergencyChecklist2CurrentVal = ''
  private emergencyChecklist3 = ''
  private emergencyChecklist3CurrentVal = ''
  private ergonomicsChecklist1 = ''
  private ergonomicsChecklist1CurrentVal = ''
  private ergonomicsChecklist2 = ''
  private ergonomicsChecklist2CurrentVal = ''
  private ergonomicsChecklist3 = ''
  private ergonomicsChecklist3CurrentVal = ''
  private ergonomicsChecklist4 = ''
  private ergonomicsChecklist4CurrentVal = ''
  private ergonomicsChecklist5 = ''
  private ergonomicsChecklist5CurrentVal = ''
  private teleworkerComments = ''
  private teleworkerCommentsCurrentVal = ''
  private managerComments = ''
  private managerCommentsCurrentVal = ''
  
  private dependentCareChecklist1 = ''
  private dependentCareChecklist1CurrentVal = ''
  private uploadedDependentCareDocumentationUrl = ''
  private selectedFile: File = new File([''], '')
  private fileSuccessfullyUploaded = false

  // Format: [Signature index, Role, Name, Date, Employee PK, Employee Ready to Sign]
  private programManagerSignature0 = [-1, '', '', '', -1, false]
  private employeeSignature0 = [-1, '', '', '', -1, false]
  private employeeSignature1 = [-1, '', '', '', -1, false]
  private managerSignature = [-1, '', '', '', -1, false]
  private programManagerSignature1 = [-1, '', '', '', -1, false]
  private divisionDirectorSignature = [-1, '', '', '', -1, false]

  private showApplicationSignedAndCompleteDialog = false

  private showErrorButton = false
  private showErrorDialog = false
  private errorDialogPosition = 'top'

  $refs!: {
    fileuploader: HTMLFormElement
  }

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

  private currentUserIsManagerOfEmployee(): boolean {
    return this.managerPk == this.$store.getters['userModule/getEmployeeProfile'].pk // eslint-disable-line @typescript-eslint/no-unsafe-return, @typescript-eslint/no-unsafe-member-access
  }

  private currentUserIsEmployeeOrManager(): boolean {
    return this.currentUserIsEmployee() || this.currentUserIsManagerOfEmployee()
  }

  private currentUserIsProgramManager(): boolean {
    return this.programManagerPk == this.$store.getters['userModule/getEmployeeProfile'].pk // eslint-disable-line @typescript-eslint/no-unsafe-return, @typescript-eslint/no-unsafe-member-access
  }

  private formErrorItems(): Array<[string, string]> {
    let errorItems: Array<[string, string]> = []
    if (!this.hoursOnsiteCurrentVal) {
      errorItems.push(['hours-onsite', 'Enter hours onsite'])
    }
    if (!this.teleworkLocationCurrentVal) {
      errorItems.push(['telework-location', 'Enter telework location'])
    }
    if (!this.hoursWorkingCurrentVal) {
      errorItems.push(['hours-working', 'Enter hours working'])
    }
    if (!this.dutiesCurrentVal) {
      errorItems.push(['duties', 'Enter Duties'])
    }
    if (!this.communicationWhenCurrentVal) {
      errorItems.push(['communication-when', 'Enter communication: when'])
    }
    if (!this.communicationTimeCurrentVal) {
      errorItems.push(['communication-time', 'Enter communication: time'])
    }
    if (!this.communicationHowCurrentVal) {
      errorItems.push(['communication-how', 'Enter communication: how'])
    }
    if (this.equipmentProvidedOther && !this.equipmentProvidedOtherValue) {
      errorItems.push(['equipment-provided', 'Enter other equipment provided'])
    }
    if (!this.workspaceChecklist1) {
      errorItems.push(['workspace-checklist-1', 'Select work space checklist - 1'])
    }
    if (!this.workspaceChecklist2) {
      errorItems.push(['workspace-checklist-2', 'Select work space checklist - 2'])
    }
    if (!this.workspaceChecklist3) {
      errorItems.push(['workspace-checklist-3', 'Select work space checklist - 3'])
    }
    if (!this.workspaceChecklist4) {
      errorItems.push(['workspace-checklist-4', 'Select work space checklist - 4'])
    }
    if (!this.workspaceChecklist5) {
      errorItems.push(['workspace-checklist-5', 'Select work space checklist - 5'])
    }
    if (!this.workspaceChecklist6) {
      errorItems.push(['workspace-checklist-6', 'Select work space checklist - 6'])
    }
    if (!this.workspaceChecklist7) {
      errorItems.push(['workspace-checklist-7', 'Select work space checklist - 7'])
    }
    if (!this.workspaceChecklist8) {
      errorItems.push(['workspace-checklist-8', 'Select work space checklist - 8'])
    }
    if (!this.workspaceChecklist9) {
      errorItems.push(['workspace-checklist-9', 'Select work space checklist - 9'])
    }
    if (!this.workspaceChecklist10) {
      errorItems.push(['workspace-checklist-10', 'Select work space checklist - 10'])
    }
    if (!this.workspaceChecklist11) {
      errorItems.push(['workspace-checklist-11', 'Select work space checklist - 11'])
    }
    if (!this.workspaceChecklist12) {
      errorItems.push(['workspace-checklist-12', 'Select work space checklist - 12'])
    }
    if (!this.emergencyChecklist1) {
      errorItems.push(['emergency-checklist-1', 'Select emergency checklist - 1'])
    }
    if (!this.emergencyChecklist2) {
      errorItems.push(['emergency-checklist-2', 'Select emergency checklist - 2'])
    }
    if (!this.emergencyChecklist3) {
      errorItems.push(['emergency-checklist-3', 'Select emergency checklist - 3'])
    }
    if (!this.ergonomicsChecklist1) {
      errorItems.push(['ergonomics-checklist-1', 'Select ergonomics checklist - a'])
    }
    if (!this.ergonomicsChecklist2) {
      errorItems.push(['ergonomics-checklist-2', 'Select ergonomics checklist - b'])
    }
    if (!this.ergonomicsChecklist3) {
      errorItems.push(['ergonomics-checklist-3', 'Select ergonomics checklist - c'])
    }
    if (!this.ergonomicsChecklist4) {
      errorItems.push(['ergonomics-checklist-4', 'Select ergonomics checklist - d'])
    }
    if (!this.ergonomicsChecklist5) {
      errorItems.push(['ergonomics-checklist-5', 'Select ergonomics checklist - e'])
    }
    if (!this.ergonomicsChecklist5) {
      errorItems.push(['ergonomics-checklist-5', 'Select ergonomics checklist - e'])
    }
    if (!this.dependentCareChecklist1) {
      errorItems.push(['dependent-care', 'Select dependent care'])
    }
    if (this.dependentCareChecklist1 == 'Y' && !this.uploadedDependentCareDocumentationUrl) {
      errorItems.push(['dependent-care', 'Upload dependent care documentation'])
    }
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

    if (application.approval_date) {
      this.approvalDate = application.approval_date.toString()
    } else {
      this.approvalDate = 'the day it is approved'
    }

    this.employeePk = application.employee_pk
    this.employeeName = application.employee_name
    this.managerPk = application.manager_pk
    this.managerName = application.manager_name
    this.programManagerPk = application.program_manager_pk
    this.programManagerName = application.program_manager_name

    if (application.date) {
      this.date = application.date.toString().split('-').join('/')
    } else {
      const today = new Date()
      const dd = String(today.getDate()).padStart(2, '0');
      const mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
      const yyyy = today.getFullYear();
      this.date = `${yyyy}/${mm}/${dd}`
    }
    this.dateCurrentVal = this.date

    this.programManagerApprove = application.program_manager_approve
    this.programManagerApproveCurrentVal = this.programManagerApprove
    this.hoursOnsite = application.hours_onsite
    this.hoursOnsiteCurrentVal = this.hoursOnsite
    this.teleworkLocation = application.telework_location
    this.teleworkLocationCurrentVal = this.teleworkLocation
    this.hoursWorking = application.hours_working
    this.hoursWorkingCurrentVal = this.hoursWorking
    this.duties = application.duties
    this.dutiesCurrentVal = this.duties
    this.communicationWhen = application.communication_when
    this.communicationWhenCurrentVal = this.communicationWhen
    this.communicationTime = application.communication_time
    this.communicationTimeCurrentVal = this.communicationTime
    this.communicationHow = application.communication_how
    this.communicationHowCurrentVal = this.communicationHow
    this.equipmentProvidedPhone = application.equipment_provided_phone
    this.equipmentProvidedPhoneCurrentVal = this.equipmentProvidedPhone
    this.equipmentProvidedLaptop = application.equipment_provided_laptop
    this.equipmentProvidedLaptopCurrentVal = this.equipmentProvidedLaptop
    this.equipmentProvidedDesktop = application.equipment_provided_desktop
    this.equipmentProvidedDesktopCurrentVal = this.equipmentProvidedDesktop
    this.equipmentProvidedMonitor = application.equipment_provided_monitor
    this.equipmentProvidedMonitorCurrentVal = this.equipmentProvidedMonitor
    this.equipmentProvidedAccess = application.equipment_provided_access
    this.equipmentProvidedAccessCurrentVal = this.equipmentProvidedAccess
    this.equipmentProvidedOther = application.equipment_provided_other
    this.equipmentProvidedOtherCurrentVal = this.equipmentProvidedOther
    this.equipmentProvidedOtherValue = application.equipment_provided_other_value
    this.equipmentProvidedOtherValueCurrentVal = this.equipmentProvidedOtherValue
    this.workspaceChecklist1 = application.workspace_checklist_1
    this.workspaceChecklist1CurrentVal = this.workspaceChecklist1
    this.workspaceChecklist2 = application.workspace_checklist_2
    this.workspaceChecklist2CurrentVal = this.workspaceChecklist2
    this.workspaceChecklist3 = application.workspace_checklist_3
    this.workspaceChecklist3CurrentVal = this.workspaceChecklist3
    this.workspaceChecklist4 = application.workspace_checklist_4
    this.workspaceChecklist4CurrentVal = this.workspaceChecklist4
    this.workspaceChecklist5 = application.workspace_checklist_5
    this.workspaceChecklist5CurrentVal = this.workspaceChecklist5
    this.workspaceChecklist6 = application.workspace_checklist_6
    this.workspaceChecklist6CurrentVal = this.workspaceChecklist6
    this.workspaceChecklist7 = application.workspace_checklist_7
    this.workspaceChecklist7CurrentVal = this.workspaceChecklist7
    this.workspaceChecklist8 = application.workspace_checklist_8
    this.workspaceChecklist8CurrentVal = this.workspaceChecklist8
    this.workspaceChecklist9 = application.workspace_checklist_9
    this.workspaceChecklist9CurrentVal = this.workspaceChecklist9
    this.workspaceChecklist10 = application.workspace_checklist_10
    this.workspaceChecklist10CurrentVal = this.workspaceChecklist10
    this.workspaceChecklist11 = application.workspace_checklist_11
    this.workspaceChecklist11CurrentVal = this.workspaceChecklist11
    this.workspaceChecklist12 = application.workspace_checklist_12
    this.workspaceChecklist12CurrentVal = this.workspaceChecklist12
    this.emergencyChecklist1 = application.emergency_checklist_1
    this.emergencyChecklist1CurrentVal = this.emergencyChecklist1
    this.emergencyChecklist2 = application.emergency_checklist_2
    this.emergencyChecklist2CurrentVal = this.emergencyChecklist2
    this.emergencyChecklist3 = application.emergency_checklist_3
    this.emergencyChecklist3CurrentVal = this.emergencyChecklist3
    this.ergonomicsChecklist1 = application.ergonomics_checklist_1
    this.ergonomicsChecklist1CurrentVal = this.ergonomicsChecklist1
    this.ergonomicsChecklist2 = application.ergonomics_checklist_2
    this.ergonomicsChecklist2CurrentVal = this.ergonomicsChecklist2
    this.ergonomicsChecklist3 = application.ergonomics_checklist_3
    this.ergonomicsChecklist3CurrentVal = this.ergonomicsChecklist3
    this.ergonomicsChecklist4 = application.ergonomics_checklist_4
    this.ergonomicsChecklist4CurrentVal = this.ergonomicsChecklist4
    this.ergonomicsChecklist5 = application.ergonomics_checklist_5
    this.ergonomicsChecklist5CurrentVal = this.ergonomicsChecklist5
    this.teleworkerComments = application.teleworker_comments
    this.teleworkerCommentsCurrentVal = this.teleworkerComments
    this.managerComments = application.manager_comments
    this.managerCommentsCurrentVal = this.managerComments
    this.dependentCareChecklist1 = application.dependent_care_checklist_1
    this.dependentCareChecklist1CurrentVal = this.dependentCareChecklist1
    this.uploadedDependentCareDocumentationUrl = application.dependent_care_documentation

    this.programManagerSignature0 = application.program_manager_signature_0
    this.employeeSignature0 = application.employee_signature_0
    this.employeeSignature1 = application.employee_signature_1
    this.managerSignature = application.manager_signature
    this.programManagerSignature1 = application.program_manager_signature_1
    this.divisionDirectorSignature = application.division_director_signature
  }

  private valuesAreChanged(): boolean {
    if (
      this.date == this.dateCurrentVal &&
      this.programManagerApprove == this.programManagerApproveCurrentVal &&
      this.hoursOnsite == this.hoursOnsiteCurrentVal &&
      this.teleworkLocation == this.teleworkLocationCurrentVal &&
      this.hoursWorking == this.hoursWorkingCurrentVal &&
      this.duties == this.dutiesCurrentVal &&
      this.communicationWhen == this.communicationWhenCurrentVal &&
      this.communicationTime == this.communicationTimeCurrentVal &&
      this.communicationHow == this.communicationHowCurrentVal &&
      this.equipmentProvidedPhone == this.equipmentProvidedPhoneCurrentVal &&
      this.equipmentProvidedLaptop == this.equipmentProvidedLaptopCurrentVal &&
      this.equipmentProvidedDesktop == this.equipmentProvidedDesktopCurrentVal &&
      this.equipmentProvidedMonitor == this.equipmentProvidedMonitorCurrentVal &&
      this.equipmentProvidedAccess == this.equipmentProvidedAccessCurrentVal &&
      this.equipmentProvidedOther == this.equipmentProvidedOtherCurrentVal &&
      this.equipmentProvidedOtherValue == this.equipmentProvidedOtherValueCurrentVal &&
      this.workspaceChecklist1 == this.workspaceChecklist1CurrentVal &&
      this.workspaceChecklist2 == this.workspaceChecklist2CurrentVal &&
      this.workspaceChecklist3 == this.workspaceChecklist3CurrentVal &&
      this.workspaceChecklist4 == this.workspaceChecklist4CurrentVal &&
      this.workspaceChecklist5 == this.workspaceChecklist5CurrentVal &&
      this.workspaceChecklist6 == this.workspaceChecklist6CurrentVal &&
      this.workspaceChecklist7 == this.workspaceChecklist7CurrentVal &&
      this.workspaceChecklist8 == this.workspaceChecklist8CurrentVal &&
      this.workspaceChecklist9 == this.workspaceChecklist9CurrentVal &&
      this.workspaceChecklist10 == this.workspaceChecklist10CurrentVal &&
      this.workspaceChecklist11 == this.workspaceChecklist11CurrentVal &&
      this.workspaceChecklist12 == this.workspaceChecklist12CurrentVal &&
      this.emergencyChecklist1 == this.emergencyChecklist1CurrentVal &&
      this.emergencyChecklist2 == this.emergencyChecklist2CurrentVal &&
      this.emergencyChecklist3 == this.emergencyChecklist3CurrentVal &&
      this.ergonomicsChecklist1 == this.ergonomicsChecklist1CurrentVal &&
      this.ergonomicsChecklist2 == this.ergonomicsChecklist2CurrentVal &&
      this.ergonomicsChecklist3 == this.ergonomicsChecklist3CurrentVal &&
      this.ergonomicsChecklist4 == this.ergonomicsChecklist4CurrentVal &&
      this.ergonomicsChecklist5 == this.ergonomicsChecklist5CurrentVal &&
      this.teleworkerComments == this.teleworkerCommentsCurrentVal &&
      this.managerComments == this.managerCommentsCurrentVal &&
      this.dependentCareChecklist1 == this.dependentCareChecklist1CurrentVal
    ) {
      return false
    } else {
      return true
    }
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
      })
      .then((response: AxiosTeleworkApplicationUpdateServerResponse) => {
        this.status = response.data.status

        this.dateCurrentVal = response.data.date.toString().split('-').join('/')
        this.programManagerApproveCurrentVal = response.data.program_manager_approve
        this.hoursOnsiteCurrentVal = response.data.hours_onsite
        this.teleworkLocationCurrentVal = response.data.telework_location
        this.hoursWorkingCurrentVal = response.data.hours_working
        this.dutiesCurrentVal = response.data.duties
        this.communicationWhenCurrentVal = response.data.communication_when
        this.communicationTimeCurrentVal = response.data.communication_time
        this.communicationHowCurrentVal = response.data.communication_how
        this.equipmentProvidedPhoneCurrentVal = response.data.equipment_provided_phone
        this.equipmentProvidedLaptopCurrentVal = response.data.equipment_provided_laptop
        this.equipmentProvidedDesktopCurrentVal = response.data.equipment_provided_desktop
        this.equipmentProvidedMonitorCurrentVal = response.data.equipment_provided_monitor
        this.equipmentProvidedAccessCurrentVal = response.data.equipment_provided_access
        this.equipmentProvidedOtherCurrentVal = response.data.equipment_provided_other
        this.equipmentProvidedOtherValueCurrentVal = response.data.equipment_provided_other_value
        this.workspaceChecklist1CurrentVal = response.data.workspace_checklist_1
        this.workspaceChecklist2CurrentVal = response.data.workspace_checklist_2
        this.workspaceChecklist3CurrentVal = response.data.workspace_checklist_3
        this.workspaceChecklist4CurrentVal = response.data.workspace_checklist_4
        this.workspaceChecklist5CurrentVal = response.data.workspace_checklist_5
        this.workspaceChecklist6CurrentVal = response.data.workspace_checklist_6
        this.workspaceChecklist7CurrentVal = response.data.workspace_checklist_7
        this.workspaceChecklist8CurrentVal = response.data.workspace_checklist_8
        this.workspaceChecklist9CurrentVal = response.data.workspace_checklist_9
        this.workspaceChecklist10CurrentVal = response.data.workspace_checklist_10
        this.workspaceChecklist11CurrentVal = response.data.workspace_checklist_11
        this.workspaceChecklist12CurrentVal = response.data.workspace_checklist_12
        this.emergencyChecklist1CurrentVal = response.data.emergency_checklist_1
        this.emergencyChecklist2CurrentVal = response.data.emergency_checklist_2
        this.emergencyChecklist3CurrentVal = response.data.emergency_checklist_3
        this.ergonomicsChecklist1CurrentVal = response.data.ergonomics_checklist_1
        this.ergonomicsChecklist2CurrentVal = response.data.ergonomics_checklist_2
        this.ergonomicsChecklist3CurrentVal = response.data.ergonomics_checklist_3
        this.ergonomicsChecklist4CurrentVal = response.data.ergonomics_checklist_4
        this.ergonomicsChecklist5CurrentVal = response.data.ergonomics_checklist_5
        this.teleworkerCommentsCurrentVal = response.data.teleworker_comments
        this.managerCommentsCurrentVal = response.data.manager_comments
        this.dependentCareChecklist1CurrentVal = response.data.dependent_care_checklist_1

        // this.signatures = response.data.all_required_signatures

        if (this.formErrorItems().length > 0) {
          this.showErrorButton = true
        }

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

  private signApplication(signatureIndex: number, employeePk: number) {
    this.$store.dispatch('teleworkModule/createSignature', {application_pk: this.applicationPk, index: signatureIndex, employee_pk: employeePk})
      .then(() => {
        this.updateTeleworkApplication()
          .then(() => {
            this.retrieveTeleworkApplication(this.applicationPk)
              .catch(e => {
                console.error('Error retrieving application after updating application after signing application:', e)
              })
            // this.$store.dispatch('teleworkModule/getAllPerformanceReviewsActionRequired')
            //   .catch(e => {
            //     console.error('Error getting getAllPerformanceReviewsActionRequired after updating PR after signing PR:', e)
            //   })
            // this.$store.dispatch('teleworkModule/getAllPerformanceReviewsActionNotRequired')
            //   .catch(e => {
            //     console.error('Error getting getAllPerformanceReviewsActionNotRequired after updating PR after signing PR:', e)
            //   })
            if (this.currentUserIsEmployee() && this.status == 'Ready for signature') {
              this.showApplicationSignedAndCompleteDialog = true
            }
          })
          .catch(e => {
            console.error('Error updating application after signing application:', e)
          })
      })
      .catch(e => {
        console.error('Error signing application:', e)
      })
  }

  private file_selected(file: Array<File>) {
    this.selectedFile = file[0];
  }

  private uploadFile() {
    let fd = new FormData();
    fd.append('pk', this.applicationPk)
    fd.append('file', this.selectedFile)
    
    TeleworkApplicationDataService.uploadDependentCareDocumentation(fd)
      .then((response: FileUploadDescriptionUploadServerResponse) => {
        if (response.status == 200) {
          this.$refs.fileuploader.reset()
          this.uploadedDependentCareDocumentationUrl = response.data
          this.fileSuccessfullyUploaded = true
          setTimeout(() => this.fileSuccessfullyUploaded = false, 5000)
          this.updateTeleworkApplication()
            .catch(e => {
              console.error('Error updating telework application after uploading dependent care documentation:', e)
            })
        }
      })
      .catch(e => {
        console.error('Error uploading dependent care documentation:', e)
      })
  }

  private openErrorDialog(position: string) {
    this.errorDialogPosition = position
    this.showErrorDialog = true
  }

  private clickedErrorItem(item: [string, string]) {
    this.showErrorDialog = false
    const element = document.getElementById(item[0])
    if (!!element) {
      const target = getScrollTarget(element)
      const offset = element.offsetTop - 50
      const duration = 500
      setScrollPosition(target, offset, duration)
    }
  }

  private returnToDashboard(): void {
    this.$router.push('/')
      .catch(e => {
        console.error('Error navigating to dashboard:', e)
      })
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

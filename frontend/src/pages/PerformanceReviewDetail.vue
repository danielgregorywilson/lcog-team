<template>
  <q-page id="performance-review-detail-page">
    <div class="q-px-md">
      <!-- Logo appears in print view only -->
      <q-img
        id="lcog-logo"
        src="../assets/lcog-banner.png"
      />
      <h4 class="text-bold text-center">Performance Evaluation Report</h4>
      <div class="eval-grid-container">
        <div class="eval-box eval-box-1">
            <div class="row text-bold">Employee:</div>
            <div class="row">{{ employeeName }}</div>
        </div>
        <div class="eval-box eval-box-2">
            <div class="row text-bold">Manager:</div>
            <div class="row">{{ managerName }}</div>
        </div>
        <div class="eval-box eval-box-3">
            <div class="row text-bold">Performance Period:</div>
            <div class="row">{{ periodStartDate | readableDate }} - {{ periodEndDate | readableDate }}</div>
        </div>
        <div class="eval-box eval-box-4">
            <div class="row text-bold">Effective Date:</div>
            <div class="row">{{ effectiveDate | readableDate }}</div>
        </div>
        <div class="eval-box eval-box-5">
            <div class="row text-bold">Division:</div>
            <div class="row">{{ division }}</div>
        </div>
        <div class="eval-box eval-box-6">
            <div class="row text-bold">Unit/Program:</div>
            <div class="row">{{ unitOrProgram }}</div>
        </div>
        <div class="eval-box eval-box-7">
            <div class="row text-bold">Job Title:</div>
            <div class="row">{{ jobTitle }}</div>
        </div>
        <div class="row eval-box eval-box-full eval-box-full-1 text-bold">
          <div class="text-uppercase">Evaluation Type:</div>
          <div class="eval-box-full-1-probationary">
            <div class="label-radio-pair">
              <q-radio v-model="evaluationType" val="P" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" />
              <div class="text-uppercase">Probat&shy;ionary:</div>
            </div>
            <div class="label-radio-pair">
              <q-radio v-model="probationaryEvaluationType" val="S" :disable="evaluationType != 'P' || !currentUserIsManagerOfEmployee() || employeeHasSigned()" />
              <div>180 days</div>
            </div>
            <div class="label-radio-pair">
              <q-radio v-model="probationaryEvaluationType" val="N" :disable="evaluationType != 'P' || !currentUserIsManagerOfEmployee() || employeeHasSigned()" />
              <div>6 months</div>
            </div>
          </div>
          <div class="eval-box-full-1-annual">
            <div class="label-radio-pair">
              <q-radio v-model="evaluationType" val="A" @input="() => this.probationaryEvaluationType = ''" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" />
              <div class="text-uppercase">Annual</div>
            </div>
          </div>
        </div>
        <div class="row eval-box eval-box-full eval-box-full-2">
          <div class="text-uppercase text-bold">Action:</div>
          <div class="label-radio-triplet">
            <div class="text-bold" id="step-increase">Step Increase:</div>
            <q-radio v-model="stepIncrease" val="Y" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" />
            <div>Yes</div>
            <q-radio v-model="stepIncrease" val="N" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" />
            <div>No</div>
          </div>
          <div class="label-radio-triplet">
            <div class="text-bold" id="top-step-bonus">Top-Step Bonus</div>
            <q-radio v-model="topStepBonus" val="Y" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" />
            <div>Yes</div>
            <q-radio v-model="topStepBonus" val="N" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" />
            <div>No</div>
          </div>
          <div id="action-other">
            <q-input outlined v-model="actionOther" label="Other" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" />
          </div>
        </div>
      </div>

      <h5 class="text-uppercase text-center text-bold"><u>Rating Scale</u></h5>
      <div class="rating-grid-container">
        <div class="rating-box"><span class="text-bold">(1)*</span> Needs Improvement</div>
        <div class="rating-box">The employee’s work performance does not consistently meet the standards of the position. Serious effort is needed to improve performance.</div>
        <div class="rating-box"><span class="text-bold">(2)</span> Meets Job Requirments</div>
        <div class="rating-box">The employee’s work performance consistently meets the standards of the position.</div>
        <div class="rating-box"><span class="text-bold">(3)</span> Exceeds Job Requirments</div>
        <div class="rating-box">The employee’s work performance is frequently or consistently above the level of a satisfactory employee.</div>
        <div class="rating-box"><span class="text-bold">(N/A)</span> Not Applicable</div>
        <div class="rating-box">Does not pertain to the employee’s actual job duties.</div>
      </div>
      <div>*Factors rated <span class="text-bold">(1)</span> Needs improvement must be addressed with a plan for improvement.</div>

      <div v-if="currentUserIsManagerOfEmployee()" id="notes">
        <hr />
        <h5 class="text-h5 text-uppercase text-bold q-my-md"><u>Your Notes for {{ employeeName }}</u></h5>
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

      <hr />

      <h5 class="text-uppercase text-bold q-my-md"><u>I. Performance Factors Reviewed</u></h5>
      <div class="factors-grid-container">

        <!-- Desktop/Tablet Headers -->
        <div class="factors-header-box text-bold text-center factors-header-desktop factors-header-sticky">Performance Factors Reviewed</div>
        <div class="factors-header-box text-bold text-center factors-header-desktop factors-header-sticky">Needs Improvement</div>
        <div class="factors-header-box text-bold text-center factors-header-desktop factors-header-sticky">Meets Job Requirements</div>
        <div class="factors-header-box text-bold text-center factors-header-desktop factors-header-sticky">Exceeds Job Requirements</div>
        <div class="factors-header-box text-bold text-center factors-header-desktop factors-header-sticky">Not Applicable</div>

        <!-- Mobile Headers -->
        <div class="factors-header-box text-bold text-center factors-header-mobile factors-header-sticky">Performance Factors Reviewed</div>
        <div class="factors-header-box text-bold text-center factors-header-mobile factors-header-sticky">Needs Improv&shy;ement</div>
        <div class="factors-header-box text-bold text-center factors-header-mobile factors-header-sticky">Meets Job Require&shy;ments</div>
        <div class="factors-header-box text-bold text-center factors-header-mobile factors-header-sticky">Exceeds Job Require&shy;ments</div>
        <div class="factors-header-box text-bold text-center factors-header-mobile factors-header-sticky">Not Appli&shy;cable</div>

        <div class="factors-box" id="factor-job-knowledge">
            <div class="row text-bold"><u>Job Knowledge</u></div>
            <div class="row">Present knowledge of techniques, skills, procedures, technologies, equipment, rules and policies of position.</div>
        </div>
        <div class="factors-radio-box"><q-radio v-model="factorJobKnowledge" val="N" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" /></div>
        <div class="factors-radio-box"><q-radio v-model="factorJobKnowledge" val="M" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" /></div>
        <div class="factors-radio-box"><q-radio v-model="factorJobKnowledge" val="E" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" /></div>
        <div class="factors-radio-box"></div>
        <div class="factors-box">
            <div class="row text-bold" id="factor-work-quality"><u>Quality of Work</u></div>
            <div class="row">Turns in high quality work and very seldom makes errors.</div>
        </div>
        <div class="factors-radio-box"><q-radio v-model="factorWorkQuality" val="N" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" /></div>
        <div class="factors-radio-box"><q-radio v-model="factorWorkQuality" val="M" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" /></div>
        <div class="factors-radio-box"><q-radio v-model="factorWorkQuality" val="E" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" /></div>
        <div class="factors-radio-box"></div>
        <div class="factors-box" id="factor-work-quantity">
            <div class="row text-bold"><u>Quantity of Work</u></div>
            <div class="row">Accomplishes stated goals and expectations.</div>
        </div>
        <div class="factors-radio-box"><q-radio v-model="factorWorkQuantity" val="N" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" /></div>
        <div class="factors-radio-box"><q-radio v-model="factorWorkQuantity" val="M" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" /></div>
        <div class="factors-radio-box"><q-radio v-model="factorWorkQuantity" val="E" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" /></div>
        <div class="factors-radio-box"></div>
        <div class="factors-box" id="factor-work-habits">
            <div class="row text-bold"><u>Work Habits</u></div>
            <div class="row">Uses equipment, supplies and time efficiently; punctual and on time.</div>
        </div>
        <div class="factors-radio-box"><q-radio v-model="factorWorkHabits" val="N" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" /></div>
        <div class="factors-radio-box"><q-radio v-model="factorWorkHabits" val="M" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" /></div>
        <div class="factors-radio-box"><q-radio v-model="factorWorkHabits" val="E" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" /></div>
        <div class="factors-radio-box"></div>
        <div class="factors-box" id="factor-analysis">
            <div class="row text-bold"><u>Analysis and Decision-Making</u></div>
            <div class="row">Has strong analytical abilities and makes sound judgements.</div>
        </div>
        <div class="factors-radio-box"><q-radio v-model="factorAnalysis" val="N" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" /></div>
        <div class="factors-radio-box"><q-radio v-model="factorAnalysis" val="M" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" /></div>
        <div class="factors-radio-box"><q-radio v-model="factorAnalysis" val="E" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" /></div>
        <div class="factors-radio-box"></div>
        <div class="factors-box" id="factor-initiative">
            <div class="row text-bold"><u>Initiative and Creativity</u></div>
            <div class="row">A self-starter and seeks new responsibilities and opportunities for leadership; demonstrates creativity in performing tasks and identifying resolutions.</div>
        </div>
        <div class="factors-radio-box"><q-radio v-model="factorInitiative" val="N" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" /></div>
        <div class="factors-radio-box"><q-radio v-model="factorInitiative" val="M" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" /></div>
        <div class="factors-radio-box"><q-radio v-model="factorInitiative" val="E" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" /></div>
        <div class="factors-radio-box"></div>
        <div class="factors-box" id="factor-interpersonal">
            <div class="row text-bold"><u>Interpersonal Relations</u></div>
            <div class="row">Presents good attitude, works well in teams, cooperates with others, and is thoughtful and courteous/polite.</div>
        </div>
        <div class="factors-radio-box"><q-radio v-model="factorInterpersonal" val="N" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" /></div>
        <div class="factors-radio-box"><q-radio v-model="factorInterpersonal" val="M" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" /></div>
        <div class="factors-radio-box"><q-radio v-model="factorInterpersonal" val="E" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" /></div>
        <div class="factors-radio-box"></div>
        <div class="factors-box" id="factor-communication">
            <div class="row text-bold"><u>Communication</u></div>
            <div class="row">Effectively communicates (oral and written) and keeps others appropriately informed.</div>
        </div>
        <div class="factors-radio-box"><q-radio v-model="factorCommunication" val="N" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" /></div>
        <div class="factors-radio-box"><q-radio v-model="factorCommunication" val="M" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" /></div>
        <div class="factors-radio-box"><q-radio v-model="factorCommunication" val="E" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" /></div>
        <div class="factors-radio-box"></div>
        <div class="factors-box" id="factor-dependability">
            <div class="row text-bold"><u>Dependability and Responsibility</u></div>
            <div class="row">Completes assigned work within prescribed timelines; rarely needs direct supervision.</div>
        </div>
        <div class="factors-radio-box"><q-radio v-model="factorDependability" val="N" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" /></div>
        <div class="factors-radio-box"><q-radio v-model="factorDependability" val="M" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" /></div>
        <div class="factors-radio-box"><q-radio v-model="factorDependability" val="E" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" /></div>
        <div class="factors-radio-box"></div>
        <div class="factors-box" id="factor-professionalism">
            <div class="row text-bold"><u>Professionalism and Customer Service</u></div>
            <div class="row">Presents and represents oneself and the agency in a positive manner; provides and delivers professional, helpful, high quality service and assistance.</div>
        </div>
        <div class="factors-radio-box"><q-radio v-model="factorProfessionalism" val="N" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" /></div>
        <div class="factors-radio-box"><q-radio v-model="factorProfessionalism" val="M" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" /></div>
        <div class="factors-radio-box"><q-radio v-model="factorProfessionalism" val="E" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" /></div>
        <div class="factors-radio-box"></div>
        <div class="factors-box" id="factor-management">
            <div class="row text-bold"><u>Project Management</u></div>
            <div class="row">Coordinates, delegates tasks to team members, and communicates internally and externally about projects; projects are high quality and are completed within timelines.</div>
        </div>
        <div class="factors-radio-box"><q-radio v-model="factorManagement" val="N" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" /></div>
        <div class="factors-radio-box"><q-radio v-model="factorManagement" val="M" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" /></div>
        <div class="factors-radio-box"><q-radio v-model="factorManagement" val="E" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" /></div>
        <div class="factors-radio-box"><q-radio v-model="factorManagement" val="NA" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" /></div>
        <div class="factors-box" id="factor-supervision">
            <div class="row text-bold"><u>Supervision</u></div>
            <div class="row">Provides support/guidance and motivation with open communication and transparency.</div>
        </div>
        <div class="factors-radio-box"><q-radio v-model="factorSupervision" val="N" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" /></div>
        <div class="factors-radio-box"><q-radio v-model="factorSupervision" val="M" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" /></div>
        <div class="factors-radio-box"><q-radio v-model="factorSupervision" val="E" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" /></div>
        <div class="factors-radio-box"><q-radio v-model="factorSupervision" val="NA" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" /></div>
      </div>

      <h5 class="text-uppercase text-bold q-my-md" id="evaluation-successes"><u>II. Employee's Successes</u></h5>
      <q-input
        v-model="evaluationSuccesses"
        type="textarea"
        :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
      />

      <h5 class="text-uppercase text-bold q-my-md" id="evaluation-opportunities"><u>III. Opportunities for Growth</u></h5>
      <q-input
        v-model="evaluationOpportunities"
        type="textarea"
        :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
      />

      <h5 class="text-uppercase text-bold q-my-md" id="evaluation-goals"><u>IV. Goals for the Coming Year</u></h5>
      <q-input
        v-model="evaluationGoalsManager"
        type="textarea"
        :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
      />

      <!-- <h5 class="text-uppercase">V. Goals for the Coming Year (Employee)</h5>
      <q-input
        v-model="evaluationGoalsEmployee"
        type="textarea"
      /> -->

      <h5><span class="text-uppercase text-bold q-my-md"><u>V. Employee Comments</u></span> (e.g. self-evaluation and goals)</h5>
      <q-input
        input-class="evaluation-comments-employee"
        v-model="evaluationCommentsEmployee"
        type="textarea"
        :disable="!currentUserIsEmployee() || employeeHasSigned()"
      />
      <q-btn v-if="currentUserIsEmployee()" id="save-comments-employee" color="white" text-color="black" label="Save comments" @click="updateEmployeeComments()" class="q-mt-sm" :disable="!employeeCommentsIsChanged()" />

      <h5 class="text-uppercase text-bold q-my-md"><u>VI. Position Description Review</u></h5>
      
      <div class="q-my-md" id="position-description-review">
        <div>Position Description: <a v-if="positionDescriptionLink" :href="positionDescriptionLink" target="_blank">{{ positionDescriptionLink }}</a><span v-else>No link provided</span></div>
        <div><q-checkbox v-model="descriptionReviewedEmployee" :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()" />Position Description has been reviewed and signed by employee and manager</div>
        <q-uploader
          v-if="currentUserIsManagerOfEmployee() && descriptionReviewedEmployee"
          ref="fileuploader"
          url=""
          @added="file_selected"
          style="max-width: 300px"
        >
          <template v-slot:header="scope">
            <div class="row no-wrap items-center q-pa-sm q-gutter-xs">
              <div class="col">
                <div class="q-uploader__title">Upload signed position description</div>
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
        <div v-if="descriptionReviewedEmployee && uploadedPositionDescriptionUrl"> <a :href="uploadedPositionDescriptionUrl" target="_blank">Current uploaded position description</a></div>
      </div>

      <div v-for="(signature, index) in signatures" :key="index" class="row signature-block">
        <div class="col">
          <div v-if="signature[1]" class="signature"><span class="signature-text">{{ signature[1] }}</span></div>
          <div v-else class="signature">
            <q-btn v-if="userCanSign(signature[3], signature[4])" color="white" text-color="black" label="Click to Sign" @click="signPerformanceReview()" class="signature-button" />
            <div v-else>&nbsp;</div>
          </div>
          <div class="signature-type"><span class="text-bold">{{ signature[0] }} Signature</span><span v-if="signature[0] == 'Employee'"><b>:</b><i class="q-ml-xs">I have reviewed this evaluation and discussed it further with my manager. Signing does not necessarily indicate agreement.</i></span></div>
        </div>
        <div class="col signature-date-block">
          <div v-if="signature[2]" class="signature-date"><span class="signature-date-text">{{ signature[2] | readableDate }}</span></div>
          <div v-else class="signature-date">&nbsp;</div>
          <span>Date</span>
        </div>
      </div>

      <!-- <div>
        <div class="row q-mb-md q-gutter-md items-start">
          <div class="col col-md-auto col-sm-12">
            <div>Date of Discussion</div>
            <q-date v-model="discussionDate" :options="noWeekends" />
          </div>
        </div>
      </div> -->

      <q-dialog v-model="showErrorDialog" :position="errorDialogPosition">
        <q-card style="width: 350px">
          <q-list bordered separator>
            <q-item v-for="(item, index) in this.formErrorItems()" :key="index" clickable @click="clickedErrorItem(item)">
              <q-item-label>{{item[1]}}</q-item-label>
            </q-item>
          </q-list>
        </q-card>
      </q-dialog>

      <!-- Spacing for footer -->
      <div style="height: 80px;"></div>

      <div id="sticky-footer" class="row justify-between" v-if="currentUserIsManagerOfEmployee()">
        <q-btn id="update-button" class="col-1" color="white" text-color="black" label="Update" :disabled="!valuesAreChanged()" @click="updatePerformanceReview()" />
        <q-btn v-if="this.showErrorButton && this.formErrorItems().length > 0" label="Show missing fields" icon="check" color="warning" @click="openErrorDialog('right')" />
        <div class="col-3 self-center status">Current Status: {{ status }}</div>
      </div>
    </div>
  </q-page>
</template>

<style scoped lang="scss">
  #lcog-logo {
    max-width: 300px;
    display: none;
  }
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
    display: grid;
    justify-content: space-between;
    align-items: center;
    grid-template-columns: auto auto auto auto;
  }
  .eval-box-full-1-probationary {
    display: grid;
    justify-content: center;
    align-items: center;
    grid-template-columns: auto auto auto;
  }
  .label-radio-pair {
    display: grid;
    justify-content: center;
    align-items: center;
    grid-template-columns: auto auto;
  }
  .label-radio-triplet {
    display: grid;
    justify-content: center;
    align-items: center;
    grid-template-columns: auto auto auto auto auto;
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
    grid-template-columns: auto 115px 115px 115px 115px;
  }
  .factors-header-mobile {
    display: none;
  }
  #update-button {
    min-width: 60px;
  }

  @media only screen and (max-width: 640px) {
    .eval-box-1 {
      grid-column-start: 1;
      grid-column-end: 13;
    }
    .eval-box-2 {
      grid-column-start: 1;
      grid-column-end: 6;
    }
    .eval-box-3 {
      grid-column-start: 6;
      grid-column-end: 13;
    }
    .eval-box-4 {
      grid-column-start: 1;
      grid-column-end: 6;
    }
    .eval-box-5 {
      grid-column-start: 6;
      grid-column-end: 13;
    }
    .eval-box-6 {
      grid-column-start: 1;
      grid-column-end: 6;
    }
    .eval-box-7 {
      grid-column-start: 6;
      grid-column-end: 13;
    } 
    .eval-box-full {
      grid-template-columns: auto;
    }
    .eval-box-full-1 {

    }
    .eval-box-full-2 {

      #action-other {
        // grid-column-start: span 3;
      }
    }
    .label-radio-pair {
      justify-content: start;
    }
    .label-radio-triplet {
      justify-content: start;
    }
    .factors-grid-container {
      grid-template-columns: auto 66px 66px 66px 65px;
    }
    .factors-header-desktop {
      display: none;
    }
    .factors-header-mobile {
      display: block;
    }

  }
  // Sticky header
  .factors-header-sticky {
    position: -webkit-sticky; /* Safari */
    position: sticky;
    top: 50px;
    z-index: 1;
  }
  .factors-header-box {
    background-color: white;
    padding: 10px;
  }
  .factors-box {
    background-color: white;
    padding: 5px;
  }
  .factors-radio-box {
    background-color: white;
    display: flex;
    justify-content: center;
  }
  .signature-block {
    margin-bottom: 20px;
  }
  .signature {
    max-width: 465px;
    height: 36px;
    border-bottom: 1px black solid;
    display: flex;
  }
  .signature-text {
    font-family: cursive, serif;
    align-self: flex-end;
  }
  .signature-type {
    max-width: 465px;
  }
  .signature-date {
    width: 100px;
    height: 36px;
    border-bottom: 1px black solid;
    display: flex;
  }
  .signature-date-text {
    align-self: flex-end;
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

  @media print {
    // Ask the browser nicely to display table borders and images
    * {
      -webkit-print-color-adjust: exact !important;   /* Chrome, Safari */
      color-adjust: exact !important;                 /*Firefox*/
    }
    #lcog-logo {
      display: block;
    }
    h4 {
      font-size: 20px;
      margin: 0;
    }
    h5 {
      font-size: 16px;
      margin: 0;
    }
    #notes {
      display: none;
    }
    .rating-box {
      padding: 0;
    }
    .factors-header-sticky {
      position: block;
    }
    .factors-header-box {
      padding-top: 0;
      padding-bottom: 0;
    }
    .factors-box {
      padding-top: 0;
      padding-bottom: 0;
    }
    .factors-grid-container {
      grid-template-columns: auto 72px 72px 72px 72px;
    }
    .signature-block {
      margin: 0;
    }
    #sticky-footer {
      display: none;
    }
  }
</style>

<script lang="ts">
import { date as quasarDate, scroll } from 'quasar'
const { getScrollTarget, setScrollPosition } = scroll
import { Component, Prop, Vue } from 'vue-property-decorator'
import PerformanceReviewDataService from '../services/PerformanceReviewDataService'
import { AxiosManagerReviewNotesForEmployeeServerResponse, AxiosPerformanceReviewUpdateServerResponse, PerformanceReviewRetrieve, ReviewNoteRetrieve, SignedPositionDescriptionUploadServerResponse } from '../store/types'
import '../filters'
import ReviewNoteDataService from '../services/ReviewNoteDataService'

@Component
export default class PerformanceReviewDetail extends Vue {
  @Prop({default: false}) readonly print!: boolean

  private prPk = ''
  private status = ''

  private employeePk = -1
  private managerPk = -1
  private employeeName = ''
  private managerName = ''
  private periodStartDate?: Date = new Date()
  private periodEndDate?: Date = new Date()
  private effectiveDate?: Date = new Date()
  private division = ''
  private unitOrProgram = ''
  private jobTitle = ''

  private evaluationTypeCurrentVal = ''
  private evaluationType = ''
  private probationaryEvaluationTypeCurrentVal = ''
  private probationaryEvaluationType = ''
  private stepIncreaseCurrentVal = ''
  private stepIncrease = ''
  private topStepBonusCurrentVal = ''
  private topStepBonus = ''
  private actionOtherCurrentVal = ''
  private actionOther = ''

  private factorJobKnowledgeCurrentVal = ''
  private factorJobKnowledge = ''
  private factorWorkQualityCurrentVal = ''
  private factorWorkQuality = ''
  private factorWorkQuantityCurrentVal = ''
  private factorWorkQuantity = ''
  private factorWorkHabitsCurrentVal = ''
  private factorWorkHabits = ''
  private factorAnalysisCurrentVal = ''
  private factorAnalysis = ''
  private factorInitiativeCurrentVal = ''
  private factorInitiative = ''
  private factorInterpersonalCurrentVal = ''
  private factorInterpersonal = ''
  private factorCommunicationCurrentVal = ''
  private factorCommunication = ''
  private factorDependabilityCurrentVal = ''
  private factorDependability = ''
  private factorProfessionalismCurrentVal = ''
  private factorProfessionalism = ''
  private factorManagementCurrentVal = ''
  private factorManagement = ''
  private factorSupervisionCurrentVal = ''
  private factorSupervision = ''

  private evaluationSuccessesCurrentVal = ''
  private evaluationSuccesses = ''
  private evaluationOpportunitiesCurrentVal = ''
  private evaluationOpportunities = ''
  private evaluationGoalsManagerCurrentVal = ''
  private evaluationGoalsManager = ''
  private evaluationCommentsEmployeeCurrentVal = ''
  private evaluationCommentsEmployee = ''

  private positionDescriptionLink = ''
  private descriptionReviewedEmployeeCurrentVal = false
  private descriptionReviewedEmployee = false
  private uploadedPositionDescriptionUrl = ''
  private selectedFile: File = new File([''], '')
  private fileSuccessfullyUploaded = false

  private signatures = [['', '', '']]

  private showErrorButton = false
  private showErrorDialog = false
  private errorDialogPosition = 'top'

  private reviewNotes: Array<ReviewNoteRetrieve> = []

  $refs!: {
    fileuploader: HTMLFormElement
  }

  private currentUserPk(): number {
    return this.$store.getters['userModule/getEmployeeProfile'].pk // eslint-disable-line
  }

  private currentUserIsUpperManager(): boolean {
    return this.$store.getters['userModule/getEmployeeProfile'].is_upper_manager // eslint-disable-line
  }

  private currentUserIsManagerOfEmployee(): boolean {
    return this.managerPk == this.$store.getters['userModule/getEmployeeProfile'].pk // eslint-disable-line
  }

  private employeeHasSigned(): boolean {
    return !!this.signatures[0][2]
  }

  private currentUserIsEmployee(): boolean {
    return this.employeePk == this.$store.getters['userModule/getEmployeeProfile'].pk // eslint-disable-line
  }

  private valuesAreChanged(): boolean {
    if (
      this.evaluationType == this.evaluationTypeCurrentVal &&
      this.probationaryEvaluationType == this.probationaryEvaluationTypeCurrentVal &&
      this.stepIncrease == this.stepIncreaseCurrentVal &&
      this.topStepBonus == this.topStepBonusCurrentVal &&
      this.actionOther == this.actionOtherCurrentVal &&
      this.factorJobKnowledge == this.factorJobKnowledgeCurrentVal &&
      this.factorWorkQuality == this.factorWorkQualityCurrentVal &&
      this.factorWorkQuantity == this.factorWorkQuantityCurrentVal &&
      this.factorWorkHabits == this.factorWorkHabitsCurrentVal &&
      this.factorAnalysis == this.factorAnalysisCurrentVal &&
      this.factorInitiative == this.factorInitiativeCurrentVal &&
      this.factorInterpersonal == this.factorInterpersonalCurrentVal &&
      this.factorCommunication == this.factorCommunicationCurrentVal &&
      this.factorDependability == this.factorDependabilityCurrentVal &&
      this.factorProfessionalism == this.factorProfessionalismCurrentVal &&
      this.factorManagement == this.factorManagementCurrentVal &&
      this.factorSupervision == this.factorSupervisionCurrentVal &&
      this.evaluationSuccesses == this.evaluationSuccessesCurrentVal &&
      this.evaluationOpportunities == this.evaluationOpportunitiesCurrentVal &&
      this.evaluationGoalsManager == this.evaluationGoalsManagerCurrentVal &&
      this.evaluationCommentsEmployee == this.evaluationCommentsEmployeeCurrentVal &&
      this.descriptionReviewedEmployee == this.descriptionReviewedEmployeeCurrentVal
    ) {
      return false
    } else {
      return true
    }
  }

  private employeeCommentsIsChanged(): boolean {
    if ( this.evaluationCommentsEmployee == this.evaluationCommentsEmployeeCurrentVal) {
      return false
    } else {
      return true
    }
  }

  private formErrorItems(): Array<[string, string]> {
    let errorItems: Array<[string, string]> = []
    if (!this.stepIncreaseCurrentVal) {
      errorItems.push(['step-increase', 'Select Step Increase'])
    }
    if (!this.topStepBonusCurrentVal) {
      errorItems.push(['top-step-bonus', 'Select Top Step Bonus'])
    }
    if (!this.factorJobKnowledgeCurrentVal) {
      errorItems.push(['factor-job-knowledge', 'Evaluate Job Knowledge'])
    }
    if (!this.factorWorkQualityCurrentVal) {
      errorItems.push(['factor-work-quality', 'Evaluate Quality of Work'])
    }
    if (!this.factorWorkQuantityCurrentVal) {
      errorItems.push(['factor-work-quantity', 'Evaluate Quantity of Work'])
    }
    if (!this.factorWorkHabitsCurrentVal) {
      errorItems.push(['factor-work-habits', 'Evaluate Work Habits'])
    }
    if (!this.factorAnalysisCurrentVal) {
      errorItems.push(['factor-analysis', 'Evaluate Analysis and Decision-Making'])
    }
    if (!this.factorInitiativeCurrentVal) {
      errorItems.push(['factor-initiative', 'Evaluate Initiative and Creativity'])
    }
    if (!this.factorInterpersonalCurrentVal) {
      errorItems.push(['factor-interpersonal', 'Evaluate Interpersonal Relations'])
    }
    if (!this.factorCommunicationCurrentVal) {
      errorItems.push(['factor-communication', 'Evaluate Communication'])
    }
    if (!this.factorDependabilityCurrentVal) {
      errorItems.push(['factor-dependability', 'Evaluate Dependability and Responsibility'])
    }
    if (!this.factorProfessionalismCurrentVal) {
      errorItems.push(['factor-professionalism', 'Evaluate Professionalism and Customer Service'])
    }
    if (!this.factorManagementCurrentVal) {
      errorItems.push(['factor-management', 'Evaluate Project Management'])
    }
    if (!this.factorSupervisionCurrentVal) {
      errorItems.push(['factor-supervision', 'Evaluate Supervision'])
    }
    if (!this.evaluationSuccessesCurrentVal) {
      errorItems.push(['evaluation-successes', 'Write Employee Successes'])
    }
    if (!this.evaluationOpportunitiesCurrentVal) {
      errorItems.push(['evaluation-opportunities', 'Write Opportunities for Growth'])
    }
    if (!this.evaluationGoalsManagerCurrentVal) {
      errorItems.push(['evaluation-goals', 'Write Goals for the Coming Year'])
    }
    if (!this.descriptionReviewedEmployeeCurrentVal) {
      errorItems.push(['position-description-review', 'Review and Sign Position Description with Employee'])
    }
    if (this.descriptionReviewedEmployeeCurrentVal && !this.uploadedPositionDescriptionUrl) {
      errorItems.push(['position-description-review', 'Upload Signed Position Description'])
    }
    return errorItems
  }

  private retrievePerformanceReview() {
    return new Promise((resolve, reject) => {
      this.$store.dispatch('performanceReviewModule/getPerformanceReview', {pk: this.$route.params.pk})
        .then(() => {
          const pr: PerformanceReviewRetrieve = this.$store.getters['performanceReviewModule/performanceReview'] // eslint-disable-line
          if (!pr) {
            console.log('PR does not seem to exist. Redirecting...')
            this.$router.push('/')
              .catch(e => {
                console.error('Error navigating to dashboard upon not finding a matching PR:', e)
                reject(e)
              })
            return
          }
          this.status = pr.status
          this.employeePk = pr.employee_pk
          this.managerPk = pr.manager_pk
          this.retrieveReviewNotes()
          this.prPk = pr.pk.toString()
          this.employeeName = pr.employee_name
          this.managerName = pr.manager_name
          this.periodStartDate = pr.period_start_date
          this.periodEndDate = pr.period_end_date
          this.effectiveDate = pr.effective_date
          this.division = pr.employee_division
          this.unitOrProgram = pr.employee_unit_or_program
          this.jobTitle = pr.employee_job_title

          this.evaluationType = pr.evaluation_type
          this.evaluationTypeCurrentVal = this.evaluationType
          this.probationaryEvaluationType = pr.probationary_evaluation_type
          this.probationaryEvaluationTypeCurrentVal = this.probationaryEvaluationType
          this.stepIncrease = pr.step_increase
          this.stepIncreaseCurrentVal = this.stepIncrease
          this.topStepBonus = pr.top_step_bonus
          this.topStepBonusCurrentVal = this.topStepBonus
          this.actionOther = pr.action_other
          this.actionOtherCurrentVal = this.actionOther

          this.factorJobKnowledge = pr.factor_job_knowledge
          this.factorJobKnowledgeCurrentVal = this.factorJobKnowledge
          this.factorWorkQuality = pr.factor_work_quality
          this.factorWorkQualityCurrentVal = this.factorWorkQuality
          this.factorWorkQuantity = pr.factor_work_quantity
          this.factorWorkQuantityCurrentVal = this.factorWorkQuantity
          this.factorWorkHabits = pr.factor_work_habits
          this.factorWorkHabitsCurrentVal = this.factorWorkHabits
          this.factorAnalysis = pr.factor_analysis
          this.factorAnalysisCurrentVal = this.factorAnalysis
          this.factorInitiative = pr.factor_initiative
          this.factorInitiativeCurrentVal = this.factorInitiative
          this.factorInterpersonal = pr.factor_interpersonal
          this.factorInterpersonalCurrentVal = this.factorInterpersonal
          this.factorCommunication = pr.factor_communication
          this.factorCommunicationCurrentVal = this.factorCommunication
          this.factorDependability = pr.factor_dependability
          this.factorDependabilityCurrentVal = this.factorDependability
          this.factorProfessionalism = pr.factor_professionalism
          this.factorProfessionalismCurrentVal = this.factorProfessionalism
          this.factorManagement = pr.factor_management
          this.factorManagementCurrentVal = this.factorManagement
          this.factorSupervision = pr.factor_supervision
          this.factorSupervisionCurrentVal = this.factorSupervision

          this.evaluationSuccesses = pr.evaluation_successes
          this.evaluationSuccessesCurrentVal = this.evaluationSuccesses
          this.evaluationOpportunities = pr.evaluation_opportunities
          this.evaluationOpportunitiesCurrentVal = this.evaluationOpportunities
          this.evaluationGoalsManager = pr.evaluation_goals_manager
          this.evaluationGoalsManagerCurrentVal = this.evaluationGoalsManager
          this.evaluationCommentsEmployee = pr.evaluation_comments_employee
          this.evaluationCommentsEmployeeCurrentVal = this.evaluationCommentsEmployee

          this.positionDescriptionLink = pr.position_description_link
          this.descriptionReviewedEmployee = pr.description_reviewed_employee
          this.descriptionReviewedEmployeeCurrentVal = this.descriptionReviewedEmployee
          this.uploadedPositionDescriptionUrl = pr.signed_position_description

          this.signatures = pr.all_required_signatures

          resolve()
        })
        .catch(e => {
          console.error('Error retrieving PR from API:', e)
          reject(e)
        })
    })
  }

  private retrieveReviewNotes(): void {
    ReviewNoteDataService.getAllManagerNotesForEmployee(this.employeePk)
      .then((response: AxiosManagerReviewNotesForEmployeeServerResponse) => {
        this.reviewNotes = response.data
      })
      .catch(e => {
        console.error('Error retrieving reivew notes from API:', e)
      })
  }

  private updatePerformanceReview() {
    return new Promise((resolve, reject) => {
      PerformanceReviewDataService.update(this.prPk, {
        evaluation_type: this.evaluationType,
        probationary_evaluation_type: this.probationaryEvaluationType,
        step_increase: this.stepIncrease,
        top_step_bonus: this.topStepBonus,
        action_other: this.actionOther,
        factor_job_knowledge: this.factorJobKnowledge,
        factor_work_quality: this.factorWorkQuality,
        factor_work_quantity: this.factorWorkQuantity,
        factor_work_habits: this.factorWorkHabits,
        factor_analysis: this.factorAnalysis,
        factor_initiative: this.factorInitiative,
        factor_interpersonal: this.factorInterpersonal,
        factor_communication: this.factorCommunication,
        factor_dependability: this.factorDependability,
        factor_professionalism: this.factorProfessionalism,
        factor_management: this.factorManagement,
        factor_supervision: this.factorSupervision,
        evaluation_successes: this.evaluationSuccesses,
        evaluation_opportunities: this.evaluationOpportunities,
        evaluation_goals_manager: this.evaluationGoalsManager,
        evaluation_comments_employee: this.evaluationCommentsEmployee,
        description_reviewed_employee: this.descriptionReviewedEmployee
      })
      .then((response: AxiosPerformanceReviewUpdateServerResponse) => {
        this.status = response.data.status

        this.evaluationTypeCurrentVal = response.data.evaluation_type
        this.probationaryEvaluationTypeCurrentVal = response.data.probationary_evaluation_type
        this.stepIncreaseCurrentVal = response.data.step_increase
        this.topStepBonusCurrentVal = response.data.top_step_bonus
        this.actionOtherCurrentVal = response.data.action_other

        this.factorJobKnowledgeCurrentVal = response.data.factor_job_knowledge
        this.factorWorkQualityCurrentVal = response.data.factor_work_quality
        this.factorWorkQuantityCurrentVal = response.data.factor_work_quantity
        this.factorWorkHabitsCurrentVal = response.data.factor_work_habits
        this.factorAnalysisCurrentVal = response.data.factor_analysis
        this.factorInitiativeCurrentVal = response.data.factor_initiative
        this.factorInterpersonalCurrentVal = response.data.factor_interpersonal
        this.factorCommunicationCurrentVal = response.data.factor_communication
        this.factorDependabilityCurrentVal = response.data.factor_dependability
        this.factorProfessionalismCurrentVal = response.data.factor_professionalism
        this.factorManagementCurrentVal = response.data.factor_management
        this.factorSupervisionCurrentVal = response.data.factor_supervision

        this.evaluationSuccessesCurrentVal = response.data.evaluation_successes
        this.evaluationOpportunitiesCurrentVal = response.data.evaluation_opportunities
        this.evaluationGoalsManagerCurrentVal = response.data.evaluation_goals_manager
        this.evaluationCommentsEmployeeCurrentVal = response.data.evaluation_comments_employee

        this.descriptionReviewedEmployeeCurrentVal = response.data.description_reviewed_employee

        this.signatures = response.data.all_required_signatures

        if (this.formErrorItems().length > 0) {
          this.showErrorButton = true
        }

        this.$store.dispatch('performanceReviewModule/getAllPerformanceReviewsActionRequired')
          .catch(e => {
            console.error('Error getting getAllPerformanceReviewsActionRequired after updaing PR:', e)
            reject(e)
          })
        this.$store.dispatch('performanceReviewModule/getAllPerformanceReviewsActionNotRequired')
          .catch(e => {
            console.error('Error getting getAllPerformanceReviewsActionNotRequired after updaing PR:', e)
            reject(e)
          })

        resolve()
      })
      .catch(e => {
        console.error('Error updating PR', e)
        reject(e)
      })
    })
  }

  private updateEmployeeComments(): void {
    PerformanceReviewDataService.updatePartial(this.prPk, {
      evaluation_comments_employee: this.evaluationCommentsEmployee,
    })
      .then((response: AxiosPerformanceReviewUpdateServerResponse) => {
        this.evaluationCommentsEmployeeCurrentVal = response.data.evaluation_comments_employee
      })
      .catch(e => {
        console.error('Error updaing employee comments:' ,e)
      })
  }

  private userCanSign(employeePk: number, employeeIsReadyToSign: boolean): boolean {
    const employeeIsCurrentUser = employeePk == this.currentUserPk()
    return employeeIsCurrentUser && employeeIsReadyToSign
  }

  private signPerformanceReview(): void {
    // PerformanceReviewDataService.signPerformanceReview(parseInt(this.pk), this.managerPk)
    this.$store.dispatch('performanceReviewModule/createSignature', {review_pk: this.prPk, employee_pk: this.currentUserPk()})
      .then(() => {
        this.updatePerformanceReview()
          .then(() => {
            this.retrievePerformanceReview()
              .catch(e => {
                console.error('Error retrieving PR after updating PR after signing PR:', e)
              })
            this.$store.dispatch('performanceReviewModule/getAllPerformanceReviewsActionRequired')
              .catch(e => {
                console.error('Error getting getAllPerformanceReviewsActionRequired after updating PR after signing PR:', e)
              })
            this.$store.dispatch('performanceReviewModule/getAllPerformanceReviewsActionNotRequired')
              .catch(e => {
                console.error('Error getting getAllPerformanceReviewsActionNotRequired after updating PR after signing PR:', e)
              })
          })
          .catch(e => {
            console.error('Error updating PR after signing PR:', e)
          })
      })
      .catch(e => {
        console.error('Error signing PR:', e)
      })
  }

  private noWeekends(date: string): boolean {
    const day = quasarDate.getDayOfWeek(new Date(date))
    return day !== 6 && day !== 7
  }

  private onClickNoteCard(pk: number): void {
    this.$router.push(`/note/${ pk }`)
      .catch(e => {
        console.error('Error navigating to PR note detail:', e)
      })
  }

  private file_selected(file: Array<File>) {
    this.selectedFile = file[0];
  }

  private uploadFile() {
    let fd = new FormData();
    fd.append('pk', this.prPk)
    fd.append('file', this.selectedFile)
    
    PerformanceReviewDataService.uploadSignedPositionDescription(fd)
      .then((response: SignedPositionDescriptionUploadServerResponse) => {
        if (response.statusText == 'OK') {
          this.$refs.fileuploader.reset() // eslint-disable-line
          this.uploadedPositionDescriptionUrl = response.data // eslint-disable-line
          this.fileSuccessfullyUploaded = true
          setTimeout(() => this.fileSuccessfullyUploaded = false, 5000)
          this.updatePerformanceReview()
            .catch(e => {
              console.error('Error updating PR after uploading signed position description:', e)
            })
        }
      })
      .catch(e => {
        console.error('Error uploading signed position description:', e)
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

  mounted() {
    this.retrievePerformanceReview()
      .then(() => {
        if (this.print) {
          setTimeout(() => window.print(), 200) // Wait briefly for logo image to load
        }
      })
      .catch(e => {
        console.error('Error retrieving PR on PR detail page mount:', e)
      })
  }
}
</script>

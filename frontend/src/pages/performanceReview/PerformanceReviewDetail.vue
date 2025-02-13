<template>
<q-page id="performance-review-detail-page">
  <div class="q-px-md">
    <!-- Logo appears in print view only -->
    <q-img
      id="lcog-logo"
      src="../../assets/lcog-banner.png"
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
          <div class="row">
            {{ readableDate(periodStartDate) }} -
            {{ readableDate(periodEndDate) }}
          </div>
      </div>
      <div class="eval-box eval-box-4">
          <div class="row text-bold">Effective Date:</div>
          <div class="row">{{ readableDate(effectiveDate) }}</div>
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
            <q-radio
              v-model="evaluationType"
              val="P"
              :disable="!currentUserIsManagerOfEmployee() ||
                employeeHasSigned()"
            />
            <div class="text-uppercase">Probat&shy;ionary:</div>
          </div>
          <div class="label-radio-pair">
            <q-radio
              v-model="probationaryEvaluationType"
              val="S"
              :disable="evaluationType != 'P' ||
                !currentUserIsManagerOfEmployee() || employeeHasSigned()"
            />
            <div>180 days</div>
          </div>
          <div class="label-radio-pair">
            <q-radio
              v-model="probationaryEvaluationType"
              val="N"
              :disable="evaluationType != 'P' ||
                !currentUserIsManagerOfEmployee() || employeeHasSigned()"
            />
            <div>6 months</div>
          </div>
        </div>
        <div class="eval-box-full-1-annual">
          <div class="label-radio-pair">
            <q-radio
              v-model="evaluationType"
              val="A"
              @input="() => probationaryEvaluationType = ''"
              :disable="!currentUserIsManagerOfEmployee() ||
                employeeHasSigned()"
            />
            <div class="text-uppercase">Annual</div>
          </div>
        </div>
      </div>
      <div class="row eval-box eval-box-full eval-box-full-2">
        <div class="text-uppercase text-bold">Action:</div>
        <div class="label-radio-triplet">
          <div class="text-bold" id="step-increase">Step Increase:</div>
          <q-radio
            v-model="stepIncrease"
            val="Y"
            :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
          />
          <div>Yes</div>
          <q-radio
            v-model="stepIncrease"
            val="N"
            :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
          />
          <div>No</div>
        </div>
        <div class="label-radio-triplet">
          <div class="text-bold" id="top-step-bonus">Top-Step Bonus</div>
          <q-radio
            v-model="topStepBonus"
            val="Y"
            :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
          />
          <div>Yes</div>
          <q-radio
            v-model="topStepBonus"
            val="N"
            :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
          />
          <div>No</div>
        </div>
        <div id="action-other">
          <q-input
            outlined
            v-model="actionOther"
            label="Other"
            :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
          />
        </div>
      </div>
    </div>

    <h5 class="text-h5 text-uppercase text-bold text-center q-my-md">
      <u>Employee Self-Evaluation</u>
    </h5>
    <div
      v-if="!currentUserIsEmployee() || employeeHasSigned() || props.print"
      class="read-only-text-area" v-html="evaluationCommentsEmployee"
    ></div>
    <q-editor
      v-else
      v-model="evaluationCommentsEmployee"
      :toolbar="editorToolbar"
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

    <div
      v-if="currentUserIsManagerOfEmployee()"
      id="notes"
    >
      <h5 class="text-h5 text-uppercase text-bold text-center q-my-md">
        <u>Peer Feedback</u>
      </h5>
      <div class="q-pa-md row items-center q-gutter-md">
        <q-icon name="forward_to_inbox" size="xl" color="primary" />
        <div>
          <div class="text-bold">
            Link: <a :href="peerFeedbackLink()">{{ peerFeedbackLink() }}</a>
          </div>
          <div>
            Send this link to anyone who may want to submit feedback for {{ employeeName }}.
          </div>
        </div>
      </div>
      
      <div class="q-pa-md row items-start q-gutter-md">
        <q-card
          v-for="note in reviewNotes"
          :key="note.pk"
          class="note-card"
        >
          <q-card-section>
            <div class="text-bold">
              {{ note.author_name }} - {{ readableDate(note.created_at) }}
            </div>
            <div class="read-only-text-area" v-html="note.note"></div>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <h5 class="text-uppercase text-center text-bold q-mb-sm q-mt-lg"><u>Rating Scale</u></h5>
    <div class="rating-grid-container">
      <div class="rating-box">
        <span class="text-bold">(1)*</span> Needs Improvement
      </div>
      <div class="rating-box">
        The employee’s work performance does not consistently meet the standards
        of the position. Serious effort is needed to improve performance.
      </div>
      <div class="rating-box">
        <span class="text-bold">(2)</span> Meets Job Requirments
      </div>
      <div class="rating-box">
        The employee’s work performance consistently meets the standards of the
        position.
      </div>
      <div class="rating-box">
        <span class="text-bold">(3)</span> Exceeds Job Requirments
      </div>
      <div class="rating-box">
        The employee’s work performance is frequently or consistently above the
        level of a satisfactory employee.
      </div>
      <div class="rating-box">
        <span class="text-bold">(N/A)</span> Not Applicable
      </div>
      <div class="rating-box">
        Does not pertain to the employee’s actual job duties.
      </div>
    </div>
    <div>
      *Factors rated <span class="text-bold">(1)</span> Needs improvement must
      be addressed with a plan for improvement.
    </div>

    <h5 class="text-uppercase text-bold q-my-md">
      <u>I. Performance Factors Reviewed</u>
    </h5>
    <div class="factors-grid-container">

      <!-- Desktop/Tablet Headers -->
      <div class="factors-header-box text-bold text-center
        factors-header-desktop factors-header-sticky"
      >
        Performance Factors Reviewed
      </div>
      <div class="factors-header-box text-bold text-center
        factors-header-desktop factors-header-sticky"
      >
        Needs Improvement
      </div>
      <div class="factors-header-box text-bold text-center
        factors-header-desktop factors-header-sticky"
      >
        Meets Job Requirements
      </div>
      <div class="factors-header-box text-bold text-center
        factors-header-desktop factors-header-sticky"
      >
        Exceeds Job Requirements
      </div>
      <div class="factors-header-box text-bold text-center
        factors-header-desktop factors-header-sticky"
      >
        Not Applicable
      </div>

      <!-- Mobile Headers -->
      <div class="factors-header-box text-bold text-center
        factors-header-mobile factors-header-sticky"
      >
        Performance Factors Reviewed
      </div>
      <div class="factors-header-box text-bold text-center
        factors-header-mobile factors-header-sticky"
      >
        Needs Improv&shy;ement
      </div>
      <div class="factors-header-box text-bold text-center
        factors-header-mobile factors-header-sticky"
      >
        Meets Job Require&shy;ments
      </div>
      <div class="factors-header-box text-bold text-center
        factors-header-mobile factors-header-sticky"
      >
        Exceeds Job Require&shy;ments
      </div>
      <div class="factors-header-box text-bold text-center
        factors-header-mobile factors-header-sticky"
      >
        Not Appli&shy;cable
      </div>

      <div class="factors-box" id="factor-job-knowledge">
          <div class="row text-bold"><u>Job Knowledge</u></div>
          <div class="row">
            Present knowledge of techniques, skills, procedures, technologies,
            equipment, rules and policies of position.
          </div>
      </div>
      <div class="factors-radio-box">
        <q-radio
          v-model="factorJobKnowledge"
          val="N"
          :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
        />
      </div>
      <div class="factors-radio-box">
        <q-radio
          v-model="factorJobKnowledge"
          val="M"
          :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
        />
      </div>
      <div class="factors-radio-box">
        <q-radio
          v-model="factorJobKnowledge"
          val="E"
          :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
        />
      </div>
      <div class="factors-radio-box">


      </div>
      <div class="factors-box">
          <div class="row text-bold" id="factor-work-quality">
            <u>Quality of Work</u>
          </div>
          <div class="row">
            Turns in high quality work and very seldom makes errors.
          </div>
      </div>
      <div class="factors-radio-box">
        <q-radio
          v-model="factorWorkQuality"
          val="N"
          :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
        />
      </div>
      <div class="factors-radio-box">
        <q-radio
          v-model="factorWorkQuality"
          val="M"
          :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
        />
      </div>
      <div class="factors-radio-box">
        <q-radio
          v-model="factorWorkQuality"
          val="E"
          :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
        />
      </div>
      <div class="factors-radio-box">


      </div>
      <div class="factors-box" id="factor-work-quantity">
          <div class="row text-bold"><u>Quantity of Work</u></div>
          <div class="row">Accomplishes stated goals and expectations.</div>
      </div>
      <div class="factors-radio-box">
        <q-radio
          v-model="factorWorkQuantity"
          val="N"
          :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
        />
      </div>
      <div class="factors-radio-box">
        <q-radio
          v-model="factorWorkQuantity"
          val="M"
          :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
        />
      </div>
      <div class="factors-radio-box">
        <q-radio
          v-model="factorWorkQuantity"
          val="E"
          :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
        />
      </div>
      <div class="factors-radio-box">


      </div>
      <div class="factors-box" id="factor-work-habits">
          <div class="row text-bold"><u>Work Habits</u></div>
          <div class="row">
            Uses equipment, supplies and time efficiently; punctual and on time.
          </div>
      </div>
      <div class="factors-radio-box">
        <q-radio
          v-model="factorWorkHabits"
          val="N"
          :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
        />
      </div>
      <div class="factors-radio-box">
        <q-radio
          v-model="factorWorkHabits"
          val="M"
          :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
        />
      </div>
      <div class="factors-radio-box">
        <q-radio
          v-model="factorWorkHabits"
          val="E"
          :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
        />
      </div>
      <div class="factors-radio-box">


      </div>
      <div class="factors-box" id="factor-analysis">
          <div class="row text-bold"><u>Analysis and Decision-Making</u></div>
          <div class="row">
            Has strong analytical abilities and makes sound judgements.
          </div>
      </div>
      <div class="factors-radio-box">
        <q-radio
          v-model="factorAnalysis"
          val="N"
          :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
        />
      </div>
      <div class="factors-radio-box">
        <q-radio
          v-model="factorAnalysis"
          val="M"
          :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
        />
      </div>
      <div class="factors-radio-box">
        <q-radio
          v-model="factorAnalysis"
          val="E"
          :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
        />
      </div>
      <div class="factors-radio-box">


      </div>
      <div class="factors-box" id="factor-initiative">
          <div class="row text-bold"><u>Initiative and Creativity</u></div>
          <div class="row">
            A self-starter and seeks new responsibilities and opportunities for
            leadership; demonstrates creativity in performing tasks and
            identifying resolutions.
          </div>
      </div>
      <div class="factors-radio-box">
        <q-radio
          v-model="factorInitiative"
          val="N"
          :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
        />
      </div>
      <div class="factors-radio-box">
        <q-radio
          v-model="factorInitiative"
          val="M"
          :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
        />
      </div>
      <div class="factors-radio-box">
        <q-radio
          v-model="factorInitiative"
          val="E"
          :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
        />
      </div>
      <div class="factors-radio-box">


      </div>
      <div class="factors-box" id="factor-interpersonal">
          <div class="row text-bold"><u>Interpersonal Relations</u></div>
          <div class="row">
            Presents good attitude, works well in teams, cooperates with others,
            and is thoughtful and courteous/polite.
          </div>
      </div>
      <div class="factors-radio-box">
        <q-radio
          v-model="factorInterpersonal"
          val="N"
          :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
        />
      </div>
      <div class="factors-radio-box">
        <q-radio
          v-model="factorInterpersonal"
          val="M"
          :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
        />
      </div>
      <div class="factors-radio-box">
        <q-radio
          v-model="factorInterpersonal"
          val="E"
          :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
        />
      </div>
      <div class="factors-radio-box">


      </div>
      <div class="factors-box" id="factor-communication">
          <div class="row text-bold"><u>Communication</u></div>
          <div class="row">
            Effectively communicates (oral and written) and keeps others
            appropriately informed.
          </div>
      </div>
      <div class="factors-radio-box">
        <q-radio
          v-model="factorCommunication"
          val="N"
          :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
        />
      </div>
      <div class="factors-radio-box">
        <q-radio
          v-model="factorCommunication"
          val="M"
          :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
        />
      </div>
      <div class="factors-radio-box">
        <q-radio
          v-model="factorCommunication"
          val="E"
          :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
        />
      </div>
      <div class="factors-radio-box">


      </div>
      <div class="factors-box" id="factor-dependability">
          <div class="row text-bold">
            <u>Dependability and Responsibility</u>
          </div>
          <div class="row">
            Completes assigned work within prescribed timelines; rarely needs
            direct supervision.
          </div>
      </div>
      <div class="factors-radio-box">
        <q-radio
          v-model="factorDependability"
          val="N"
          :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
        />
      </div>
      <div class="factors-radio-box">
        <q-radio
          v-model="factorDependability"
          val="M"
          :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
        />
      </div>
      <div class="factors-radio-box">
        <q-radio
          v-model="factorDependability"
          val="E"
          :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
        />
      </div>
      <div class="factors-radio-box">


      </div>
      <div class="factors-box" id="factor-professionalism">
          <div class="row text-bold">
            <u>Professionalism and Customer Service</u>
          </div>
          <div class="row">
            Presents and represents oneself and the agency in a positive manner;
            provides and delivers professional, helpful, high quality service
            and assistance.
          </div>
      </div>
      <div class="factors-radio-box">
        <q-radio
          v-model="factorProfessionalism"
          val="N"
          :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
        />
      </div>
      <div class="factors-radio-box">
        <q-radio
          v-model="factorProfessionalism"
          val="M"
          :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
        />
      </div>
      <div class="factors-radio-box">
        <q-radio
          v-model="factorProfessionalism"
          val="E"
          :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
        />
      </div>
      <div class="factors-radio-box">


      </div>
      <div class="factors-box" id="factor-management">
          <div class="row text-bold"><u>Project Management</u></div>
          <div class="row">
            Coordinates, delegates tasks to team members, and communicates
            internally and externally about projects; projects are high quality
            and are completed within timelines.
          </div>
      </div>
      <div class="factors-radio-box">
        <q-radio
          v-model="factorManagement"
          val="N"
          :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
        />
      </div>
      <div class="factors-radio-box">
        <q-radio
          v-model="factorManagement"
          val="M"
          :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
        />
      </div>
      <div class="factors-radio-box">
        <q-radio
          v-model="factorManagement"
          val="E"
          :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
        />
      </div>
      <div class="factors-radio-box">
        <q-radio
          v-model="factorManagement"
          val="NA"
          :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
        />
      </div>
      <div class="factors-box" id="factor-supervision">
          <div class="row text-bold"><u>Supervision</u></div>
          <div class="row">
            Provides support/guidance and motivation with open communication and
            transparency.
          </div>
      </div>
      <div class="factors-radio-box">
        <q-radio
          v-model="factorSupervision"
          val="N"
          :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
        />
      </div>
      <div class="factors-radio-box">
        <q-radio
          v-model="factorSupervision"
          val="M"
          :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
        />
      </div>
      <div class="factors-radio-box">
        <q-radio
          v-model="factorSupervision"
          val="E"
          :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
        />
      </div>
      <div class="factors-radio-box">
        <q-radio
          v-model="factorSupervision"
          val="NA"
          :disable="!currentUserIsManagerOfEmployee() || employeeHasSigned()"
        />
      </div>
    </div>

    <h5 class="text-uppercase text-bold q-my-md" id="evaluation-successes">
      <u>II. Employee's Successes</u>
    </h5>
    <div
      v-if="
        !currentUserIsManagerOfEmployee() || employeeHasSigned() || props.print
      "
      class="read-only-text-area" v-html="evaluationSuccesses"
    ></div>
    <q-editor
      v-else
      v-model="evaluationSuccesses"
      :toolbar="editorToolbar"
    />

    <h5 class="text-uppercase text-bold q-my-md" id="evaluation-opportunities">
      <u>III. Opportunities for Growth</u>
    </h5>
    <div
      v-if="
        !currentUserIsManagerOfEmployee() || employeeHasSigned() || props.print
      "
      class="read-only-text-area" v-html="evaluationOpportunities"
    ></div>
    <q-editor
      v-else
      v-model="evaluationOpportunities"
      :toolbar="editorToolbar"
    />

    <h5 class="text-uppercase text-bold q-my-md" id="evaluation-goals">
      <u>IV. Goals for the Coming Year</u>
    </h5>
    <div
      v-if="
        !currentUserIsManagerOfEmployee() || employeeHasSigned() || props.print
      "
      class="read-only-text-area" v-html="evaluationGoalsManager"
    ></div>
    <q-editor
      v-else
      v-model="evaluationGoalsManager"
      :toolbar="editorToolbar"
    />

    <!-- <h5 class="text-uppercase">V. Goals for the Coming Year (Employee)</h5>
    <q-input
      v-model="evaluationGoalsEmployee"
      type="textarea"
    /> -->

    <div
      v-for="(signature, index) in signatures"
      :key="index"
      class="row signature-block"
    >
      <div class="col">
        <div v-if="signature[1]" class="signature">
          <span class="signature-text">{{ signature[1] }}</span>
        </div>
        <div v-else class="signature">
          <q-btn
            v-if="userCanSign(signature[3], signature[4])"
            color="white"
            text-color="black"
            label="Click to Sign"
            @click="signPerformanceReview()"
            class="signature-button"
          />
          <div v-else>&nbsp;</div>
        </div>
        <div class="signature-type">
          <span class="text-bold">{{ signature[0] }} Signature</span>
          <span v-if="signature[0] == 'Employee'">
            <b>:</b><i class="q-ml-xs">
              I have reviewed this evaluation and discussed it further with my
              manager. Signing does not necessarily indicate agreement.
            </i>
          </span>
        </div>
      </div>
      <div class="col signature-date-block">
        <div v-if="signature[2]" class="signature-date">
          <span class="signature-date-text">
            {{ readableDate(signature[2]) }}
          </span>
        </div>
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

    <!-- Dialog of all error items -->
    <q-dialog v-model="showErrorDialog" :position="errorDialogPosition">
      <q-card style="width: 350px">
        <q-list bordered separator>
          <q-item
            v-for="(item, index) in formErrorItems()"
            :key="index"
            clickable
            @click="clickedErrorItem(item)"
          >
            <q-item-label>{{item[1]}}</q-item-label>
          </q-item>
        </q-list>
      </q-card>
    </q-dialog>

    <!-- Dialog for when you are done and have signed the PR -->
    <q-dialog v-model="showPRSignedAndCompleteDialog">
      <q-card>
        <q-card-section class="row items-center">
          <q-avatar icon="check" color="primary" text-color="white" />
          <div class="col">
            <span class="q-ml-sm row">
              Your signature has been recorded, and you're all done!
            </span>
            <span
              class="q-ml-sm row"
              v-if="nextPersonToSign() && !currentUserIsEmployee()"
            >
              {{ nextPersonToSign() }} will be notified to sign next.
            </span>
          </div>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" color="primary" v-close-popup />
          <q-btn
            flat
            label="Return to Dashboard"
            color="primary"
            @click="returnToDashboard()"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Spacing for footer -->
    <div style="height: 80px;"></div>

    <div
      id="sticky-footer"
      class="row justify-between"
      v-if="currentUserIsManagerOfEmployee()"
    >
      <q-btn
        id="update-button"
        class="col-1"
        color="white"
        text-color="black"
        label="Update"
        :disabled="!valuesAreChanged()"
        @click="updatePerformanceReview()"
      />
      <q-btn
        v-if="showErrorButton && formErrorItems().length > 0"
        label="Show missing fields"
        icon="check"
        color="warning"
        @click="openErrorDialog('right')"
      />
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
.read-only-text-area {
  white-space: pre-line;
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
    print-color-adjust: exact !important;                 /*Firefox*/
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
  #position-description-section {
    display: none;
  }
  .signature-block {
    margin: 0;
  }
  #sticky-footer {
    display: none;
  }
}
</style>

<script setup lang="ts">
import { scroll, useQuasar } from 'quasar'
import { onMounted, ref, Ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { readableDate } from 'src/filters'
import { usePerformanceReviewStore } from 'src/stores/performancereview'
import { useUserStore } from 'src/stores/user'
import { PRSignatures, ReviewNoteRetrieve } from 'src/types'
import { getRoutePk } from 'src/utils'


const $q = useQuasar()
const route = useRoute()
const router = useRouter()
const performanceReviewStore = usePerformanceReviewStore()
const userStore = useUserStore()
const { getScrollTarget, setVerticalScrollPosition } = scroll

const props = defineProps<{
  print?: boolean,
}>()

type PositionType = 'top' | 'standard' | 'right' | 'bottom' | 'left' | undefined

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

let factorJobKnowledgeCurrentVal = ref('')
let factorJobKnowledge = ref('')
let factorWorkQualityCurrentVal = ref('')
let factorWorkQuality = ref('')
let factorWorkQuantityCurrentVal = ref('')
let factorWorkQuantity = ref('')
let factorWorkHabitsCurrentVal = ref('')
let factorWorkHabits = ref('')
let factorAnalysisCurrentVal = ref('')
let factorAnalysis = ref('')
let factorInitiativeCurrentVal = ref('')
let factorInitiative = ref('')
let factorInterpersonalCurrentVal = ref('')
let factorInterpersonal = ref('')
let factorCommunicationCurrentVal = ref('')
let factorCommunication = ref('')
let factorDependabilityCurrentVal = ref('')
let factorDependability = ref('')
let factorProfessionalismCurrentVal = ref('')
let factorProfessionalism = ref('')
let factorManagementCurrentVal = ref('')
let factorManagement = ref('')
let factorSupervisionCurrentVal = ref('')
let factorSupervision = ref('')

let evaluationSuccessesCurrentVal = ref('')
let evaluationSuccesses = ref('')
let evaluationOpportunitiesCurrentVal = ref('')
let evaluationOpportunities = ref('')
let evaluationGoalsManagerCurrentVal = ref('')
let evaluationGoalsManager = ref('')
let evaluationCommentsEmployeeCurrentVal = ref('')
let evaluationCommentsEmployee = ref('')

let signatures: Ref<PRSignatures> = ref([['', '', new Date(), -1, false]])

let showErrorButton = ref(false)
let showErrorDialog = ref(false)
let errorDialogPosition: Ref<PositionType> = ref('standard')

let showPRSignedAndCompleteDialog = ref(false)

let reviewNotes = ref([]) as Ref<Array<ReviewNoteRetrieve>>

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

function currentUserIsManagerOfEmployee(): boolean {
  return managerPk.value == currentUserPk()
}

function employeeHasSigned(): boolean {
  return !!signatures.value[0][2]
}

function nextPersonToSign(): string {
  return userStore.getEmployeeProfile.next_to_sign_prs
}

function currentUserIsEmployee(): boolean {
  return employeePk.value == currentUserPk()
}

function peerFeedbackLink(): string {
  return `${ window.location.origin }/note/new?employee=${ employeePk.value }`
}

function valuesAreChanged(): boolean {
  if (
    evaluationType.value == evaluationTypeCurrentVal.value &&
    probationaryEvaluationType.value ==
      probationaryEvaluationTypeCurrentVal.value &&
    stepIncrease.value == stepIncreaseCurrentVal.value &&
    topStepBonus.value == topStepBonusCurrentVal.value &&
    actionOther.value == actionOtherCurrentVal.value &&
    factorJobKnowledge.value == factorJobKnowledgeCurrentVal.value &&
    factorWorkQuality.value == factorWorkQualityCurrentVal.value &&
    factorWorkQuantity.value == factorWorkQuantityCurrentVal.value &&
    factorWorkHabits.value == factorWorkHabitsCurrentVal.value &&
    factorAnalysis.value == factorAnalysisCurrentVal.value &&
    factorInitiative.value == factorInitiativeCurrentVal.value &&
    factorInterpersonal.value == factorInterpersonalCurrentVal.value &&
    factorCommunication.value == factorCommunicationCurrentVal.value &&
    factorDependability.value == factorDependabilityCurrentVal.value &&
    factorProfessionalism.value == factorProfessionalismCurrentVal.value &&
    factorManagement.value == factorManagementCurrentVal.value &&
    factorSupervision.value == factorSupervisionCurrentVal.value &&
    evaluationSuccesses.value == evaluationSuccessesCurrentVal.value &&
    evaluationOpportunities.value == evaluationOpportunitiesCurrentVal.value &&
    evaluationGoalsManager.value == evaluationGoalsManagerCurrentVal.value &&
    evaluationCommentsEmployee.value ==
      evaluationCommentsEmployeeCurrentVal.value
  ) {
    return false
  } else {
    return true
  }
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

function formErrorItems(): Array<[string, string]> {
  let errorItems: Array<[string, string]> = []
  if (!stepIncreaseCurrentVal.value) {
    errorItems.push(['step-increase', 'Select Step Increase'])
  }
  if (!topStepBonusCurrentVal.value) {
    errorItems.push(['top-step-bonus', 'Select Top Step Bonus'])
  }
  if (!factorJobKnowledgeCurrentVal.value) {
    errorItems.push(['factor-job-knowledge', 'Evaluate Job Knowledge'])
  }
  if (!factorWorkQualityCurrentVal.value) {
    errorItems.push(['factor-work-quality', 'Evaluate Quality of Work'])
  }
  if (!factorWorkQuantityCurrentVal.value) {
    errorItems.push(['factor-work-quantity', 'Evaluate Quantity of Work'])
  }
  if (!factorWorkHabitsCurrentVal.value) {
    errorItems.push(['factor-work-habits', 'Evaluate Work Habits'])
  }
  if (!factorAnalysisCurrentVal.value) {
    errorItems.push(
      ['factor-analysis', 'Evaluate Analysis and Decision-Making']
    )
  }
  if (!factorInitiativeCurrentVal.value) {
    errorItems.push(['factor-initiative', 'Evaluate Initiative and Creativity'])
  }
  if (!factorInterpersonalCurrentVal.value) {
    errorItems.push(
      ['factor-interpersonal', 'Evaluate Interpersonal Relations']
    )
  }
  if (!factorCommunicationCurrentVal.value) {
    errorItems.push(['factor-communication', 'Evaluate Communication'])
  }
  if (!factorDependabilityCurrentVal.value) {
    errorItems.push(
      ['factor-dependability', 'Evaluate Dependability and Responsibility']
    )
  }
  if (!factorProfessionalismCurrentVal.value) {
    errorItems.push(
      [
        'factor-professionalism',
        'Evaluate Professionalism and Customer Service'
      ]
    )
  }
  if (!factorManagementCurrentVal.value) {
    errorItems.push(['factor-management', 'Evaluate Project Management'])
  }
  if (!factorSupervisionCurrentVal.value) {
    errorItems.push(['factor-supervision', 'Evaluate Supervision'])
  }
  if (!evaluationSuccessesCurrentVal.value) {
    errorItems.push(['evaluation-successes', 'Write Employee Successes'])
  }
  if (!evaluationOpportunitiesCurrentVal.value) {
    errorItems.push(
      ['evaluation-opportunities', 'Write Opportunities for Growth']
    )
  }
  if (!evaluationGoalsManagerCurrentVal.value) {
    errorItems.push(['evaluation-goals', 'Write Goals for the Coming Year'])
  }
  return errorItems
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

          retrieveReviewNotes()

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

          factorJobKnowledge.value = pr.factor_job_knowledge
          factorJobKnowledgeCurrentVal.value = factorJobKnowledge.value
          factorWorkQuality.value = pr.factor_work_quality
          factorWorkQualityCurrentVal.value = factorWorkQuality.value
          factorWorkQuantity.value = pr.factor_work_quantity
          factorWorkQuantityCurrentVal.value = factorWorkQuantity.value
          factorWorkHabits.value = pr.factor_work_habits
          factorWorkHabitsCurrentVal.value = factorWorkHabits.value
          factorAnalysis.value = pr.factor_analysis
          factorAnalysisCurrentVal.value = factorAnalysis.value
          factorInitiative.value = pr.factor_initiative
          factorInitiativeCurrentVal.value = factorInitiative.value
          factorInterpersonal.value = pr.factor_interpersonal
          factorInterpersonalCurrentVal.value = factorInterpersonal.value
          factorCommunication.value = pr.factor_communication
          factorCommunicationCurrentVal.value = factorCommunication.value
          factorDependability.value = pr.factor_dependability
          factorDependabilityCurrentVal.value = factorDependability.value
          factorProfessionalism.value = pr.factor_professionalism
          factorProfessionalismCurrentVal.value = factorProfessionalism.value
          factorManagement.value = pr.factor_management
          factorManagementCurrentVal.value = factorManagement.value
          factorSupervision.value = pr.factor_supervision
          factorSupervisionCurrentVal.value = factorSupervision.value

          evaluationSuccesses.value = pr.evaluation_successes
          evaluationSuccessesCurrentVal.value = evaluationSuccesses.value
          evaluationOpportunities.value = pr.evaluation_opportunities
          evaluationOpportunitiesCurrentVal.value =
            evaluationOpportunities.value
          evaluationGoalsManager.value = pr.evaluation_goals_manager
          evaluationGoalsManagerCurrentVal.value = evaluationGoalsManager.value
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

function retrieveReviewNotes(): void {
  performanceReviewStore.getAllRecentNotesForEmployee(
    employeePk.value.toString()
  )
    .then((notes: Array<ReviewNoteRetrieve>) => {
      reviewNotes.value = notes
    })
    .catch(e => {
      console.error('Error retrieving reivew notes from API:', e)
    })
}

function updatePerformanceReview() {
  return new Promise((resolve, reject) => {
    performanceReviewStore.updatePerformanceReview(prPk.value.toString(), {
      evaluation_type: evaluationType.value,
      probationary_evaluation_type: probationaryEvaluationType.value,
      step_increase: stepIncrease.value,
      top_step_bonus: topStepBonus.value,
      action_other: actionOther.value,
      factor_job_knowledge: factorJobKnowledge.value,
      factor_work_quality: factorWorkQuality.value,
      factor_work_quantity: factorWorkQuantity.value,
      factor_work_habits: factorWorkHabits.value,
      factor_analysis: factorAnalysis.value,
      factor_initiative: factorInitiative.value,
      factor_interpersonal: factorInterpersonal.value,
      factor_communication: factorCommunication.value,
      factor_dependability: factorDependability.value,
      factor_professionalism: factorProfessionalism.value,
      factor_management: factorManagement.value,
      factor_supervision: factorSupervision.value,
      evaluation_successes: evaluationSuccesses.value,
      evaluation_opportunities: evaluationOpportunities.value,
      evaluation_goals_manager: evaluationGoalsManager.value,
      evaluation_comments_employee: evaluationCommentsEmployee.value
    })
    .then((pr) => {
      status.value = pr.status

      evaluationTypeCurrentVal.value = pr.evaluation_type
      probationaryEvaluationTypeCurrentVal.value =
        pr.probationary_evaluation_type
      stepIncreaseCurrentVal.value = pr.step_increase
      topStepBonusCurrentVal.value = pr.top_step_bonus
      actionOtherCurrentVal.value = pr.action_other

      factorJobKnowledgeCurrentVal.value = pr.factor_job_knowledge
      factorWorkQualityCurrentVal.value = pr.factor_work_quality
      factorWorkQuantityCurrentVal.value = pr.factor_work_quantity
      factorWorkHabitsCurrentVal.value = pr.factor_work_habits
      factorAnalysisCurrentVal.value = pr.factor_analysis
      factorInitiativeCurrentVal.value = pr.factor_initiative
      factorInterpersonalCurrentVal.value = pr.factor_interpersonal
      factorCommunicationCurrentVal.value = pr.factor_communication
      factorDependabilityCurrentVal.value = pr.factor_dependability
      factorProfessionalismCurrentVal.value = pr.factor_professionalism
      factorManagementCurrentVal.value = pr.factor_management
      factorSupervisionCurrentVal.value = pr.factor_supervision

      evaluationSuccessesCurrentVal.value = pr.evaluation_successes
      evaluationOpportunitiesCurrentVal.value = pr.evaluation_opportunities
      evaluationGoalsManagerCurrentVal.value = pr.evaluation_goals_manager
      evaluationCommentsEmployeeCurrentVal.value =
        pr.evaluation_comments_employee

      signatures.value = pr.all_required_signatures

      if (formErrorItems().length > 0) {
        showErrorButton.value = true
      }

      performanceReviewStore.getAllPerformanceReviewsActionRequired()
      performanceReviewStore.getAllPerformanceReviewsActionNotRequired()

      resolve('Updated')
    })
    .catch(e => {
      console.error('Error updating PR', e)
      reject(e)
    })
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

function userCanSign(
  employeePk: number, employeeIsReadyToSign: boolean
): boolean {
  const employeeIsCurrentUser = employeePk == currentUserPk()
  return employeeIsCurrentUser && employeeIsReadyToSign
}

function signPerformanceReview(): void {
  performanceReviewStore.createSignature({
    review_pk: prPk.value,
    employee_pk: currentUserPk()
  })
    .then(() => {
      updatePerformanceReview()
        .then(() => {
          retrievePerformanceReview()
          performanceReviewStore.getAllPerformanceReviewsActionRequired()
          performanceReviewStore.getAllPerformanceReviewsActionNotRequired()
          showPRSignedAndCompleteDialog.value = true
        })
        .catch(e => {
          console.error('Error updating PR after signing PR:', e)
        })
    })
}

// import { date as quasarDate } from 'quasar'
// function noWeekends(date: string): boolean {
//   const day = quasarDate.getDayOfWeek(new Date(date))
//   return day !== 6 && day !== 7
// }

function openErrorDialog(position: PositionType) {
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

function returnToDashboard(): void {
  router.push('/')
    .catch(e => {
      console.error('Error navigating to dashboard:', e)
    })
}

onMounted(() => {
  retrievePerformanceReview()
    .then(() => {
      if (props.print) {
        window.print()
      }
    })
    .catch(e => {
      console.error('Error retrieving PR on PR detail page mount:', e)
    })
})
</script>

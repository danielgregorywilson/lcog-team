<template>
  <q-page class="q-pa-md">
    <p>All Staff,</p>
    <p>This is a friendly reminder to be vigilant against Cybercrime. Cybercrime is one of the biggest risks not only for organizations but also individuals. Cybercriminals never sleep and constantly make attempt to steal confidential data or hijack the entire system. The financial damage of Cybercrime tops millions of dollars for organization and thousands of dollars for individuals. The common denominator is that they do not care who you are, and the damage will not be small if you are affected.</p>
    <p>Cybercriminals utilize many different tactics to infiltrate our private digital assets. The most common tool they leverage is email. This is because all they need to do is craft and send malicious emails out to random or targeted victims and wait for them to react and step in the trap.</p>
    <p>The good news is that we can prevent falling into the trap of malicious emails by paying a little attention to the emails we receive.  Here is a few tips.</p>
    <ol>
      <li>
        <p><strong>Check the source:</strong> Emails come either from internal (LCOG) or external (Internet) sources. It is good practice to first check if an email came from internal or external source. In general, emails from outside the organization have more risks. LCOG's email system appends the alert (highlighted below in yellow) on all external source emails to help draw your attention.</p>
        <img src="../assets/security-message/image-1.png" />
      </li>
      <li>
        <p><strong>Check the sender:</strong> Cybercriminals send malicious emails disguised as a trusted external or internal sender. LCOG's email system alerts you as described above if such an email comes from an outside source but it’s a good habit to verify the sender's email address in case you use an email system with no such protection. The following tricks are commonly used by Cybercriminals to impersonate trusted sources.</p>
        <p>Ex 1: The sender’s display name appears to be legitimate but the email address is bogus</p>
        <img src="../assets/security-message/image-2.png" />
        <p>Ex 2: The sender’s email address looks legitimate at a glance but it is not if you look carefully</p>
        <img src="../assets/security-message/image-3.png" />
        <p>Ex 3: The sender appears to be an LCOG employee, but it came from outside</p>
        <img src="../assets/security-message/image-4.png" />
      </li>
      <li><strong>Do not open attachments:</strong> It goes without saying “never open email attachments from an unknown sender” but it is prudent to always check the sender’s legitimacy as described previously to make sure it is from known trusted sources.</li>
      <li>
        <p><strong>Do not click links:</strong> Cybercriminals plant landmines in the embedded links of an email's body. They can easily disguise the appearance of the links. You can tell where the link points to by hovering your cursor over the link. It will display the real address in a pop-up window. LCOG's email system checks and blocks all "known" malicious links. However, it is a good practice to remember what you see is not always what you think they are.</p>
        <img src="../assets/security-message/image-5.png" />
      </li>
      <li><strong>Check the context:</strong> Pay attention to email context such as spelling, grammar, and language tone to help determine the authenticity of the email. Cybercriminals leverage the sense of urgency, fear, and greed, and use an authoritative tone to entice or agitate you.</li>
      <li><strong>Do not reply:</strong> Cybercriminals try to trick you one way or another to draw your attention. Never reply to suspicious emails.</li>
      <li><strong>Get help:</strong> Contact LCOG Information Services using the Helpdesk ticketing system for help if you are unsure what to do.</li>
      <li><strong>Lastly:</strong> It is very important to immediately report to LCOG IS team if you open a malicious link or an attachment. It helps the team to scope damage and minimize the impact.</li>
    </ol>
    <p>When it comes to cybersecurity, it is wise to think the threats are always around the corner. And with a proper caution, we can minimize the risk. We ask all of you to be diligent with emails whether they look legitimate or suspicious.</p>
    <p>Please verify below that you have read and understood this message. Thank you for your time!</p>
    <form>
      <div class="row items-center q-gutter-sm">
        <q-checkbox v-model="acknowledge" />
        <span>I acknowledge I have read and understood this notification</span>
      </div>
      <div class="row items-center q-gutter-sm">
        <q-btn :disabled="!acknowledge"  @click="submitAcknowledgement()">Submit</q-btn>
        <span class="thanks q-ml-sm q-mt-sm" :hidden="!showThanksMessage"><strong>Thank you! Your response has been recorded.</strong></span>
      </div>
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
import ReviewNoteTable from '../components/ReviewNoteTable.vue';
import PerformanceReviewTable from '../components/PerformanceReviewTable.vue';
import { PerformanceReviewRetrieve } from '../store/types'

@Component({
  components: { PerformanceReviewTable, ReviewNoteTable }
})
export default class Dashboard extends Vue {
  private acknowledge = false
  private showThanksMessage = false
  private hasSubmitted = false
  
  private submitAcknowledgement(): void {
    // TODO
    // this.$store.dispatch('')
    if (!this.hasSubmitted) {
      this.showThanksMessage = true
      this.hasSubmitted = true
    }
  }

  // private signPerformanceReview(): void {
  //   // PerformanceReviewDataService.signPerformanceReview(parseInt(this.pk), this.managerPk)
  //   this.$store.dispatch('performanceReviewModule/createSignature', {review_pk: this.prPk, employee_pk: this.currentUserPk()})
  //     .then(() => {
  //       this.updatePerformanceReview()
  //         .then(() => {
  //           this.retrievePerformanceReview()
  //             .catch(e => {
  //               console.error('Error retrieving PR after updating PR after signing PR:', e)
  //             })
  //           this.$store.dispatch('performanceReviewModule/getAllPerformanceReviewsActionRequired')
  //             .catch(e => {
  //               console.error('Error getting getAllPerformanceReviewsActionRequired after updating PR after signing PR:', e)
  //             })
  //           this.$store.dispatch('performanceReviewModule/getAllPerformanceReviewsActionNotRequired')
  //             .catch(e => {
  //               console.error('Error getting getAllPerformanceReviewsActionNotRequired after updating PR after signing PR:', e)
  //             })
  //           this.showPRSignedAndCompleteDialog = true
  //         })
  //         .catch(e => {
  //           console.error('Error updating PR after signing PR:', e)
  //         })
  //     })
  //     .catch(e => {
  //       console.error('Error signing PR:', e)
  //     })
  // }
  
  private isManager(): boolean {
    return this.$store.getters['userModule/getEmployeeProfile'].is_manager // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-return
  }

  private isUpperManager(): boolean {
    return this.$store.getters['userModule/getEmployeeProfile'].is_upper_manager // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-return
  }

  private isTheHRManager(): boolean {
    return this.$store.getters['userModule/getEmployeeProfile'].is_hr_manager // eslint-disable-line
  }

  private isTheExecutiveDirector(): boolean {
    return this.$store.getters['userModule/getEmployeeProfile'].is_executive_director // eslint-disable-line
  }

  private getNextReview(): PerformanceReviewRetrieve {
    return this.$store.getters['performanceReviewModule/nextPerformanceReview'] // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-return
  }

  private nextReviewNeedsEvaluation(): boolean {
    return this.getNextReview().status == 'Needs evaluation'
  }

  private userSignedNextEvaluation(): boolean {
    // Return if there is a date for the employee's signature on the review
    if (this.getNextReview().all_required_signatures) {
      return !!this.getNextReview().all_required_signatures[0][2]
    } else {
      return false
    }
  }

  private viewReview(pk: number): void {
    this.$router.push(`pr/${ pk }`)
      .catch(e => {
        console.error('Error navigating to PR detail', e)
      })
  }
};
</script>

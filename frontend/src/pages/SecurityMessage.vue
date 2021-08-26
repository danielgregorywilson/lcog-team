<template>
  <q-page class="q-pa-md">
    <div v-html="message"></div>
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
import { PerformanceReviewRetrieve } from '../store/types'
import SecurityMessageDataService from '../services/SecurityMessageDataService'

@Component
export default class SecurityMessage extends Vue {
  private message = ''
  private acknowledge = false
  private showThanksMessage = false
  private hasSubmitted = false
  
  private retrieveLatestSecurityMessage(): void {
    SecurityMessageDataService.getLatestSecurityMessage()
      .then(response => {
        this.message = response.data.content
      })
      .catch(e => {
        console.error('Error retrieving latest security message from API:', e)
      })
  }

  private submitAcknowledgement(): void {
    // TODO
    // this.$store.dispatch('')
    if (!this.hasSubmitted) {
      this.showThanksMessage = true
      this.hasSubmitted = true
    }
  }

  mounted() {
    this.retrieveLatestSecurityMessage()
      .catch(e => {
        console.error('Error retrieving latest Security Message:', e)
      })
  }

};
</script>

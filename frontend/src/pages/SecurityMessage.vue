<template>
  <q-page class="q-pa-md">
    <div v-html="message"></div>
    <form>
      <div class="row items-center q-gutter-sm">
        <q-checkbox v-model="acknowledge" :disable="hasViewedCurrentSecurityMessage()" />
        <span>I acknowledge I have read and understood this notification</span>
      </div>
      <div class="row items-center q-gutter-sm">
        <q-btn :disabled="hasViewedCurrentSecurityMessage()" @click="submitAcknowledgement()">Submit</q-btn>
        <span class="thanks q-ml-sm q-mt-sm" :hidden="!hasViewedCurrentSecurityMessage()"><strong>Thank you! Your response has been recorded.</strong></span>
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
import SecurityMessageDataService from '../services/SecurityMessageDataService'

@Component
export default class SecurityMessage extends Vue {
  private message = ''
  private securityMessagePk = -1
  private acknowledge = false
  
  private currentUserPk(): number {
    return this.$store.getters['userModule/getEmployeeProfile'].pk // eslint-disable-line @typescript-eslint/no-unsafe-return, @typescript-eslint/no-unsafe-member-access
  }

  private hasViewedCurrentSecurityMessage(): boolean {
    return this.$store.getters['securityMessageModule/viewedLatestSecurityMessage']
  }

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

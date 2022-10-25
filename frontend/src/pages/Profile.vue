<template>
  <q-page class="q-pa-md">
    <p class="text-h5">Update Your Profile</p>
    <form>
      <!-- DISPLAY NAME -->
      <p class="row text-h6 q-mt-lg q-mb-none">Display Name</p>
      <div class="row items-center q-gutter-sm">
        <q-input v-model="displayName" />
      </div>
      
      <p class="row text-h6 q-mt-lg q-mb-none">Email Notifications</p>
      <!-- ALL EMAILS -->
      <p class="row q-mb-none text-bold">All</p>
      <div class="row items-center q-gutter-sm">
        <q-toggle
          v-model="emailOptOutAll"
          color="negative"
          checked-icon="clear"
          unchecked-icon="mail"
          :label="emailOptOutAll ? 'Opt out of all email notifications' : 'Receive email notifications'"
          class="text-bold"
        />
      </div>
      <hr/>
      <!-- TIMEOFF EMAILS -->
      <p class="row q-mb-none text-bold">Time Off</p>
      <div class="row items-center q-gutter-sm">
        <q-toggle
          v-model="emailOptOutTimeOffAll"
          color="negative"
          checked-icon="clear"
          unchecked-icon="mail"
          :label="emailOptOutTimeOffAll ? 'Opt out of all time off email notifications' : 'Receive time off email notifications'"
          class="text-bold"
          :disable="emailOptOutAll"
        />
      </div>
      <div class="row items-center q-gutter-sm">
        <q-toggle
          v-model="emailOptOutTimeOffWeekly"
          color="negative"
          checked-icon="clear"
          unchecked-icon="mail"
          :label="emailOptOutTimeOffWeekly ? 'Opt out of weekly time off email notifications' : 'Receive weekly time off email notifications'"
          :disable="emailOptOutAll || emailOptOutTimeOffAll"
        />
      </div>
      <div class="row items-center q-gutter-sm">
        <q-toggle
          v-model="emailOptOutTimeOffDaily"
          color="negative"
          checked-icon="clear"
          unchecked-icon="mail"
          :label="emailOptOutTimeOffDaily ? 'Opt out of daily time off email notifications' : 'Receive daily time off email notifications'"
          :disable="emailOptOutAll || emailOptOutTimeOffAll"
        />
      </div>
      <div class="row items-center q-gutter-sm q-mt-sm">
        <q-btn :disabled="submitted" @click="submitProfileForm()">Submit</q-btn>
        <span class="success q-ml-sm q-mt-sm" :hidden="!submitted"><strong>Profile Updated.</strong></span>
      </div>
    </form>
  </q-page>
</template>

<style scoped>
.q-input {
  width: 300px;
}

.success {
    color: green;
}
</style>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import EmployeeDataService from '../services/EmployeeDataService'
import { AxiosEmployeeRetrieveOneServerResponse, VuexStoreGetters } from '../store/types'

@Component
export default class Profile extends Vue {
  private getters = this.$store.getters as VuexStoreGetters
  
  public displayName = ''
  public emailOptOutAll = false
  public emailOptOutTimeOffAll = false
  public emailOptOutTimeOffWeekly = false
  public emailOptOutTimeOffDaily = false

  private employeePk = -1
  public submitted = false

  private retrieveProfile(): Promise<AxiosEmployeeRetrieveOneServerResponse> {
    return new Promise((resolve, reject) => {
      // We cannot guarantee the user has arrived in vuex state immediately, so request it again here
      this.$store.dispatch('userModule/simpleUserRequest')
        .then((simpleUserresponse: AxiosEmployeeRetrieveOneServerResponse) => {
          // Now that we have the user's pk, get or create a Telework Application for that user
          this.displayName = simpleUserresponse.data.name
          this.employeePk = simpleUserresponse.data.pk
          this.emailOptOutAll = simpleUserresponse.data.email_opt_out_all
          this.emailOptOutTimeOffAll = simpleUserresponse.data.email_opt_out_timeoff_all
          this.emailOptOutTimeOffWeekly = simpleUserresponse.data.email_opt_out_timeoff_weekly
          this.emailOptOutTimeOffDaily = simpleUserresponse.data.email_opt_out_timeoff_daily
        })
        .catch(e => {
          console.error('Error getting user from API:', e)
          reject(e)
        })
    })
  }

  public submitProfileForm(): void {
    EmployeeDataService.updatePartial(this.employeePk, {
      display_name: this.displayName,
      email_opt_out_all: this.emailOptOutAll,
      email_opt_out_timeoff_all: this.emailOptOutTimeOffAll,
      email_opt_out_timeoff_weekly: this.emailOptOutTimeOffWeekly,
      email_opt_out_timeoff_daily: this.emailOptOutTimeOffDaily
    })
      .then(() => {
        this.$store.dispatch('userModule/userRequest')
        .catch(e => {
          console.error('Error getting user from store', e)
        })
        this.submitted = true
        setTimeout(() => this.submitted = false, 3000)
      })
      .catch(e => {
        console.error('Error updating employee profile settings:', e)
      })
  }

  mounted() { 
    this.retrieveProfile()
      .catch(e => {
        console.error('Error retrieving Employee profile from API:', e)
      })
  }

};
</script>

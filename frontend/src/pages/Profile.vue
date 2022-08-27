<template>
  <q-page class="q-pa-md">
    <p class="text-h5">Update Your Profile</p>
    <form>
      <div class="row items-center q-gutter-sm">
        <q-input v-model="displayName" label="Display Name" stack-label />
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
export default class SecurityMessage extends Vue {
  private getters = this.$store.getters as VuexStoreGetters
  
  private displayName = ''
  private employeePk = -1
  private submitted = false

  private retrieveProfile(): Promise<AxiosEmployeeRetrieveOneServerResponse> {
    return new Promise((resolve, reject) => {
      // We cannot guarantee the user has arrived in vuex state immediately, so request it again here
      this.$store.dispatch('userModule/simpleUserRequest')
        .then((simpleUserresponse: AxiosEmployeeRetrieveOneServerResponse) => {
          // Now that we have the user's pk, get or create a Telework Application for that user
          this.displayName = simpleUserresponse.data.name
          this.employeePk = simpleUserresponse.data.pk
        })
        .catch(e => {
          console.error('Error getting user from API:', e)
          reject(e)
        })
    })
  }

  private submitProfileForm(): void {
    EmployeeDataService.updatePartial(this.employeePk, {display_name: this.displayName})
      .then(() => {
        this.$store.dispatch('userModule/userRequest')
        .catch(e => {
          console.error('Error getting user from store', e)
        })
        this.submitted = true
        setTimeout(() => this.submitted = false, 3000)
      })
      .catch(e => {
        console.error('Error retrieving latest security message from API:', e)
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

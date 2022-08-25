<template>
  <q-page class="q-pa-md">
    <p class="text-h5">Update Your Profile</p>
    <form>
      <div class="row items-center q-gutter-sm">
        <q-input v-model="currentUserName" label="Display Name" stack-label />
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
import { VuexStoreGetters } from '../store/types'

@Component
export default class SecurityMessage extends Vue {
  private getters = this.$store.getters as VuexStoreGetters
  
  private displayName = ''
  private employeeNumber = -1
  private submitted = false
  
  private currentUserPk = this.$store.getters['userModule/getEmployeeProfile'].pk
  private currentUserName = this.$store.getters['userModule/getEmployeeProfile'].name

  private submitProfileForm(): void {
    EmployeeDataService.updateProfile(this.currentUserPk)
      .then(response => {
        this.submitted = true
        setTimeout(() => this.submitted = false, 3000)
      })
      .catch(e => {
        console.error('Error retrieving latest security message from API:', e)
      })
  }

  mounted() { 
    this.retrieveEmployeeProfile()
  }

};
</script>

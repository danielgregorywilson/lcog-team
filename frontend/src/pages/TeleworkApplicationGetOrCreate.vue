<template>
  <q-page>
    <q-spinner-grid
      class="spinner"
      color="primary"
      size="xl"
    />
  </q-page>
</template>

<style scoped lang="scss">
.spinner {
  position: fixed;
  top: 50%;
  left: 50%;
}
</style>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { AxiosTeleworkApplicationRetrieveOneServerResponse, AxiosEmployeeRetrieveOneServerResponse } from '../store/types'

@Component
export default class TeleworkApplicationGetOrCreate extends Vue {

  private getOrCreateTeleworkApplication(): Promise<AxiosTeleworkApplicationRetrieveOneServerResponse> {
    return new Promise((resolve, reject) => {
      // We cannot guarantee the user has arrived in vuex state immediately, so request it again here
      this.$store.dispatch('userModule/simpleUserRequest')
        .then((simpleUserresponse: AxiosEmployeeRetrieveOneServerResponse) => {
          // Now that we have the user's pk, get or create a Telework Application for that user
          this.$store.dispatch('teleworkModule/getOrCreateTeleworkApplicationByEmployee', {employeePk: simpleUserresponse.data.pk})
            .then((teleworkApplicationResponse) => {
              // Now that we've created the Telework Application, get the user again to refresh the applications they can view
              // TODO: Write an action to just update telework_applications_can_view 
              this.$store.dispatch('userModule/userRequest')
                .then(() => {
                  resolve(teleworkApplicationResponse)
                })
                .catch(e => {
                  console.error('Error getting user from API:', e)
                  reject(e)
                })
            })
            .catch(e => {
              console.error('Error getting or creating Telework Application from API:', e)
              reject(e)
            })
        })
        .catch(e => {
          console.error('Error getting user from API:', e)
          reject(e)
        })
    })
  }

  mounted() {
    this.getOrCreateTeleworkApplication()
      .then(response => {
        this.$router.push(`/telework-application/${ response.data.pk }`)
          .catch(e => {
            console.error('Error navigating to telework application detail:', e)
          })
      })
      .catch(e => {
        console.error('Error getting or creating Telework Application from API:', e)
      })
  }

};
</script>

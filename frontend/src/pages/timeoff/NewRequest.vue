<template>
  <div>
    <div class="q-gutter-md">
      <q-date v-model="dates" range/>
    </div>
    <q-input
        v-model="note"
        label="Note"
        class="q-pb-md"
      />
    <q-btn id="review-note-create-button" color="white" text-color="black" label="Create" :disabled="!formIsFilled()" @click="createTimeOffRequest()" />
  </div>
</template>

<style lang="scss">

</style>

<script lang="ts">
import { Notify } from 'quasar'
import { Component, Vue } from 'vue-property-decorator'
import { TimeOffRequestDates, VuexStoreGetters } from '../../store/types'

@Component
export default class TimeOffRequest extends Vue {
  private getters = this.$store.getters as VuexStoreGetters

  private dates: TimeOffRequestDates = []
  private note = ''

  private formIsFilled(): boolean {
    if (!!this.dates) {
      return true
    } else {
      return false
    }
  }

  private createTimeOffRequest(): void {
    // setTimeout(() => {
    //   this.dates = []
    //   this.note = ''
    //   Notify.create('Your request has been submitted')
    // }, 500)
    
    this.$store.dispatch('timeOffModule/createTimeOffRequest', {dates: this.dates, note: this.note})
      .then(() => {
        Notify.create('Created a new time off request.')
        this.$router.push({ name: 'timeoff-my-requests'})
          .then(() => {
            // location.reload() // TODO: This seems to be necessary in order to immediately edit a review note after creating it.
          })
          .catch(e => {
            console.error('Error navigating to dashboard after creating review note:', e)
          })
      })
      .catch(e => {
        console.error('Error creating review note:', e)
      })
  }

  // private upcomingTimeOff(): Array<TimeOff> {
  //   return this.getters['timeOffModule/upcomingTimeOff'].results
  // }

  // private retrieveUpcomingTimeOff(): void {
  //   this.$store.dispatch('timeOffModule/getUpcomingTimeOff')
  //     .catch(e => {
  //       console.error('Error retrieving upcoming time off', e)
  //     })
  // }

  mounted() {
    // this.retrieveUpcomingTimeOff()
  }
}
</script>

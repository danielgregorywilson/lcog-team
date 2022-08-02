<template>
  <div>
    <div class="q-gutter-md row">
      <q-date v-model="dates" range @input="dateChanged()"/>
      <div v-if="touchedCalendar && conflictingResponsibilityBuddies().length != 0">
        <q-icon color="orange" name="warning" size="xl" class="q-ml-sm" />
        <div>
          <div>One or more team members with shared responsibilities will be also be unavailable:</div>
          <ul>
            <li v-for="employee of conflictingResponsibilityBuddies()" :key="employee.pk">
              <router-link :to="{ name: 'employee-responsibilities', params: { pk: employee.pk } }">{{ employee.name }}</router-link>: {{ employee.responsibility_names[0] }}<span v-if="employee.responsibility_names.length > 1"> and {{ employee.responsibility_names.length - 1 }} more</span>
            </li>
          </ul>
        </div>
      </div>
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
import { TimeOffRequestDates, TimeOffRequestRetrieve, VuexStoreGetters } from '../../store/types'

@Component
export default class TimeOffRequest extends Vue {
  private getters = this.$store.getters as VuexStoreGetters

  private touchedCalendar = false
  private dates: TimeOffRequestDates = {'from': '', 'to': ''}
  private note = ''

  private formIsFilled(): boolean {
    if (this.dates && (this.dates.hasOwnProperty('from') && this.dates.from != '') || (!this.dates.hasOwnProperty('from') && this.dates != '')) {
      return true
    } else {
      return false
    }
  }

  private conflictingResponsibilityBuddies(): Array<TimeOffRequestRetrieve> {
    return this.getters['timeOffModule/conflictingTimeOffRequests']
  }

  private dateChanged(): void {
    // Check if there are any coworkers out with shared responsibilities
    this.touchedCalendar = true
    if (this.dates) {
      this.$store.dispatch('timeOffModule/getConflictingResponsibilities', { dates: this.dates })
        .catch(e => {
          console.error('Error creating review note:', e)
        })
    }
  }

  private createTimeOffRequest(): void {
    if (this.dates.hasOwnProperty('from') && this.dates.from == '') {
      return
    }    
    this.$store.dispatch('timeOffModule/createTimeOffRequest', { dates: this.dates, note: this.note })
      .then(() => {
        Notify.create('Created a new time off request.')
        this.$router.push({ name: 'timeoff-my-requests'})
          .then(() => {
            location.reload() // TODO: This seems to be necessary in order to immediately edit a time off request after creating it.
          })
          .catch(e => {
            console.error('Error navigating to My Requests page after creating time off request:', e)
          })
      })
      .catch(e => {
        console.error('Error creating review note:', e)
      })
  }
}
</script>

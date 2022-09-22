<template>
  <div>
    <div class="q-gutter-md row">
      <q-date v-model="dates" range @input="dateChanged()"/>
      <div v-if="conflictingResponsibilityBuddies().length != 0">
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
        label="Public Note (visible to team members)"
        class="q-pb-md"
    />
    <q-input
      v-model="privateNote"
      label="Private Note (visible to manager only)"
      class="q-pb-md"
    />
    <q-btn color="white" text-color="black" label="Update" :disabled="!formIsFilled()" @click="updateTimeOffRequest()" />
  </div>
</template>

<style lang="scss">

</style>

<script lang="ts">
import TimeOffDataService from 'src/services/TimeOffDataService'
import { Component, Vue } from 'vue-property-decorator'
import { TimeOffRequestDates, TimeOffRequestRetrieve, AxiosTimeOffRequestRetrieveOneServerResponse, VuexStoreGetters } from '../../store/types'

@Component
export default class TimeOffRequest extends Vue {
  private getters = this.$store.getters as VuexStoreGetters

  private pk = ''
  private dates: TimeOffRequestDates = {'from': '', 'to': ''}
  private note = ''
  private privateNote = ''

  private formIsFilled(): boolean {
    if (!!this.dates) {
      return true
    } else {
      return false
    }
  }

  // TODO: Do a valuesAreChanged thing like with ReviewNoteDetail so we aren't always resetting acknowledgements unnecessarily

  private conflictingResponsibilityBuddies(): Array<TimeOffRequestRetrieve> {
    return this.getters['timeOffModule/conflictingTimeOffRequests']
  }

  private dateChanged(): void {
    // Check if there are any coworkers out with shared responsibilities
    if (this.dates) {
      this.$store.dispatch('timeOffModule/getConflictingResponsibilities', { dates: this.dates })
        .catch(e => {
          console.error('Error getting conflicting responsibilities:', e)
        })
    }
  }

  private retrieveRequest(): void {
    TimeOffDataService.get(this.$route.params.pk)
      .then((response: AxiosTimeOffRequestRetrieveOneServerResponse) => {
        const startDate: string = response.data.start_date.toString().split('-').join('/')
        const endDate: string = response.data.end_date.toString().split('-').join('/')
        this.pk = response.data.pk.toString()
        if (startDate == endDate) {
          this.dates = startDate
        } else {
          this.dates = {'from': startDate, 'to': endDate}
        }
        this.note = response.data.note
        this.privateNote = response.data.private_note
      })
      .catch(e => {
        console.error('Error getting time off request:', e);
      });
  }

  private updateTimeOffRequest(): void {
    TimeOffDataService.update(this.pk, {
      dates: this.dates,
      note: this.note,
      privateNote: this.privateNote
    })
      .then(() => {
        this.$router.push({ name: 'timeoff-my-requests'})
          .catch(e => {
            console.error('Error navigating to My Requests page after creating time off request:', e)
          })
      })
      .catch(e => {
        console.error('Error updating time off request:', e)
      })
  }

  mounted() {
    this.retrieveRequest();
  }
}
</script>

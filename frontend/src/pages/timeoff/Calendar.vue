<template>
  <div>
    <div class="q-gutter-md q-mt-md">
      <q-btn @click="setThisWeek()">Today</q-btn>
      <q-btn-group>
        <q-btn color="secondary" icon="west" @click="weekBackward()"/>
        <q-btn color="secondary" icon="east" @click="weekForward()"/>
      </q-btn-group>
    </div>
    <div class="q-mt-lg">
      <div v-for="day of teamTimeOff()" :key="day.date">
        <div class="text-h5"><span>{{day.date}}</span><span v-if="day.isToday"> (Today)</span></div>
        <ul>
          <div v-for="request of day.requests" :key="request.pk">
            <q-icon v-if="request.acknowledged==null" color="orange" name="help" size="sm" />
            <q-icon v-if="request.acknowledged==false" color="red" name="cancel" size="sm" />
            <q-icon v-if="request.acknowledged && request.acknowledged==true" color="green" name="check_circle" size="sm" />
            <router-link :to="{ name: 'employee-responsibilities', params: { pk: request.employee_pk } }">{{ request.employee_name }}</router-link>
            <q-icon v-if="true" color="red" name="warning" size="sm" class="q-ml-sm">
              <q-tooltip content-style="font-size: 16px">
                <div>One or more team members with shared responsibilities will be also be unavailable:</div>
                <ul>
                  <li>Dan Hogue: Fiddle with the fiddles</li>
                  <li>Andy Smith: Futz with the futzes</li>
                </ul>
              </q-tooltip>
            </q-icon>
          </div>
        </ul>
      </div>
    </div>
  </div>
</template>

<style lang="scss">

</style>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { TimeOffRequestRetrieve, VuexStoreGetters } from '../../store/types'

type TimeOffCalendarData = Array<{date: string, isToday: boolean, requests: Array<TimeOffRequestRetrieve>}>

@Component
export default class TimeOffCalendar extends Vue {
  private getters = this.$store.getters as VuexStoreGetters

  private today = new Date()
  private thisWeekMonday = new Date()
  private selectedMonday = new Date()

  private teamTimeOff(): TimeOffCalendarData {
    const apiResults = this.getters['timeOffModule/teamTimeOffRequests'].results
    let sortedTimeOff: TimeOffCalendarData = []
    if (apiResults) {
      for (let i=0; i<5; i++) {
        let d = new Date(this.selectedMonday.getTime() + i*(1000 * 60 * 60 * 24))
        let isToday = d.setHours(0,0,0,0) === this.today.setHours(0,0,0,0)
        sortedTimeOff.push({
          date: d.toLocaleDateString('en-us', { weekday: 'long', month: 'long', day: 'numeric' }),
          isToday: isToday,
          requests: apiResults.filter(request => {
            const targetDateMS = d.setHours(0,0,0,0)
            
            const fromDate = new Date(request.start_date)
            const fromTZOffset = fromDate.getTimezoneOffset() * 60000
            const fromDateMS = new Date(fromDate.getTime() + fromTZOffset).setHours(0,0,0,0)
            
            const toDate = new Date(request.end_date)
            const toTZOffset = toDate.getTimezoneOffset() * 60000
            const toDateMS = new Date(toDate.getTime() + toTZOffset).setHours(0,0,0,0)

            if (fromDateMS <= targetDateMS && targetDateMS <= toDateMS) {
              return true
            } else {
              return false
            }
          })
        })
      }
    }
    return sortedTimeOff
  }

  // TODO: This currently gets all time off; should probably just get for a period
  private retrieveTeamTimeOff(): void {
    this.$store.dispatch('timeOffModule/getTeamTimeOffRequests')
      .catch(e => {
        console.error('Error retrieving team time off', e)
      })
  }

  private setDates() {
    let prevMonday = new Date()
    prevMonday.setDate(prevMonday.getDate() - (prevMonday.getDay() + 6) % 7)
    this.thisWeekMonday = prevMonday
    this.selectedMonday = prevMonday
  }

  private setThisWeek() {
    this.selectedMonday = this.thisWeekMonday
  }

  private weekBackward() {
    this.selectedMonday = new Date(this.selectedMonday.getTime() - 7 * (1000 * 60 * 60 * 24))
  }

  private weekForward() {
    this.selectedMonday = new Date(this.selectedMonday.getTime() + 7 * (1000 * 60 * 60 * 24))
  }

  mounted() {
    this.setDates()
    this.retrieveTeamTimeOff()
  }
}
</script>

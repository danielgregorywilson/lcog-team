<template>
  <div>
    <div class="q-gutter-md q-mt-md">
      <q-btn>Today</q-btn>
      <q-btn-group>
        <q-btn color="secondary" icon="west" />
        <q-btn color="secondary" icon="east" />
      </q-btn-group>
    </div>
    <div class="q-mt-lg">
      <div class="text-h5">Wednesday, June 29 (Today)</div>
      <ul>
        <div><router-link :to="{ name: 'employee-responsibilities', params: { pk: 275 } }">Daniel Wilson</router-link></div>
        <div>Keith Testerman</div>
      </ul>
      <div class="text-h5">Thursday, June 30</div>
      <ul>
        <div>Dan Wilson (pending)</div>
        <div>Dan Hogue</div>
      </ul>
      <div class="text-h5">Friday, July 1</div>
      <ul>
        <div>Heidi Leyba</div>
      </ul>
    </div>
  </div>
</template>

<style lang="scss">

</style>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { VuexStoreGetters } from '../../store/types'

@Component
export default class TimeOffCalendar extends Vue {
  private getters = this.$store.getters as VuexStoreGetters

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

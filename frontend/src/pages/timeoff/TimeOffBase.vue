<template>
  <q-page class="q-pa-md">
    <div class="text-h4">Time Off</div>
    <div class="q-my-md row justify-between">
      <div class="q-gutter-sm">
        <q-btn :to="{ name: 'timeoff-calendar' }" unelevated rounded color="primary" icon="list" label="Who Is Out?" />
        <q-btn :to="{ name: 'timeoff-my-requests' }" unelevated rounded color="primary" icon="calendar_today" label="My Requests" />
        <q-btn v-if="isManager()" :to="{ name: 'timeoff-manage-requests' }" unelevated rounded color="primary" icon="book" label="Manage Requests">
          <q-badge v-if="numUnacknowledgedManagedTimeOffRequests()" rounded color="red" floating>{{ numUnacknowledgedManagedTimeOffRequests() }}</q-badge>
        </q-btn>
      </div>
    </div>
    <router-view :key="$route.path" />
  </q-page>
</template>

<style scoped lang="scss">
</style>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { TimeOffRequestRetrieve, VuexStoreGetters } from '../../store/types'

@Component
export default class TimeOffBase extends Vue {
  private getters = this.$store.getters as VuexStoreGetters

  private isManager() {
    return this.getters['userModule/getEmployeeProfile'].is_manager
  }

  private managedTimeOffRequests(): Array<TimeOffRequestRetrieve> {
    return this.getters['timeOffModule/managedTimeOffRequests'].results
  }

  private numUnacknowledgedManagedTimeOffRequests(): number {
    const tors = this.getters['timeOffModule/managedTimeOffRequests'].results
    if (tors) {
      return tors.filter(tor => tor.acknowledged == null).length
    } else {
      return 0
    }
  }

  private retrieveManagedTimeOffRequests(): void {
    this.$store.dispatch('timeOffModule/getManagedTimeOffRequests')
      .catch(e => {
        console.error('Error retrieving my upcoming time off requests', e)
      })
  }

  mounted() {
    this.retrieveManagedTimeOffRequests()
  }
}
</script>

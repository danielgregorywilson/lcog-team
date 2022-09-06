<template>
  <q-page class="q-pa-md">
    <div class="text-h4">EIS</div>
    <div class="q-mt-sm">
      <q-stepper
        v-model="step"
        vertical
        color="primary"
        animated
      >
        <q-step
          :name="1"
          title="Select campaign settings"
          icon="settings"
          :done="step > 1"
        >
          For each ad campaign that you create, you can control how much you're willing to
          spend on clicks and conversions, which networks and geographical locations you want
          your ads to show on, and more.

          <q-stepper-navigation>
            <q-btn @click="step = 2" color="primary" label="Continue" />
          </q-stepper-navigation>
        </q-step>

        <q-step
          :name="2"
          title="Create an ad group"
          caption="Optional"
          icon="create_new_folder"
          :done="step > 2"
        >
          An ad group contains one or more ads which target a shared set of keywords.

          <q-stepper-navigation>
            <q-btn @click="step = 4" color="primary" label="Continue" />
            <q-btn flat @click="step = 1" color="primary" label="Back" class="q-ml-sm" />
          </q-stepper-navigation>
        </q-step>

        <q-step
          :name="3"
          title="Ad template"
          icon="assignment"
          disable
        >
          This step won't show up because it is disabled.
        </q-step>

        <q-step
          :name="4"
          title="Create an ad"
          icon="add_comment"
        >
          Try out different ad text to see what brings in the most customers, and learn how to
          enhance your ads using features like ad extensions. If you run into any problems with
          your ads, find out how to tell if they're running and how to resolve approval issues.

          <q-stepper-navigation>
            <q-btn color="primary" label="Finish" />
            <q-btn flat @click="step = 2" color="primary" label="Back" class="q-ml-sm" />
          </q-stepper-navigation>
        </q-step>
      </q-stepper>
    </div>
  </q-page>
</template>

<style scoped lang="scss">
</style>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { VuexStoreGetters } from '../../store/types'

@Component
export default class EIS extends Vue {
  private getters = this.$store.getters as VuexStoreGetters

  private step = 1;

  // private isManager() {
  //   return this.getters['userModule/getEmployeeProfile'].is_manager
  // }

  // private managedTimeOffRequests(): Array<TimeOffRequestRetrieve> {
  //   return this.getters['timeOffModule/managedTimeOffRequests'].results
  // }

  // private numUnacknowledgedManagedTimeOffRequests(): number {
  //   const tors = this.getters['timeOffModule/managedTimeOffRequests'].results
  //   if (tors) {
  //     return tors.filter(tor => tor.acknowledged == null).length
  //   } else {
  //     return 0
  //   }
  // }

  // private retrieveManagedTimeOffRequests(): void {
  //   this.$store.dispatch('timeOffModule/getManagedTimeOffRequests')
  //     .catch(e => {
  //       console.error('Error retrieving my upcoming time off requests', e)
  //     })
  // }

  mounted() {
    // this.retrieveManagedTimeOffRequests()
  }
}
</script>

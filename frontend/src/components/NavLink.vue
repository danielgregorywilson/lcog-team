<template>
  <q-item
    clickable
    :to="link"
    v-if="isVisible()"
  >
    <q-item-section
      v-if="icon"
      avatar
    >
      <q-icon :name="icon" />
    </q-item-section>

    <q-item-section>
      <q-item-label>{{ title }}</q-item-label>
    </q-item-section>
  </q-item>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import { VuexStoreGetters } from '../store/types'

@Component
export default class NavLink extends Vue{
  @Prop({required: true}) readonly title!: string
  @Prop({default: '#'}) readonly link!: string
  @Prop({default: ''}) readonly icon!: string
  @Prop({default: false}) readonly managerOnly!: boolean
  @Prop({default: false}) readonly eligibleForTeleworkApplicationOnly!: boolean
  @Prop({default: false}) readonly hasWorkflowRoles!: boolean

  private getters = this.$store.getters as VuexStoreGetters

  private isVisible(): boolean {
    const shouldNotViewBecauseNotManager = this.managerOnly && this.getters['userModule/isManager']
    const shouldNotViewBecauseNotEligibleForTeleworkApplication = this.eligibleForTeleworkApplicationOnly && !this.getters['userModule/getEmployeeProfile'].is_eligible_for_telework_application
    const shouldNotViewBeacuseNoWorkflowRoles = this.hasWorkflowRoles && !this.getters['userModule/hasWorkflowRoles']
    if (shouldNotViewBecauseNotManager || shouldNotViewBecauseNotEligibleForTeleworkApplication || shouldNotViewBeacuseNoWorkflowRoles) {
      return false
    } else {
      return true
    }
  }
};
</script>

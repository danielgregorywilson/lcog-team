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

@Component
export default class NavLink extends Vue{
  @Prop({required: true}) readonly title!: string
  @Prop({default: '#'}) readonly link!: string
  @Prop({default: ''}) readonly icon!: string
  @Prop({default: false}) readonly managerOnly!: boolean
  @Prop({default: false}) readonly eligibleForTeleworkApplicationOnly!: boolean
  @Prop({default: false}) readonly hasWorkflowRoles!: boolean

  private isVisible(): boolean {
    const shouldNotViewBecauseNotManager = this.managerOnly && !this.$store.getters['userModule/isManager'] // eslint-disable-line @typescript-eslint/no-unsafe-member-access
    const shouldNotViewBecauseNotEligibleForTeleworkApplication = this.eligibleForTeleworkApplicationOnly && !this.$store.getters['userModule/getEmployeeProfile'].is_eligible_for_telework_application // eslint-disable-line @typescript-eslint/no-unsafe-member-access
    const shouldNotViewBeacuseNoWorkflowRoles = this.hasWorkflowRoles && !this.$store.getters['userModule/hasWorkflowRoles']
    if (shouldNotViewBecauseNotManager || shouldNotViewBecauseNotEligibleForTeleworkApplication || shouldNotViewBeacuseNoWorkflowRoles) {
      return false
    } else {
      return true
    }
  }
};
</script>

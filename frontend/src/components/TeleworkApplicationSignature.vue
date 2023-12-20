<!-- Not converted from Quasar 1/Vue 2 -->
<template>
  <div class="row signature-block">
    <div class="col">
      <div v-if="signature[2]" class="signature"><span class="signature-text">{{ signature[2] }}</span></div>
      <div v-else class="signature">
        <q-btn v-if="userCanSign(signature[4], signature[5])" color="white" text-color="black" label="Click to Sign" @click="signPerformanceReview()" class="signature-button" />
        <div v-else>&nbsp;</div>
      </div>
      <div class="signature-type"><span class="text-bold">{{ signature[1] }} Signature</span></div>
    </div>
    <div class="col signature-date-block">
      <div v-if="signature[3]" class="signature-date"><span class="signature-date-text">{{ signature[3] | readableDate }}</span></div>
      <div v-else class="signature-date">&nbsp;</div>
      <span>Date</span>
    </div>
  </div>
</template>

<style scoped lang="scss">
  .signature-block {
    margin-bottom: 20px;
  }
  .signature {
    max-width: 465px;
    height: 36px;
    border-bottom: 1px black solid;
    display: flex;
  }
  .signature-text {
    font-family: cursive, serif;
    align-self: flex-end;
  }
  .signature-type {
    max-width: 465px;
  }
  .signature-date {
    width: 100px;
    height: 36px;
    border-bottom: 1px black solid;
    display: flex;
  }
  .signature-date-text {
    align-self: flex-end;
  }

  @media print {
    .signature-block {
      margin: 0;
    }
  }
</style>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import '../filters'

@Component
export default class TeleworkApplicationSignature extends Vue {
  // Format: [Signature index, Role, Name, Date, Employee PK, Employee Ready to Sign]
  @Prop({required: true}) readonly signature!: [number, string, string, string, number, boolean]
  @Prop({required: true}) readonly currentUserPk!: number
  // @Prop({default: '#'}) readonly link!: string
  // @Prop({default: ''}) readonly icon!: string
  // @Prop({default: false}) readonly managerOnly!: boolean

  private userCanSign(employeePk: number, employeeIsReadyToSign: boolean): boolean {
    const employeeIsCurrentUser = employeePk == this.currentUserPk
    return employeeIsCurrentUser && employeeIsReadyToSign
  }

  private signPerformanceReview(): void {
    this.$emit('clicked-sign-button', this.signature[0], this.signature[4])
  }

  // private isVisible(): boolean {
  //   if (this.managerOnly && !this.$store.getters['userModule/getEmployeeProfile'].is_manager) { // eslint-disable-line @typescript-eslint/no-unsafe-member-access
  //     return false
  //   } else {
  //     return true
  //   }
  // }
};
</script>

<template>
  <q-page class="q-mt-md">
    <div class="text-h3 q-mb-md">Generate Desk Reservation Reports</div>
    <div class="text-h4 q-mb-md"></div>
    <q-btn-toggle
        v-model="showReport"
        class="q-pb-md"
        spread
        no-caps
        rounded
        unelevated
        toggle-color="primary"
        color="white"
        text-color="primary"
        :options="[
          {label: 'Generate Desk Usage Report', value: 'desk'},
          {label: 'Generate Employee Usage Report', value: 'employee'}
        ]"
      />
    <div v-if="showReport=='desk'">
      <q-form
        @submit="deskFormSubmit"
      >
        <div class="row justify-center">Start Date/Time (defaults to midnight on the first day of last month)</div>
        <div class="row justify-center q-gutter-md q-mb-md">
          <q-date
            v-model="startDateTime"
            mask="YYYY-MM-DD HH:mm"
          />
          <q-time
            v-model="startDateTime"
            mask="YYYY-MM-DD HH:mm"
          />
        </div>
        <div class="row justify-center">End Date/Time (defaults to 11:59PM on the last day of last month)</div>
        <div class="row justify-center q-gutter-md q-mb-md">
          <q-date
            v-model="endDateTime"
            mask="YYYY-MM-DD HH:mm"
          />
          <q-time
            v-model="endDateTime"
            mask="YYYY-MM-DD HH:mm"
          />
        </div>
        <div class="row justify-center q-mb-md">
          <q-btn label="Submit" type="submit" color="primary" :loading="formSubmitted"/>
        </div>
      </q-form>
    </div>
    <div v-if="showReport=='employee'">
      <q-form
        @submit="employeeFormSubmit"
      >
        <div class="row justify-center">Start Date/Time (defaults to midnight on the first day of last month)</div>
        <div class="row justify-center q-gutter-md q-mb-md">
          <q-date
            v-model="startDateTime"
            mask="YYYY-MM-DD HH:mm"
          />
          <q-time
            v-model="startDateTime"
            mask="YYYY-MM-DD HH:mm"
          />
        </div>
        <div class="row justify-center">End Date/Time (defaults to 11:59PM on the last day of last month)</div>
        <div class="row justify-center q-gutter-md q-mb-md">
          <q-date
            v-model="endDateTime"
            mask="YYYY-MM-DD HH:mm"
          />
          <q-time
            v-model="endDateTime"
            mask="YYYY-MM-DD HH:mm"
          />
        </div>
        <div class="row justify-center q-mb-md">
          <q-btn label="Submit" type="submit" color="primary" :loading="formSubmitted"/>
        </div>
      </q-form>
    </div>
  </q-page>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

@Component
export default class Report extends Vue{
  private showReport = 'desk'
  private startDateTime = ''
  private endDateTime = ''
  private formSubmitted = false

  private deskFormSubmit (): void {
    this.formReset()
    this.formSubmitted = true
    // TODO: Make request for desk report
    setTimeout(() => {
      this.formSubmitted = false
    }, 1000)
  }

  private employeeFormSubmit (): void {
    this.formReset()
    this.formSubmitted = true
    // TODO: Make request for employee report
    setTimeout(() => {
      this.formSubmitted = false
    }, 1000)
  }

  private formReset (): void {
    this.startDateTime = ''
    this.endDateTime = ''
  }
}
</script>

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
        <div class="row justify-center">End Date/Time (defaults to midnight on the first day of this month)</div>
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
import DeskReservationDataService from 'src/services/DeskReservationDataService'
import { Component, Vue } from 'vue-property-decorator'
import { AxiosGetReservationReportDataServerResponse, GetReservationDataInterface } from '../../store/types'

@Component
export default class Report extends Vue{
  private showReport = 'desk'
  private startDateTime = ''
  private endDateTime = ''
  private formSubmitted = false

  private deskFormSubmit (): void {
    this.formSubmitted = true
    DeskReservationDataService.getDeskUsageReport({
      startDateTime: this.startDateTime,
      endDateTime: this.endDateTime
    })
      .then((response: AxiosGetReservationReportDataServerResponse) => {
        this.download_desk_usage_report(response.data)
        this.formReset()
        this.formSubmitted = false
      })
      .catch(e => {
        console.error('Error generating desk usage report:', e)
      })
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

  private download_desk_usage_report(data: GetReservationDataInterface) {
    // Define the heading for each row of the data
    var csv = 'Desk,Total Hours,Days Utilized\n'

    // Merge the data with CSV
    Object.keys(data).forEach((key) => {
      var row = [key, data[key]['total_hours'], data[key]['days_utilized']].join(',')
      csv += row
      csv += '\n'
    });

    var hiddenElement = document.createElement('a')
    hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv)
    hiddenElement.target = '_blank'

    // Provide the name for the CSV file to be downloaded
    let startString = this.startDateTime ? this.startDateTime.replace(' ','_') : 'beginning_of_last_month'
    let endString = this.endDateTime ? this.endDateTime.replace(' ','_') : 'end_of_last_month'
    hiddenElement.download = `desk_usage_report_${startString}_${endString}.csv`
    hiddenElement.click()
  }
}
</script>

<template>
  <q-page class="q-mt-md" style="max-width: 754px;">
    <div class="text-h3 text-center q-mb-md">
      Generate Desk Reservation Reports
    </div>
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
          {label: 'All Desk Summary', value: 'desk-summary'},
          {label: 'Desk Detail', value: 'desk-detail'},
          {label: 'All Employee Summary', value: 'employee-summary'},
          {label: 'Employee Detail', value: 'employee-detail'}
        ]"
      />
      <div class="text-h6">
        <div v-if="showReport=='desk-summary'">
          Each desk with total hours, days utilized, and most frequent employee
          over a time period.
        </div>
        <div v-else-if="showReport=='desk-detail'">
          Selected desks with all employee usage over a time period.
        </div>
        <div v-else-if="showReport=='employee-summary'">
          Each employee with total hours, days utilized, and most frequent desk
          over a time period.
        </div>
        <div v-else-if="showReport=='employee-detail'">
          Selected employees with all desk usage over a time period.
        </div>
      </div>

      <q-option-group
        v-if="showReport=='desk-detail'"
        :options="deskOptions"
        v-model="selectedDesks"
        type="checkbox"
        :inline="true"
      />

      <div class="row justify-center">
        Start Date/Time (defaults to midnight on the first day of last month)
      </div>
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
      <div class="row justify-center">
        End Date/Time (defaults to midnight on the first day of this month)
      </div>
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
        <q-btn
          label="Submit"
          color="primary"
          @click="submitForm()"
          :loading="formSubmitted"
        />
      </div>
  </q-page>
</template>

<script setup lang="ts">
import { onMounted, Ref, ref } from 'vue'
import {
  GetDeskSummaryReportDataInterface, GetDetailReportDataInterface,
  GetEmployeeSummaryReportDataInterface
} from 'src/types'
import { useDeskReservationStore } from 'src/stores/deskreservation'

const deskReservationStore = useDeskReservationStore()

let showReport = ref('desk-summary')
let startDateTime = ref('')
let endDateTime = ref('')
let formSubmitted = ref(false)

let deskOptions = ref([]) as Ref<{label: string, value: number}[]>
let employeeOptions = ref([]) as Ref<{label: string, value: number}[]>
let selectedDesks = ref([])
let selectedEmployees = ref([])

function submitForm() {
  if (showReport.value === 'desk-summary') {
    deskSummaryFormSubmit()
  } else if (showReport.value === 'desk-detail') {
    deskDetailFormSubmit()
  } else if (showReport.value === 'employee-summary') {
    employeeSummaryFormSubmit()
  } else if (showReport.value === 'employee-detail') {
    employeeDetailFormSubmit()
  }
}

function deskSummaryFormSubmit () {
  formSubmitted.value = true
  deskReservationStore.getDeskSummaryReport({
    startDateTime: startDateTime.value,
    endDateTime: endDateTime.value
  })
    .then((reportData) => {
      download_desk_summary_report(reportData)
      formReset()
      formSubmitted.value = false
    })
    .catch(e => {
      console.error('Error generating desk summary report:', e)
    })
}

function deskDetailFormSubmit () {
  formSubmitted.value = true
  deskReservationStore.getDeskDetailReport({
    desks: selectedDesks.value,
    startDateTime: startDateTime.value,
    endDateTime: endDateTime.value
  })
    .then((reportData) => {
      download_desk_detail_report(reportData)
      // formReset()
      formSubmitted.value = false
    })
    .catch(e => {
      console.error('Error generating desk detail report:', e)
    })
}

function employeeSummaryFormSubmit() {
  formSubmitted.value = true
  deskReservationStore.getEmployeeSummaryReport({
    startDateTime: startDateTime.value,
    endDateTime: endDateTime.value
  })
    .then((reportData) => {
      download_employee_summary_report(reportData)
      formReset()
      formSubmitted.value = false
    })
    .catch(e => {
      console.error('Error generating employee summary report:', e)
    })
}

function employeeDetailFormSubmit() {
  formSubmitted.value = true
  deskReservationStore.getEmployeeDetailReport({
    emplotees: selectedEmployees.value,
    startDateTime: startDateTime.value,
    endDateTime: endDateTime.value
  })
    .then((reportData) => {
      download_employee_detail_report(reportData)
      formReset()
      formSubmitted.value = false
    })
    .catch(e => {
      console.error('Error generating employee detail report:', e)
    })
}

function formReset() {
  startDateTime.value = ''
  endDateTime.value = ''
}

function download_desk_summary_report(data: GetDeskSummaryReportDataInterface) {
  // Define the heading for each row of the data
  var csv = 'Desk,Total Hours,Days Utilized,Most Frequent Employee\n'

  // Merge the data with CSV
  Object.keys(data).forEach((key) => {
    var row = [key, data[key]['total_hours'], data[key]['days_utilized'], data[key]['most_frequent_employee']].join(',')
    csv += row
    csv += '\n'
  })

  var hiddenElement = document.createElement('a')
  hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv)
  hiddenElement.target = '_blank'

  // Provide the name for the CSV file to be downloaded
  let startString = startDateTime.value ? startDateTime.value.replace(' ','_') : 'beginning_of_last_month'
  let endString = endDateTime.value ? endDateTime.value.replace(' ','_') : 'end_of_last_month'
  hiddenElement.download = `desk_summary_${startString}_${endString}.csv`
  hiddenElement.click()
}

function download_desk_detail_report(data: GetDetailReportDataInterface) {
  // Define the heading for each row of the data
  var csv = 'Desk,Employee,Day,Total Hours\n'

  // Merge the data with CSV
  Object.keys(data).forEach((key) => {
    var row = [
      data[key]['desk'],
      data[key]['employee'],
      data[key]['day'],
      data[key]['total_hours']
    ].join(',')
    csv += row
    csv += '\n'
  })

  var hiddenElement = document.createElement('a')
  hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv)
  hiddenElement.target = '_blank'

  // Provide the name for the CSV file to be downloaded
  let startString = startDateTime.value ? startDateTime.value.replace(' ','_') :
    'beginning_of_last_month'
  let endString = endDateTime.value ? endDateTime.value.replace(' ','_') :
    'end_of_last_month'
  hiddenElement.download = `desk_detail_${startString}_${endString}.csv`
  hiddenElement.click()
}

function download_employee_summary_report(data: GetEmployeeSummaryReportDataInterface) {
  // Define the heading for each row of the data
  var csv = 'Employee,Total Hours,Days Utilized,Most Frequent Desk\n'

  // Merge the data with CSV
  Object.keys(data).forEach((key) => {
    var row = [key, data[key]['total_hours'], data[key]['days_utilized'], data[key]['most_frequent_desk']].join(',')
    csv += row
    csv += '\n'
  })

  var hiddenElement = document.createElement('a')
  hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv)
  hiddenElement.target = '_blank'

  // Provide the name for the CSV file to be downloaded
  let startString = startDateTime.value ? startDateTime.value.replace(' ','_') : 'beginning_of_last_month'
  let endString = endDateTime.value ? endDateTime.value.replace(' ','_') : 'end_of_last_month'
  hiddenElement.download = `employee_summary_${startString}_${endString}.csv`
  hiddenElement.click()
}

onMounted(() => {
  deskReservationStore.getAllDesks()
    .then(() => {
      for (let desk of deskReservationStore.allDesks) {
        deskOptions.value.push({label: desk.number, value: desk.pk})
      }
    })
})

</script>

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
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import {
  GetDeskReservationDataInterface, GetEmployeeDeskReservationDataInterface
} from 'src/types'
import { useDeskReservationStore } from 'src/stores/deskreservation'

const deskReservationStore = useDeskReservationStore()

let showReport = ref('desk')
let startDateTime = ref('')
let endDateTime = ref('')
let formSubmitted = ref(false)

function deskFormSubmit () {
  formSubmitted.value = true
  deskReservationStore.getDeskUsageReport({
    startDateTime: startDateTime.value,
    endDateTime: endDateTime.value
  })
    .then((reportData) => {
      download_desk_usage_report(reportData)
      formReset()
      formSubmitted.value = false
    })
    .catch(e => {
      console.error('Error generating desk usage report:', e)
    })
}

function employeeFormSubmit() {
  formSubmitted.value = true
  deskReservationStore.getEmployeeDeskUsageReport({
    startDateTime: startDateTime.value,
    endDateTime: endDateTime.value
  })
    .then((reportData) => {
      download_employee_desk_usage_report(reportData)
      formReset()
      formSubmitted.value = false
    })
    .catch(e => {
      console.error('Error generating employee desk usage report:', e)
    })
}

function formReset() {
  startDateTime.value = ''
  endDateTime.value = ''
}

function download_desk_usage_report(data: GetDeskReservationDataInterface) {
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
  hiddenElement.download = `desk_usage_report_${startString}_${endString}.csv`
  hiddenElement.click()
}

function download_employee_desk_usage_report(data: GetEmployeeDeskReservationDataInterface) {
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
  hiddenElement.download = `employee_desk_usage_report_${startString}_${endString}.csv`
  hiddenElement.click()
}

</script>

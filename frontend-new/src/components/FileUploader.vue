<template>
<q-uploader
  ref="fileuploader"
  url=""
  max-file-size="20000000"
  @rejected="rejectFileTooLarge"
  style="max-width: 300px"
>
  <template v-slot:header="scope">
    <div class="row no-wrap items-center q-pa-sm q-gutter-xs">
      <q-btn v-if="scope.canAddFiles" type="a" icon="add_box" round dense flat>
        <q-uploader-add-trigger />
        <q-tooltip>Pick File</q-tooltip>
      </q-btn>
      <q-btn v-if="scope.canUpload" icon="cloud_upload" @click="uploadFile()" round dense flat >
        <q-tooltip>Upload File</q-tooltip>
      </q-btn>

      <q-btn v-if="scope.isUploading" icon="clear" @click="scope.abort" round dense flat >
        <q-tooltip>Abort Upload</q-tooltip>
      </q-btn>
    </div>
  </template>
  <template v-slot:list="scope">
    <q-list separator>
      <q-item v-for="file in scope.files" :key="file.name">
        <q-item-section>
          <q-item-label class="full-width ellipsis">
            {{ file.name }}
          </q-item-label>
          <q-item-label caption>
            {{ file.__sizeLabel }}
          </q-item-label>
        </q-item-section>
        <q-item-section top side>
          <q-btn
            class="gt-xs"
            size="12px"
            flat
            dense
            round
            icon="delete"
            @click="scope.removeFile(file)"
          />
        </q-item-section>
      </q-item>
    </q-list>
  </template>
</q-uploader>
<div v-if="fileSuccessfullyUploaded" class="text-green">Successfully uploaded</div>
<div v-if="fileTooLarge" class="text-red">File is too large</div>
</template>

<script setup lang="ts">
import { onMounted, onUpdated, ref } from 'vue'

let selectedFile = ref(new File([''], ''))
let fileTooLarge = ref(false)
let fileSuccessfullyUploaded = ref(false)


// const emptyEmployee = {pk: -1, name: '', legal_name: ''}

// const props = defineProps<{
//   label: string,
//   employee: SimpleEmployeeRetrieve,
//   useLegalName: boolean
//   readOnly: boolean
// }>()

// const emit = defineEmits<{
//   (e: 'clear'): void
//   (e: 'input', arg: SimpleEmployeeRetrieve): void
// }>()

function file_selected(file: Array<File>) {
  selectedFile.value = file[0];
}

function rejectFileTooLarge() {
  fileTooLarge.value = true
  setTimeout(() => fileTooLarge.value = false, 5000)
}

function uploadFile() {
  let fd = new FormData();
  fd.append('pk', this.prPk)
  fd.append('file', this.selectedFile)

  // PerformanceReviewDataService.uploadSignedPositionDescription(fd)
  //   .then((response: FileUploadDescriptionUploadServerResponse) => {
  //     if (response.status == 200) {
  //       this.$refs.fileuploader.reset()
  //       this.uploadedPositionDescriptionUrl = response.data
  //       this.fileSuccessfullyUploaded = true
  //       setTimeout(() => this.fileSuccessfullyUploaded = false, 5000)
  //       this.updatePerformanceReview()
  //         .catch(e => {
  //           console.error('Error updating PR after uploading signed position description:', e)
  //         })
  //     }
  //   })
  //   .catch(e => {
  //     console.error('Error uploading signed position description:', e)
  //   })
}

onMounted(() => {
  // selectedEmployee.value = props.employee
})

onUpdated(() => {
  // selectedEmployee.value = props.employee
})
</script>

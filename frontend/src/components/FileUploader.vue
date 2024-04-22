<template>
<q-uploader
  ref="fileuploader"
  max-file-size="20000000"
  @added="file_selected"
  @rejected="rejectFileTooLarge"
  style="max-width: 300px"
>
  <template v-slot:header="scope">
    <div class="row no-wrap items-center q-pa-sm q-gutter-xs">
      <q-btn v-if="scope.canAddFiles" type="a" icon="add_box" round dense flat>
        <q-uploader-add-trigger />
        <q-tooltip>Pick File</q-tooltip>
      </q-btn>
      <q-btn
        v-if="scope.isUploading"
        icon="clear"
        @click="scope.abort"
        round
        dense
        flat
      >
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
<div v-if="fileSuccessfullyUploaded" class="text-green">
  Successfully uploaded
</div>
<div v-if="fileTooLarge" class="text-red">File is too large</div>
</template>

<script setup lang="ts">
import axios from 'axios'
import { onMounted, onUpdated, ref } from 'vue'
import { apiURL, handlePromiseError } from 'src/stores/index'

let selectedFile = ref(new File([''], ''))
let fileTooLarge = ref(false)
let fileSuccessfullyUploaded = ref(false)

const props = defineProps<{
  file: File,
  contentTypeAppLabel: string,
  contentTypeModel: string,
  objectPk?: string,
  readOnly: boolean
}>()

const emit = defineEmits<{
  (e: 'uploaded', arg: URL): void
}>()

function file_selected(files: Array<File>) {
  selectedFile.value = files[0];
  uploadFile()
}

function rejectFileTooLarge() {
  fileTooLarge.value = true
  setTimeout(() => fileTooLarge.value = false, 5000)
}

function uploadFile() {
  let fd = new FormData();
  fd.append('content_type_app_label', props.contentTypeAppLabel)
  fd.append('content_type_model', props.contentTypeModel)
  fd.append('object_pk', props.objectPk || '')
  fd.append('file', selectedFile.value)
  doUpload(fd).then((url) => {
    fileSuccessfullyUploaded.value = true
    setTimeout(() => fileSuccessfullyUploaded.value = false, 5000)
    emit('uploaded', url)
  })
}

function doUpload(data: FormData): Promise<any> {
  return new Promise((resolve, reject) => {
    axios({ url: `${ apiURL }api/v1/fileupload`, method: 'POST', data })
      .then((resp) => {
        resolve(resp.data)
      })
      .catch(e => {
        handlePromiseError(reject, 'Error uploading file', e)
      })
  })
}

onMounted(() => {
  // selectedEmployee.value = props.employee
})

onUpdated(() => {
  // selectedEmployee.value = props.employee
})
</script>

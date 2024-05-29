<template>
<div>
  <q-btn
    :label="props.iconButton ? '' : props.documentUrl.split('/').pop()"
    :icon="props.iconButton ? 'file_open' : ''"
    @click="showDialog = true"
    flat
  />

  <q-dialog id="document-viewer-dialog" v-model="showDialog">
    <q-card class="file-viewer">
      <embed
        v-if="isPDF()"
        :src="props.documentUrl"
        type="application/pdf"
      >
      <div v-else>
        <q-img :src="props.documentUrl" />
        <div v-if="!isImage()" class="text-negative">
          Document filetype {{ fileExtension() }} may not be supported
        </div>
      </div>

      <q-separator />

      <q-card-actions align="center">
        <q-btn
          class="dialog-button"
          flat
          color="primary"
          round
          icon="open_in_new"
          size="lg"
          @click="openDocument()"
        />
        <q-btn
          class="dialog-button"
          v-close-popup
          flat
          color="primary"
          round
          icon="file_download"
          size="lg"
          @click="downloadDocument()"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</div>
</template>
  
<style scoped lang="scss">

.file-viewer {
  height: 100%;
  width: 100%;
  padding: 10px;

  embed {
    width: 100%;
    height: 100%;
  }
}
.dialog-button {
  margin: 0 10px;
}
</style>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

const props = defineProps<{
  iconButton?: boolean
  documentUrl: string
}>()

let showDialog = ref(false)

function isImage() {
  return props.documentUrl.match(/\.(jpeg|jpg|gif|png)$/)
}

function isPDF() {
  return props.documentUrl.match(/\.(pdf)$/)
}

function fileExtension() {
  return props.documentUrl.split('.').pop()
}

function openDocument() {
  window.open(props.documentUrl, '_blank')
}

function downloadDocument() {
  axios({
      url: props.documentUrl,
      method: 'GET',
      responseType: 'blob'
  })
      .then((response) => {
          const url = window.URL
              .createObjectURL(new Blob([response.data]));
          const link = document.createElement('a');
          link.href = url;
          const fileName = props.documentUrl.split('/').pop()
          link.setAttribute('download', fileName ? fileName : 'document');
          document.body.appendChild(link);
          link.click();
      })
}

</script>

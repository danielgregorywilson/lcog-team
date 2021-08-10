<template>
  <q-page>
    <!-- <q-header reveal elevated class="header">
      <q-toolbar>
        <q-btn flat round dense icon="menu" @click="drawerLeft = !drawerLeft" />

        <q-toolbar-title>
          <strong>Quasar</strong> Framework
        </q-toolbar-title>

        <q-btn flat round dense icon="menu" @click="drawerRight = !drawerRight" />
      </q-toolbar>
    </q-header> -->
    <div class="q-pa-md q-gutter-sm">
      <div>Please complete the following tasks:</div>
      <div class="q-gutter-xs q-pt-sm q-pb-md">
        <div class="row items-center">
          <q-avatar size="md" font-size="25px" :color="this.hasReadPolicy ? 'green' : 'grey-4'" :text-color="this.hasReadPolicy ? 'white' : 'grey-6'" icon="check" />
          <div class="q-pl-sm">Read the policy</div>
        </div>
        <div class="row items-center">
          <q-avatar size="md" font-size="25px" :color="this.hasPerformedSpeedTest ? 'green' : 'grey-4'" :text-color="this.hasPerformedSpeedTest ? 'white' : 'grey-6'" icon="check" />
          <div class="q-pl-sm">Perform an internet speed test</div>
        </div>
        <div class="row items-center">
          <q-avatar size="md" font-size="25px" :color="this.hasDoneErgonomicsThing ? 'green' : 'grey-4'" :text-color="this.hasDoneErgonomicsThing ? 'white' : 'grey-6'" icon="check" />
          <div class="q-pl-sm">Do something with ergonomics</div>
        </div>
        <div class="row items-center">
          <q-avatar size="md" font-size="25px" :color="this.isComplete ? 'green' : 'grey-4'" :text-color="this.isComplete ? 'white' : 'grey-6'" icon="check" />
          <div class="q-pl-sm">Complete</div>
        </div>
      </div>
      <q-card>
        <q-card-section>
          1) Read the policy
        </q-card-section>
        <q-separator inset />
        <q-card-section>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </q-card-section>
        <q-separator inset />
        <q-card-section>
          <q-checkbox v-model="hasReadPolicy" label="I have read and understood the policy" />
        </q-card-section>
      </q-card>
      <q-card>
        <q-card-section>
          2) Perform an internet speed test
        </q-card-section>
        <q-separator inset />
        <q-card-section>
          <ol>
            <li>Visit <a href="https://www.speedtest.net/" target="_blank">https://www.speedtest.net/</a></li>
            <li>Click "GO" and allow the test to run.</li>
            <li>When the test has completed, take a screenshot, for example by pressing Windows Key + PrtScn. The screenshot will appear in your Pictures > Screenshots folder.</li>
            <li>
            <q-uploader
              ref="fileuploader"
              url=""
              @added="file_selected"
              style="max-width: 300px"
            >
              <template v-slot:header="scope">
                <div class="row no-wrap items-center q-pa-sm q-gutter-xs">
                  <div class="col">
                    <div class="q-uploader__title">Upload the screenshot here</div>
                  </div>
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
            <div v-if="this.fileSuccessfullyUploaded" class="text-green">Successfully uploaded</div>
            </li>
          </ol>
        </q-card-section>
      </q-card>
      <q-card>
        <q-card-section>
          3) Do something with ergonomics
        </q-card-section>
        <q-separator inset />
        <q-card-section>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </q-card-section>
        <q-separator inset />
        <q-card-section>
          <q-checkbox v-model="hasDoneErgonomicsThing" label="I have done the ergonomics thing" />
        </q-card-section>
      </q-card>
      <div class="row items-center">
        <q-btn :color="isComplete ? 'green': 'white'" :text-color="isComplete ? 'white' : 'black'" label="Submit" :disabled="!hasReadPolicy || !hasPerformedSpeedTest || !hasDoneErgonomicsThing" @click="isComplete=true" />
        <div v-if="isComplete" class="text-green q-pl-sm">Thank you! You have completed the telework policy exercises.</div>
      </div>
    </div>
  </q-page>
</template>

<style scoped lang="scss">
  .header {
    top: 50px;
  }
</style>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

@Component
export default class TeleworkPolicy extends Vue{
  private hasReadPolicy = false;
  private hasPerformedSpeedTest = false;
  private hasDoneErgonomicsThing = false;
  private isComplete = false;
  
  private selectedFile: File = new File([''], '')
  private fileSuccessfullyUploaded = false

  private file_selected(file: Array<File>) {
    this.selectedFile = file[0];
  }

  private uploadFile() {
    let fd = new FormData();
    fd.append('file', this.selectedFile)
    
    const delay = t => new Promise(resolve => setTimeout(resolve, t));

    delay(1000).then(() => {
      this.$refs.fileuploader.reset() // eslint-disable-line
      this.hasPerformedSpeedTest = true
      this.fileSuccessfullyUploaded = true
      setTimeout(() => this.fileSuccessfullyUploaded = false, 5000)
    });

    // PerformanceReviewDataService.uploadSignedPositionDescription(fd)
    //   .then((response: SignedPositionDescriptionUploadServerResponse) => {
    //     if (response.status == 200) {
    //       this.$refs.fileuploader.reset() // eslint-disable-line
    //       this.uploadedPositionDescriptionUrl = response.data // eslint-disable-line
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

  $refs!: {
    fileuploader: HTMLFormElement
  }
}
</script>

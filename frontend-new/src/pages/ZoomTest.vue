<template>
<q-layout view="lHh Lpr lFf">
  <q-page-container>
    <q-page class="row items-center">
      <div class="col">
        <div class="row justify-center items-center">
          <q-btn :disable="authenticated()" href="https://zoom.us/oauth/authorize?response_type=code&client_id=PFvjFxQERmqeMKlaJ_R4g&redirect_uri=https://team-staging.lcog.org/zoom">
            Authenticate
          </q-btn>
          <q-icon v-if="authenticated()" name="check" color="green" size="2em" />
        </div>
        <div class="row justify-center q-mt-md">
          <q-btn :disable="!authenticated()" @click="makeZoomLink()">
            Make me a Zoom meeting!
          </q-btn>
        </div>
        {{ zoomAuthenticationCode }}
        {{ zoomAuthenticationCode !== '' }}
        <div class="row justify-center">{{ zoomLink }}</div>
      </div>
    </q-page>
  </q-page-container>
</q-layout>
</template>

<style lang="scss">
</style>

<script setup lang="ts">
import { ref } from 'vue'

import { useRoute } from 'vue-router';
import { useUserStore } from 'src/stores/user'

const route = useRoute()
const userStore = useUserStore()

const danUserId = '7826406771'

let zoomAuthenticationCode = route.query.code
let zoomLink = ref('')

function authenticated(): boolean {
  return zoomAuthenticationCode !== ''
}

function makeZoomLink(): void {
  userStore.createZoomMeeting(danUserId)
    .then(meetingLink => {
      debugger
      zoomLink.value = meetingLink
    })
    .catch(e => {
      console.error('Error creating a zoom meeting:', e)
    })
}
</script>

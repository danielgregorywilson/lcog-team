<template>
<q-layout view="lHh Lpr lFf">
  <q-page-container>
    <q-page class="row items-center">
      <div class="col">
        <div class="row justify-center items-center">
          <q-btn :disable="hasAuthorizationCode()" href="https://zoom.us/oauth/authorize?response_type=code&client_id=PFvjFxQERmqeMKlaJ_R4g&redirect_uri=https://team-staging.lcog.org/zoom">
            Get Auth Code
          </q-btn>
          <q-icon v-if="hasAuthorizationCode()" name="check" color="green" size="2em" />
        </div>
        <div class="row justify-center items-center q-mt-md">
          <q-btn :disable="!hasAuthorizationCode() || hasAccessToken()" @click="getAccessToken()">
            Get Access Token
          </q-btn>
          <q-icon v-if="hasAccessToken()" name="check" color="green" size="2em" />
        </div>
        <div class="row justify-center q-mt-md">
          <q-btn :disable="!hasAccessToken()" @click="makeZoomLink()">
            Make me a Zoom meeting!
          </q-btn>
        </div>
        <div>Authorization Code: {{ authorizationCode() }}</div>
        <div>Access Token: {{ accessToken }}</div>
        <div class="row justify-center">{{ zoomLink }}</div>
        {{ ABC }}A
      </div>
    </q-page>
  </q-page-container>
</q-layout>
</template>

<style lang="scss">
</style>

<script setup lang="ts">
import { ref, Ref } from 'vue'

import { useRoute } from 'vue-router';
import { useUserStore } from 'src/stores/user'

const route = useRoute()
const userStore = useUserStore()

const ABC = import.meta.env.VUE_APP_ZOOM_CLIENT_ID

const danUserId = '7826406771'

let accessToken = ref('')
let zoomLink = ref('')

function authorizationCode(): Ref<string> {
  if (route.query.code === undefined) {
    return ref('')
  }
  return ref(route.query.code as string)
}

function hasAuthorizationCode(): boolean {
  return authorizationCode().value !== ''
}

function hasAccessToken(): boolean {
  return typeof accessToken.value == 'string' && accessToken.value !== ''
}

function getAccessToken(): void {
  userStore.getZoomAccessToken(authorizationCode().value)
  .then(accessToken => {
    accessToken.value = accessToken
  })
  .catch(e => {
    console.error('Error requesting a zoom access token:', e)
  })
}

function makeZoomLink(): void {
  userStore.createZoomMeeting(danUserId)
    .then(meetingLink => {
      zoomLink.value = meetingLink
    })
    .catch(e => {
      console.error('Error creating a zoom meeting:', e)
    })
}
</script>

<template>
<div>
  <div v-if="action.type == 'LINK'">
    <q-btn
      @click="navigateToURL(action.url.toString())"
      color="secondary"
      :label="action.name"
    />
    {{ action.description }}
  </div>
  <div v-if="action.type == 'API'">
    <div v-if="action.name == 'Open a new employee ticket'" class="q-mb-sm">
      <q-btn
        @click="authenticateWithGTA()"
        color="secondary"
        label="Authenticate with GoToAssist"
      >
        <q-icon
          v-if="authStore.goToAuthCode != ''" name="check" class="q-ml-sm"
        />
      </q-btn>
      ->
      <q-btn
        @click="authStore.createNewIncident(authStore.goToAccessToken)"
        color="secondary"
        :label="action.name"
        :disable="!authStore.goToAuthCode"
      >
        <!-- <q-icon
          v-if="authStore.goToAuthCode == ''" name="check" class="q-ml-sm"
        /> -->
      </q-btn>
    </div>
    <q-btn
      v-else
      @click="apiRequest(action.url.toString())"
      color="secondary"
      :label="action.name"
    />
    {{ action.description }}
  </div>
  <div v-if="action.type == 'EMAIL'"></div>
</div>
</template>

<script setup lang="ts">
import { Action } from 'src/types'
import { useAuthStore } from 'src/stores/auth'

const authStore = useAuthStore()

// var { AuthorizationCode } = require("simple-oauth2")
// var crypto = require("crypto")

// import { AuthorizationCode } from 'simple-oauth2'

import { OAuthClient, SessionStorage } from '@volverjs/auth-vue'

defineProps<{
  action: Action
}>()

function navigateToURL(url: string) {
  window.open(url, '_blank')
}

function apiRequest(url: string) {
  fetch(url)
    .then((response) => response.json())
    .then((data) => console.log(data));
}

function authenticateWithGTA() {
  const serviceUrl = import.meta.env.VITE_GOTO_SERVICE_URL
  const clientId = import.meta.env.VITE_GOTO_CLIENT_ID
  const redirectUri = import.meta.env.VITE_GOTO_REDIRECT_URI
  const state = encodeURIComponent(window.location.pathname)

  if (!!serviceUrl && !!clientId && !!redirectUri && !!state) {
    window.open(
      `${serviceUrl}?client_id=${clientId}&response_type=code` +
        `&redirect_uri=${redirectUri}&state=${state}`,
      '_self'
    )
  }
}

</script>

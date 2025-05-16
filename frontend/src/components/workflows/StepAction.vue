<template>
<div>
  {{ action }}
  <div v-if="action.type == 'LINK'">
    <q-btn
      @click="navigateToURL(action.url.toString())"
      color="secondary"
      :label="action.name"
    />
    {{ action.description }}
  </div>
  <div v-if="action.type == 'API'">
    <q-btn
      v-if="action.name == 'Authenticate with GoToAssist'"
      @click="authenticateWithGTA()"
      color="secondary"
      :label="action.name"
    />
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
  const serviceUrl = import.meta.env.VITE_OAUTH_SERVICE_URL
  const clientId = import.meta.env.VITE_OAUTH_CLIENT_ID
  const clientSecret = import.meta.env.VITE_OAUTH_CLIENT_SECRET
  const redirectUri = import.meta.env.VITE_OAUTH_REDIRECT_URI
  const state = encodeURIComponent(window.location.pathname)

  if (!!serviceUrl && !!clientId && !!clientSecret) {
    window.open(
      `https://authentication.logmeininc.com/oauth/authorize?client_id=${clientId}&response_type=code&redirect_uri=${redirectUri}&state=${state}`,
      '_self'
    )
    
    // require("dotenv").config();
    // var { AuthorizationCode } = require("simple-oauth2");
    // var crypto = require("crypto");

    // var oauthConfig = {
    //     client: {
    //         id: clientId,
    //         secret: clientSecret
    //     },
    //     auth: {
    //         tokenHost: serviceUrl
    //     }
    // };
    // var oauthClient = new AuthorizationCode(oauthConfig);

    // var expectedStateForAuthorizationCode = crypto.randomBytes(15).toString('hex');
    // var authorizationUrl = oauthClient.authorizeURL({
    //     redirect_uri: redirectUri,
    //     scope: 'messaging.v1.send',
    //     state: expectedStateForAuthorizationCode
    // });
    // console.log('Open in browser to send a SMS: ', authorizationUrl);


    // const authClient = new OAuthClient({
    //   url, // The URL of the OAuth issuer
    //   clientId, // The client id of the application
    //   // The client authentication method, default: 'none'
    //   // Are also supported: 'client_secret_basic', 'client_secret_post' and 'private_key_jwt'
    //   tokenEndpointAuthMethod: 'none',
    //   // The scopes requested to the OAuth server
    //   scopes: 'openid profile email',
    //   // The storage to use for persisting the refresh token, default: new LocalStorage('oauth')
    //   storage: new SessionStorage('my-session-storage')
    // })

    // authClient.initialize().then(() => {
    //   debugger
    // }).catch((error) => {
    //   console.error('Error initializing OAuth client:', error)
    // })
  }
  
  
  
  
  // var oauthConfig = {
  //   client: {
  //       id: process.env.VITE_OAUTH_CLIENT_ID,
  //       secret: process.env.VITE_OAUTH_CLIENT_SECRET
  //   },
  //   auth: {
  //       tokenHost: process.env.VITE_OAUTH_SERVICE_URL
  //   }
  // }
  // var oauthClient = new AuthorizationCode(oauthConfig)
  // debugger
  // var expectedStateForAuthorizationCode = crypto.randomBytes(15).toString('hex')
  // var authorizationUrl = oauthClient.authorizeURL({
  //     redirect_uri: process.env.OAUTH_REDIRECT_URI,
  //     scope: 'messaging.v1.send',
  //     state: expectedStateForAuthorizationCode
  // })
  // console.log('Open in browser to send a SMS: ', authorizationUrl)
}

</script>

<template>
  <q-page padding>
    <form class="login" @submit.prevent="login">
      <h4>Sign in</h4>
      <div class="row q-pa-xs">
        <label class="q-pr-sm">User name</label>
        <input 
          required
          v-model="username"
          id="username"
          type="text"
          placeholder="Snoopy"
          autocapitalize="none"
        />
      </div>
      <div class="row q-pa-xs">
        <label class="q-pr-sm">Password</label>
        <input
          required
          v-model="password"
          id="password"
          type="password"
          placeholder="Password"
        />
      </div>
      <hr/>
      <button type="submit">Login</button>
      </form>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
  
function login(): void {
  authStore.usernameAuthRequest(
    { username: username.value, password: password.value }
  )
    .then(() => router.push('/'))
    .catch((err) => console.log(err))
}

</script>

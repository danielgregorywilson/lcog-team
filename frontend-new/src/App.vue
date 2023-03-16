<template>
  <router-view />
</template>

<script lang="ts">
import axios from 'axios'
import { defineComponent } from 'vue'

const token = localStorage.getItem('user-token')
if (token) {
  axios.defaults.headers.common['Authorization'] = `Token ${ token }`
}

export default defineComponent({
  name: 'App'
});
</script>

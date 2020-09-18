<template>
  <div id="q-app">
    <router-view />
  </div>
</template>
<script lang="ts">
import axios from 'axios';
import { defineComponent } from '@vue/composition-api';

const token = localStorage.getItem('user-token')
if (token) {
  axios.defaults.headers.common['Authorization'] = 'Token ' + token
}

export default defineComponent({
  name: 'App',
});
</script>

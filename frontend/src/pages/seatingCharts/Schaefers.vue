<template>
  <q-page class="row items-center justify-evenly">
    <router-view></router-view>
  </q-page>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

@Component
export default class Schaefers extends Vue{}
</script>

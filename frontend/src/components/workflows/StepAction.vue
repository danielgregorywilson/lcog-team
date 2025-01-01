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
  <div v-if="action.type == 'API'"></div>
  <div v-if="action.type == 'EMAIL'"></div>
</div>
</template>

<script setup lang="ts">
import { Action } from 'src/types'

defineProps<{
  action: Action
}>()

function navigateToURL(url: string) {
  window.open(url, '_blank')
}

</script>

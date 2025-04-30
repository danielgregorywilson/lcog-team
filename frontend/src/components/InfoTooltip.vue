<template>
<q-avatar icon="help" size="25px" font-size="20px" color="white" text-color="primary">
  <q-tooltip :delay="100"><div id="tooltip-text" v-html="text"></div></q-tooltip>
</q-avatar>
</template>

<style scoped lang="scss">
#tooltip-text {
  font-size: 16px;
}
</style>

<script setup lang="ts">
defineProps<{
  text: string
}>()
</script>

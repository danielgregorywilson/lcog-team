<template>
  <div class="row q-mb-md">
    <q-btn-group push>
      <q-btn push color="primary" glossy label="Active" :to="{ name: 'workflow-dashboard' }" />
      <q-btn push color="secondary" glossy label="Complete" :to="{ name: 'workflows-complete-onboarding' }" />
      <q-btn push color="primary" glossy label="Deleted" :to="{ name: 'workflows-archived' }"  />
    </q-btn-group>
  </div>
  <router-view />
</template>

<script setup lang="ts">


</script>

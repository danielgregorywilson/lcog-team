<template>
  <q-page class="">
    <div class="header">
      <div class="row items-center q-gutter-md q-ma-none">
        <div>Schaefers</div>
        <q-btn-group push class="">
          <q-btn push color="secondary" glossy label="First Floor" :to="{ name: 'schaefers-1' }" />
          <q-btn push color="secondary" glossy label="Second Floor" :to="{ name: 'schaefers-2' }" />
          <q-btn push color="secondary" glossy label="Third Floor" :to="{ name: 'schaefers-3' }"  />
        </q-btn-group>
        <div>Park Place</div>
        <q-btn-group push class="">
          <q-btn push color="secondary" glossy label="Fourth Floor" :to="{ name: 'park-place-4' }" />
          <q-btn push color="secondary" glossy label="Fifth Floor" :to="{ name: 'park-place-5' }" />
        </q-btn-group>
      </div>
    </div>
    <router-view></router-view>
  </q-page>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

@Component
export default class SeatingCharts extends Vue{}
</script>

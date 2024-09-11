<template>
  <q-layout view="lHh Lpr lFf">
    <q-page-container>
      <q-page class="row justify-center">
        <div class="header row justify-between">
          <!-- <div class="row items-center q-gutter-md q-ma-none">
            <div>Schaefers</div>
            <q-btn-group push class="">
              <q-btn push color="primary" glossy label="First Floor" :to="{ name: 'schaefers-1' }" />
              <q-btn push color="primary" glossy label="Second Floor" :to="{ name: 'schaefers-2' }" />
              <q-btn push color="primary" glossy label="Third Floor" :to="{ name: 'schaefers-3' }"  />
            </q-btn-group>
            <div>Park Place</div>
            <q-btn-group push class="">
              <q-btn push color="primary" glossy label="Fourth Floor" :to="{ name: 'park-place-4' }" />
              <q-btn push color="primary" glossy label="Fifth Floor" :to="{ name: 'park-place-5' }" />
            </q-btn-group>
          </div> -->
          <!-- <q-icon name="help" color="primary" size="48px" class="q-mr-md q-mt-lg cursor-pointer" @click="showHelp = !showHelp" /> -->
        </div>
        
        <router-view></router-view>

        <q-dialog v-model="showHelp">
          <q-card id="help-dialog">
            <q-card-section class="q-ma-lg">
              <div class="row items-center q-gutter-lg">
                <q-avatar icon="meeting_room" size="100px" font-size="52px" color="primary" text-color="white" />
                <div class="text-h5">
                  <div>1) Select your name from the dropdown</div>
                  <div>2) Select an available (yellow or orange) desk</div>
                  <div>3) Click “Reserve”</div>
                </div>
              </div>
            </q-card-section>

            
          </q-card>
        </q-dialog>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<style lang="scss"> 
#help-dialog {
  max-width: 700px;
}
</style>

<script setup lang="ts">
import { ref, watch } from 'vue'

import useEventBus from 'src/eventBus'

const { bus } = useEventBus()

let showHelp = ref(false)

// We trigger opening the help dialog in Schaefers1.vue, Schaefers2.vue,
// and Schaefers3.vue.
watch(() => bus.value.get('showReservationHelpDialog'), () => {
  showHelp.value = true
})
</script>

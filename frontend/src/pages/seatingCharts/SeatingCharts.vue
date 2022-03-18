<template>
  <q-page class="">
    <div class="header row justify-between">
      <div class="row items-center q-gutter-md q-ma-none">
        <div>Schaefers</div>
        <q-btn-group push class="">
          <q-btn push color="primary" glossy label="First Floor" :to="{ name: 'schaefers-1' }" />
          <q-btn push color="primary" glossy label="Second Floor" :to="{ name: 'schaefers-2' }" />
          <q-btn push color="primary" glossy label="Third Floor" :to="{ name: 'schaefers-3' }"  />
        </q-btn-group>
        <!-- <div>Park Place</div>
        <q-btn-group push class="">
          <q-btn push color="primary" glossy label="Fourth Floor" :to="{ name: 'park-place-4' }" />
          <q-btn push color="primary" glossy label="Fifth Floor" :to="{ name: 'park-place-5' }" />
        </q-btn-group> -->
      </div>
      <q-icon name="help" color="primary" size="48px" class="q-mr-md q-mt-lg cursor-pointer" @click="showHelp = !showHelp" />
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
</template>

<style lang="scss"> 

#help-dialog {
  max-width: 700px;
}

</style>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

@Component
export default class SeatingCharts extends Vue{

  private showHelp = false;

}
</script>

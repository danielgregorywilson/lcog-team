<template>
  <q-layout view="lHh Lpr lFf">
    <q-page-container>
      <q-page class="row items-center">
        <div class="col">
          <div class="text-h4 q-mb-lg row justify-center">Click to access PTC or Carina</div>
          <div class="kiosk-button-container row justify-center">
            <q-btn class="kiosk-button" href="https://orptc.dcisoftware.com/?isSessionOut=1">
              <q-img
                class="kiosk-image"
                src="../assets/ptc-logo.png"
              />
            </q-btn>
            <q-btn class="kiosk-button" href="https://www.carina.org/homecare/medicaid/oregon/:token">
              <q-img
                class="kiosk-image"
                src="../assets/carina-logo.png"
              />
            </q-btn>
          </div>
      </div>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<style lang="scss"> 
  .kiosk-button-container {
    margin: auto;
    display: flex;
    justify-content: space-around;
    align-items: center;
  }

  .kiosk-button {
    width: 500px;
    height: 400px;
  }

  .kiosk-image{
    width: 450px;
    height: auto;
  }
</style>

<script lang="ts">

import { Component, Vue } from 'vue-property-decorator'

@Component
export default class SchaefersKiosk extends Vue{

}
</script>

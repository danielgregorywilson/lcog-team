<template>
<q-layout view="lHh Lpr lFf">
  <q-page-container>
    <q-page class="row items-center">
      <div class="col">
        <div class="text-h4 q-mb-lg row justify-center">
          Click to access PTC, Carina, or Orchards
        </div>
        <div class="kiosk-button-container row justify-center">
          <q-btn
            class="kiosk-button"
            href="https://orptc.dcisoftware.com/?isSessionOut=1"
          >
            <q-img
              class="kiosk-image"
              src="../assets/ptc-logo.png"
            />
          </q-btn>
          <q-btn
            class="kiosk-button"
            href="https://www.carina.org/homecare/medicaid/oregon/:token"
          >
            <q-img
              class="kiosk-image"
              src="../assets/carina-logo.png"
            />
          </q-btn>
          <q-btn
            class="kiosk-button"
            href="https://www.orchardsbcu.com/Public/ApplicantDisclosure"
          >
            <q-img
              class="kiosk-image"
              src="../assets/orchards-logo.png"
            />
          </q-btn>
          <q-btn
            class="kiosk-button"
            href="https://www.carewellseiu503.org/training/orientation/"
          >
            <q-img
              class="kiosk-image"
              src="../assets/carewell-logo.jpg"
              style="width: 410px;"
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
    margin-bottom: 30px;
  }

  .kiosk-image{
    width: 450px;
    height: auto;
  }
</style>

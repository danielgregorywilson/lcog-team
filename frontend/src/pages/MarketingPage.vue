<template>
<q-layout view="lHh Lpr lFf">
  <q-page-container>
    <q-page>
      <div class="row items-center q-pa-sm q-pl-md">
        <q-img
          src="../assets/summit-suite-logo.png"
          style="width: 150px;"
          class="q-mr-md"
        />
        <div class="title">Public Interest Software for Governments by LCOG</div>
      </div>
      <q-img
        src="../assets/mountainbkg_right@10x.png"
      />
      <div id="hero-text" class="row items-center q-pl-xl q-pb-xl">
        <div class="col">
          <div class="hero-text-header">Simple Tools for Smoother Operations</div>
          <div class="q-pt-sm">Government teams run on processes—but too often, the software meant to support them is expensive, bloated, or just doesn’t fit. Summit Suite is a collection of lightweight, modular apps designed to streamline essential tasks without unnecessary complexity.</div>
          <div class="q-pt-sm">Each app in the suite does one thing well—whether it’s managing employee transitions, reconciling credit card purchases, or automating multi-step approval processes.</div>
        </div>
        <div class="col">
          <div class="row items-center justify-center">
            <q-btn>Get Involved</q-btn>
          </div>
        </div>
      </div>
      <div id="hero-subtext" class="row items-center q-py-xl q-pr-lg">
        <div class="col"></div>
        <div class="col">
          <div class="hero-subtext-header">Individually powerful, better together. </div>
          <div>Summit Suite’s tools are designed to integrate seamlessly with your existing systems while remaining flexible, affordable, and easy to use.</div>
        </div>
      </div>
      <div class="row product items-center q-pl-md">
        <div class="col">
          <div>Workflows</div>
          <div>A lot of text. A lot of text. A lot of text. A lot of text. A lot of text. A whole lotta of text. A whole lotta of text. A whole lotta of text. A whole lotta of text. A whole lotta of text. A whole lotta of text. A whole lotta of text. A whole lotta of text. A whole lotta of text. A whole lotta of text. A whole lotta of text.</div>
        </div>
        <div class="col">
          <div class="row items-center justify-center">
            <q-btn>Get Involved</q-btn>
          </div>
        </div>
      </div>
    </q-page>
  </q-page-container>
</q-layout>
</template>

<style lang="scss">
.q-header {
  display: none;
}

.title {
  color: #191C20;
  font-family: 'Raleway';
  font-size: 36px;
  font-style: normal;
  font-weight: 400;
  line-height: 44px; /* 122.222% */
}

#hero-image {
  height: 150px;
}

#hero-text {
  background-color: #1D2D3A;;
  font-family: 'Raleway';
  font-size: 24px;
  color: #F8F9FF;
 
  .hero-text-header {
    color: #D2E4FF;
    font-size: 32px;
  }
}

#hero-subtext {
  background-color: #F9E287;
  font-family: 'Raleway';
  font-size: 24px;
  color: #191C20;

  .hero-subtext-header {
    font-size: 32px;
  }
}

.product {
  background-color: pink;
  height: 300px;
}







</style>

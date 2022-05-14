<template>
  <q-page id="schaefers-page" class="row items-center justify-evenly">
    <div class="col">
      <div>
        <router-view></router-view>
      </div>
    </div>

    <q-dialog
      v-model="showScreensaver"
      :maximized="true"
      transition-show="slide-up"
      transition-hide="slide-down"
      @mousemove="mouseMoveOverScreensaver"
    >
      <q-card class="row items-center justify-center">
        <q-card-section>
          <div class="text-h6 row justify-center">Oh, I'm sorry. We weren't expecting you.</div>
          <div class="text-h6 row justify-center">Please, move the mouse to wake.</div>
        </q-card-section>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<style lang="scss"> 

#schaefers-page {
  width: 1366px;
}

</style>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

@Component
export default class Schaefers extends Vue{
  private showScreensaver = false

  mouseMoveOverScreensaver() {
    this.showScreensaver = false
  }

  mounted() {
    const hourOfDay = new Date().getHours()
    if (hourOfDay < 6 || hourOfDay >= 18) {
      this.showScreensaver = true
    }
  }
}
</script>

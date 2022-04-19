<template>
  <q-page id="schaefers-page" class="row items-center justify-evenly">
    <div class="col">
      <div>
        <router-view></router-view>
      </div>
      <div class="row justify-center" id="refresh-timer">Time to refresh: {{ count }}</div>
    </div>
  </q-page>
</template>

<style lang="scss"> 

#schaefers-page {
  width: 1366px;
}

#refresh-timer {
  // margin-top: -80px;
}

</style>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

@Component
export default class Schaefers extends Vue{
  // TODO: Remove. This is a temporary timer to refresh the page every 10 minutes so we get updates from other screens.
  private count: number = 60 * 5

  mounted() {
    // TODO: Remove timer.
    // var el = document.getElementById('time-to-update');
    setInterval(() => {
        this.count -= 1;
        // el.innerHTML = count;
        if (this.count <= 0) {
            location.reload();
        }
    }, 1000);
  }

}
</script>

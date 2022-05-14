<template>
  <q-page id="schaefers-page" class="row items-center justify-evenly">
    <div class="col">
      <div>
        <router-view></router-view>
      </div>
    </div>
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
}
</script>

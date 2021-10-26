<template>
  <q-page>
    <div class="q-ma-sm">
      <div class="text-h4 text-center">Release Notes</div>
      <vue-release-notes v-bind:releases="releaseNotes" />
    </div>
  </q-page>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import VueReleaseNotes from 'vue-release-notes'
import 'vue-release-notes/dist/vue-release-notes.css'
import { releases } from '../releaseNotes'

@Component({
  components: { VueReleaseNotes } // eslint-disable-line @typescript-eslint/no-unsafe-assignment
})
export default class ReleaseNotes extends Vue{
  private releaseNotes = releases
}
</script>

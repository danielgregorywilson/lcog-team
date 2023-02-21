<template>
  <div>
    <div v-if="action.type == 'LINK'">
      <q-btn
        @click="navigateToURL(action.url)"
        color="secondary"
        :label="action.name"
      />
      {{ action.description }}
    </div>
    <div v-if="action.type == 'API'"></div>
    <div v-if="action.type == 'EMAIL'"></div>
  </div>
</template>

<style scoped lang="scss">
</style>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import { Action } from '../../store/types'

@Component
export default class StepAction extends Vue {
@Prop({required: true}) readonly action!: Action

public navigateToURL(url: string) {
  window.open(url, '_blank');
}

}
</script>

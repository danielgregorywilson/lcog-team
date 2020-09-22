<template>
  <q-item
    clickable
    :to="link"
  >
    <q-item-section
      v-if="icon"
      avatar
    >
      <q-icon :name="icon" />
    </q-item-section>

    <q-item-section>
      <q-item-label>{{ title }}</q-item-label>
    </q-item-section>
  </q-item>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'

@Component
export default class NavLink extends Vue{
  @Prop({required: true}) readonly title!: string
  @Prop({default: '#'}) readonly link!: string
  @Prop({default: ''}) readonly icon!: string
};
</script>

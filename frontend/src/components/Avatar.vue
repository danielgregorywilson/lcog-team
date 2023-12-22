<template>
  <div class="avatar">
    <div v-if="!photo" class="initials">{{ initials }}</div>
    <img v-else :src="photo" alt="User avatar">
    <q-tooltip :delay="300" :offset="[0, 10]">{{ name }}</q-tooltip>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue'

export default defineComponent({
  name: 'Avatar',
  props: {
    initials: {
      type: String,
      default: ''
    },
    photo: {
      type: String as PropType<string | undefined>,
      default: undefined
    },
    name: {
      type: String,
      default: ''
    }
  }
})
</script>

<style scoped>
.avatar {
  display: inline-block;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #ccc;
  text-align: center;
  font-size: 20px;
  line-height: 40px;
  overflow: hidden;
}

.initials {
  color: #fff;
}
</style>
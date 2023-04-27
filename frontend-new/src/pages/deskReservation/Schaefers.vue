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

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

import TrustedIPDataService from 'src/services/TrustedIPDataService'
import { useAuthStore } from 'src/stores/auth'

const authStore = useAuthStore()
const router = useRouter()

let showScreensaver = ref(false)

function mouseMoveOverScreensaver() {
  showScreensaver.value = false
}

onMounted(() => {
  // Boot session to dashboard if not authenticated or IP not in trusted IP lists
  if (!authStore.isAuthenticated) {
    TrustedIPDataService.getTrustedIPs()
      .then((response: {data: boolean}) => {
        const addressIsSafe = response.data
        if (!addressIsSafe) {
          router.push('/')
            .catch((e) => {
              console.error('Error navigating to dashboard upon rejecting connection to desk reservations:', e)
            })
        }
      })
      .catch(e => {
        console.error('Error getting safe IP address status from API:', e)
      })
  }
  
  const hourOfDay = new Date().getHours()
  if (hourOfDay < 6 || hourOfDay >= 18) {
    showScreensaver.value = true
  }
})
</script>

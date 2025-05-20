<script setup lang="ts">
import { useAuthStore } from 'src/stores/auth'
import { onMounted } from 'vue'

const authStore = useAuthStore()

onMounted(() => {
  const params = new URLSearchParams(window.location.search)
  const code = params.get('code')
  const state = params.get('state')
  if (!!code && !!state) {
    authStore.setGoToAuthCode(code).then(() => {
      authStore.getGoToAccessToken(code).then(() => {
        window.location.replace(state)
      })
    })
  }
})
</script>
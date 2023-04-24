import { NavigationGuard } from 'vue-router'


import { useAuthStore } from 'src/stores/auth'


// const { cookies } = useCookies()

export const authGuard: NavigationGuard = async (to, from, next) => {
  const authStore = useAuthStore()
  if (authStore.isAuthenticated) {
    next()
    return
  }
  next('dashboard')
}
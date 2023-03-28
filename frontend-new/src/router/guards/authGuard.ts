import { useAuthStore } from 'src/stores/auth';
import type { NavigationGuard } from 'vue-router';

export const authGuard: NavigationGuard = async (to, from, next) => {
  const userStore = useAuthStore();

  // Fetch user data from the server or local storage
  await userStore.fetchUser();

  // Check if the user is authenticated
  if (userStore.isAuthenticated) {
    next();
  } else {
    // You can use try/catch to get an id token and set it to your request header
    // ex: try { ... next() } catch { ... next({ name: '/login') }
    next('/login');
  }
};
import { RouteConfig } from 'vue-router';

import authStore from '../store/modules/auth' // Vuex Store


const ifNotAuthenticated = (to, from, next) => {
  if (!authStore?.state?.token) { // TODO: This should use the isAuthenticated getter
    next()
    return
  }
  next('/')
}

const ifAuthenticated = (to, from, next) => {
  if (!!authStore?.state?.token) { // TODO: This should use the isAuthenticated getter
    next()
    return
  }
  next('auth/login')
}

const routes: RouteConfig[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        alias: '/dashboard',
        name: 'dashboard',
        component: () => import('pages/Index.vue'),
        beforeEnter: ifAuthenticated,
      },
      {
        path: 'pr/:pk',
        name: 'pr-details',
        component: () => import('pages/PerformanceReviewDetail.vue'),
        beforeEnter: ifAuthenticated,
      },
      {
        path: '/time-off',
        name: 'time-off',
        component: () => import('pages/TimeOffRequests.vue'),
        beforeEnter: ifAuthenticated,
      }
    ]
  },
  {
    path: '/auth',
    component: () => import('layouts/AuthLayout.vue'),
    children: [
      {
        path: 'login',
        name: 'login',
        component: () => import('pages/auth/Login.vue'),
        beforeEnter: ifNotAuthenticated,
      },
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '*',
    component: () => import('pages/Error404.vue')
  }
];

export default routes;

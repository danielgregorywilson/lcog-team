import { RouteConfig } from 'vue-router';

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
      },
      {
        path: 'pr/:pk',
        name: 'pr-details',
        component: () => import('pages/PerformanceReviewDetail.vue')
      },
      {
        path: '/time-off',
        name: 'time-off',
        component: () => import('pages/TimeOffRequests.vue')
      }
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

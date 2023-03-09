import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', component: () => import('pages/IndexPage.vue') }],
  },

  /////////////////////////
  // MEALS ON WHEELS MAP //
  /////////////////////////
  {
    path: '/mow-map',
    name: 'mow-map',
    component: () => import('src/pages/meals/MOWMap.vue'),
    // beforeEnter: ifCanViewMealsOnWheelsRoutes
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;

import { NavigationGuardNext, RouteLocation, RouteRecordRaw } from 'vue-router'


// TODO: Route guards don't work with Pinia
// https://pinia.vuejs.org/core-concepts/outside-component-usage.html
const ifAuthenticated = (to: RouteLocation, from: RouteLocation, next: NavigationGuardNext) => {
  // const authStore = useAuthStore()
  // if (authStore.isAuthenticated) { // TODO: This should use the isAuthenticated getter
  //   next()
  //   return
  // }
  // next('dashboard')
}

const ifCanViewTimeOffRequest = (to: RouteLocation, from: RouteLocation, next: NavigationGuardNext) => {
  next()
  // const toPk = typeof to.params.pk == 'string' ? to.params.pk : to.params.pk[0]
  // if (
  //   authStore.isAuthenticated && cookies.get('time_off_requests_can_view') &&
  //   cookies.get('time_off_requests_can_view').indexOf(toPk) != -1
  // ) {
  //   next()
  //   return
  // } else {
  //   next('/timeoff')
  // }
}




const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '/', redirect: '/dashboard' },
      {
        path: '/dashboard',
        name: 'dashboard',
        component: () => import('pages/Dashboard.vue')
      },
      {
        path: 'release-notes',
        name: 'release-notes',
        component: () => import('src/pages/ReleaseNotes.vue')
      },
      {
        path: '/profile',
        name: 'profile',
        component: () => import('src/pages/Profile.vue'),
        // beforeEnter: ifAuthenticated
      },
      //////////////////////
      // RESPONSIBILITIES //
      //////////////////////
      {
        path: '/responsibilities',
        name: 'responsibilities',
        component: () => import('src/pages/responsibilities/Responsibilities.vue'),
        redirect: {name: 'all-responsibilities'},
        children: [
          {
            path: 'all',
            name: 'all-responsibilities',
            component: () => import('src/pages/responsibilities/AllResponsibilities.vue'),
          },
          {
            path: 'orphaned',
            name: 'orphaned-responsibilities',
            component: () => import('src/pages/responsibilities/OrphanedResponsibilities.vue'),
          },
          {
            path: 'tag',
            name: 'tag',
            component: () => import('src/pages/responsibilities/Tags.vue'),
            children: [
              {
                path: 'all',
                name: 'all-tags',
                component: () => import ('src/pages/responsibilities/AllTags.vue')
              },
              {
                path: ':pk',
                name: 'tagged-responsibilities',
                component: () => import ('src/pages/responsibilities/TaggedResponsibilities.vue')
              }
            ]
          },
          {
            path: ':pk',
            name: 'employee-responsibilities',
            component: () => import('src/pages/responsibilities/EmployeeResponsibilities.vue'),
            children: [
              {
                path: 'secondary',
                name: 'employee-secondary-responsibilities',
                component: () => import('src/pages/responsibilities/EmployeeResponsibilities.vue'),
                props: { secondary: true }
              }
            ]
          }
        ]
      },
      //////////////
      // TIME OFF //
      //////////////
      {
        path: '/timeoff',
        name: 'timeoff',
        component: () => import('src/pages/timeoff/TimeOffBase.vue'),
        meta: { requiresAuth: true },
        redirect: {name: 'timeoff-my-requests'},
        children: [
          {
            path: 'calendar',
            name: 'timeoff-calendar',
            component: () => import('src/pages/timeoff/Calendar.vue'),
          },
          {
            path: 'new-request',
            name: 'timeoff-new-request',
            component: () => import('src/pages/timeoff/NewRequest.vue'),
          },
          {
            path: 'my-requests',
            name: 'timeoff-my-requests',
            component: () => import('src/pages/timeoff/MyRequests.vue'),
          },
          {
            path: 'request-detail/:pk',
            name: 'timeoff-request-detail',
            component: () => import('src/pages/timeoff/RequestDetail.vue'),
            beforeEnter: ifCanViewTimeOffRequest,
          },
          {
            path: 'manage-requests',
            name: 'timeoff-manage-requests',
            component: () => import('src/pages/timeoff/ManageRequests.vue'),
          }
        ]
      },
    ],
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

  /////////////////////////
  // USERNAME LOGIN PAGE //
  /////////////////////////
  {
    path: '/auth',
    component: () => import('layouts/AuthLayout.vue'),
    children: [
      {
        path: 'login',
        name: 'login',
        component: () => import('pages/UsernameLogin.vue'),
        // beforeEnter: ifNotAuthenticated,
      },
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;

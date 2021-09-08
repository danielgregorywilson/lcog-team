import Vue from 'vue';
import { Route, RouteConfig } from 'vue-router';

import authState from '../store/modules/auth/state'

type Next = (path?: string) => void

// const ifNotAuthenticated = (to: Route, from: Route, next: Next) => {
//   if (!authState.token) { // TODO: This should use the isAuthenticated getter
//     next()
//     return
//   }
//   next('/')
// }

const ifAuthenticated = (to: Route, from: Route, next: Next) => {
  if (!!authState.token) { // TODO: This should use the isAuthenticated getter
    next()
    return
  }
  next('dashboard')
}

const ifManager = (to: Route, from: Route, next: Next) => {
  if (Vue.prototype.$cookies.get('is_manager') == 'true') { // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-call
    next()
    return
  }
  next('dashboard')
}

const ifCanViewReview = (to: Route, from: Route, next: Next) => {
  if (Vue.prototype.$cookies.get('prs_can_view').indexOf(to.params.pk) != -1) { // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-call
    next()
    return
  } else {
    console.info('User can not view PR', to.params.pk, 'Redirecting to dashboard.')
    next('dashboard')
  }
}

const ifCanViewNote = (to: Route, from: Route, next: Next) => {
  if (Vue.prototype.$cookies.get('notes_can_view') && Vue.prototype.$cookies.get('notes_can_view').indexOf(parseInt(to.params.pk)) != -1) { // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-call
    next()
    return
  } else {
    next('dashboard')
  }
}

const ifCanViewTeleworkApplication = (to: Route, from: Route, next: Next) => {
  if (Vue.prototype.$cookies.get('telework_applications_can_view').indexOf(to.params.pk) != -1) { // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-call
    next()
    return
  } else {
    console.info('User can not view Telework Application', to.params.pk, 'Redirecting to dashboard.')
    next('dashboard')
  }
}

// TODO: Add a reset password view as in Django version, unless we're authenticating with LDAP
const routes: RouteConfig[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '/', redirect: '/dashboard' },
      {
        path: '/dashboard',
        name: 'dashboard',
        component: () => import('pages/Dashboard.vue'),
      },
      {
        path: '/reviews',
        name: 'reviews',
        component: () => import('pages/PerformanceReviews.vue'),
        beforeEnter: ifManager,
      },
      {
        path: '/note/new',
        name: 'note-create',
        component: () => import('pages/ReviewNoteCreate.vue'),
        beforeEnter: ifManager,
      },
      {
        path: '/note/:pk',
        name: 'note-details',
        component: () => import('pages/ReviewNoteDetail.vue'),
        beforeEnter: ifCanViewNote,
      },
      {
        path: '/pr/:pk',
        name: 'pr-details',
        component: () => import('pages/PerformanceReviewDetail.vue'),
        beforeEnter: ifCanViewReview,
      },
      {
        path: '/timeoff',
        name: 'timeoff',
        component: () => import('pages/TimeOffRequests.vue'),
        // beforeEnter: ifAuthenticated,
      },
      {
        path: '/telework-application',
        name: 'telework-application',
        // component: () => import('pages/TeleworkApplication.vue'),
        component: () => import('pages/TeleworkApplicationGetOrCreate.vue'),
        beforeEnter: ifAuthenticated,
      },
      {
        path: '/telework-application/:pk',
        name: 'telework-application-detail',
        component: () => import('pages/TeleworkApplication.vue'),
        beforeEnter: ifCanViewTeleworkApplication,
      },
      {
        path: '/telework',
        name: 'telework',
        component: () => import('pages/TeleworkPolicy.vue'),
        // beforeEnter: ifAuthenticated,
      },
      {
        path: '/security-message',
        name: 'security-message',
        component: () => import('pages/SecurityMessage.vue'),
        beforeEnter: ifAuthenticated,
      }
    ]
  },
  {
    path: '/print',
    component: () => import('layouts/PrintLayout.vue'),
    children: [
      {
        path: 'pr/:pk',
        name: 'pr-print',
        component: () => import('pages/PerformanceReviewDetail.vue'),
        beforeEnter: ifManager,
        props: {
          print: true
        }
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
        // beforeEnter: ifNotAuthenticated,
      },
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/404',
    component: () => import('pages/Error404.vue')
  },
  {
    path: '*',
    component: () => {
      console.log('Hit the 404')
      return import('pages/Error404.vue')
    }
  }
];

export default routes;

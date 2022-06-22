import Vue from 'vue';
import { Route, RouteConfig } from 'vue-router';

import http from '../http-common';
import authState from '../store/modules/auth/state'

import { AxiosUserRetrieveOneServerResponse } from '../store/types'


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
  if (!!authState.token && Vue.prototype.$cookies.get('is_manager') == 'true') { // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-call
    next()
    return
  }
  next('dashboard')
}

const ifEligibleForTeleworkApplication = (to: Route, from: Route, next: Next) => {
  if (!!authState.token && Vue.prototype.$cookies.get('is_eligible_for_telework_application') == 'true') { // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-call
    next()
    return
  }
  next('dashboard')
}

// const ifHasManager = (to: Route, from: Route, next: Next) => {
//   if (!!authState.token && Vue.prototype.$cookies.get('has_manager') == 'true') { // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-call
//     next()
//     return
//   }
//   next('dashboard')
// }

const ifCanViewReview = (to: Route, from: Route, next: Next) => {
  if (!!authState.token && Vue.prototype.$cookies.get('prs_can_view').indexOf(to.params.pk) != -1) { // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-call
    next()
    return
  } else {
    console.info('User cannot view PR', to.params.pk, 'Redirecting to dashboard.')
    next('dashboard')
  }
}

const ifCanViewNote = (to: Route, from: Route, next: Next) => {
  if (!!authState.token && Vue.prototype.$cookies.get('notes_can_view') && Vue.prototype.$cookies.get('notes_can_view').indexOf(parseInt(to.params.pk)) != -1) { // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-call
    next()
    return
  } else {
    next('dashboard')
  }
}

const ifCanViewTeleworkApplication = (to: Route, from: Route, next: Next) => {
  if (!!authState.token && Vue.prototype.$cookies.get('telework_applications_can_view').indexOf(to.params.pk) != -1) { // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-call
    next()
    return
  } else {
    console.info('User cannot view Telework Application', to.params.pk, 'Redirecting to dashboard.')
    next('dashboard')
  }
}

// const ifCanViewSeatingCharts = (to: Route, from: Route, next: Next) => {
//   if (!!authState.token && Vue.prototype.$cookies.get('can_view_seating_charts') == 'true') { // eslint-disable-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-call
//     next()
//     return
//   } else {
//     console.info('User cannot view seating charts. Redirecting to dashboard.')
//     next('dashboard')
//   }
// }

const ifCanViewDeskReservationReports = (to: Route, from: Route, next: Next) => {
  http.get('api/v1/current-user/')
    .then((resp: AxiosUserRetrieveOneServerResponse) => {
      if (resp.data.can_view_desk_reservation_reports) {
        next()
        return
      } else {
        console.info('User cannot view Desk Reservation Reports', to.params.pk, 'Redirecting to dashboard.')
        next('dashboard')
      }
    })
    .catch(e => {
      console.error('Error getting current user:', e)
    })
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
        component: () => import('pages/Dashboard.vue')
      },
      {
        path: 'release-notes',
        name: 'release-notes',
        component: () => import('pages/ReleaseNotes.vue')
      },
      {
        path: '/responsibilities',
        name: 'responsibilities',
        component: () => import('src/pages/responsibilities/Responsibilities.vue'),
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
            path: 'tags',
            name: 'tags',
            component: () => import('src/pages/responsibilities/Tags.vue'),
          },
          {
            path: 'tag',
            name: 'tag',
            component: () => import('src/pages/responsibilities/TaggedResponsibilities.vue'),
            children: [
              {
                path: ':pk',
                name: 'tagged-responsibilities',
                component: () => import ('src/pages/responsibilities/TaggedResponsibility.vue')
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
                props: { secondary: true }
              }
            ]
          }
        ]
      },
      {
        path: '/reviews',
        name: 'reviews',
        component: () => import('pages/PerformanceReviews.vue'),
        beforeEnter: ifManager
      },
      {
        path: '/mileage-reimbursement',
        name: 'mileage-reimbursement',
        component: () => import('src/pages/mileageReimbursement/MileageReimbursement.vue'),
        children: [
          {
            path: 'create',
            name: 'mileage-reimbursement-create',
            component: () => import('src/pages/mileageReimbursement/MileageReimbursementCreate.vue'),
          },
          {
            path: 'list',
            name: 'mileage-reimbursement-list',
            component: () => import('src/pages/mileageReimbursement/MileageReimbursementList.vue'),
          },
          // {
          //   path: 'approve',
          //   name: 'mileage-reimbursement-approve',
          //   component: () => import('src/pages/mileageReimbursement/MileageReimbursementApprove.vue'),
          // },
          // {
          //   path: ':pk',
          //   name: 'mileage-reimbursement-detail',
          //   component: () => import('src/pages/mileageReimbursement/MileageReimbursementDetail.vue'),
          // }
        ]
      },
      {
        path: '/note/new',
        name: 'note-create',
        component: () => import('pages/ReviewNoteCreate.vue'),
        beforeEnter: ifManager
      },
      {
        path: '/note/:pk',
        name: 'note-details',
        component: () => import('pages/ReviewNoteDetail.vue'),
        beforeEnter: ifCanViewNote
      },
      {
        path: '/pr/:pk',
        name: 'pr-details',
        component: () => import('pages/PerformanceReviewDetail.vue'),
        beforeEnter: ifCanViewReview
      },
      {
        path: '/timeoff',
        name: 'timeoff',
        component: () => import('pages/TimeOffRequests.vue'),
        // beforeEnter: ifAuthenticated
      },
      {
        path: '/telework-application',
        name: 'telework-application',
        // component: () => import('pages/TeleworkApplication.vue'),
        component: () => import('pages/TeleworkApplicationGetOrCreate.vue'),
        beforeEnter: ifEligibleForTeleworkApplication
      },
      {
        path: '/telework-application/:pk',
        name: 'telework-application-detail',
        component: () => import('pages/TeleworkApplication.vue'),
        beforeEnter: ifCanViewTeleworkApplication
      },
      {
        path: '/telework',
        name: 'telework',
        component: () => import('pages/TeleworkPolicy.vue'),
        // beforeEnter: ifAuthenticated
      },
      {
        path: '/security-message',
        name: 'security-message',
        component: () => import('pages/SecurityMessage.vue'),
        beforeEnter: ifAuthenticated
      },
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
  {
    path: '/desk-reservation',
    component: () => import('src/pages/deskReservation/DeskReservation.vue'),
    children: [
      {
        path: 'schaefers',
        name: 'schaefers',
        component: () => import('src/pages/deskReservation/Schaefers.vue'),
        children: [
          {
            path: '1',
            name: 'schaefers-1',
            component: () => import('src/pages/deskReservation/Schaefers1.vue'),
            children: [
              {
                path: 'desk/:deskNumber',
                name: 'schaefers-1-desk',
              }
            ]
          },
          {
            path: '2',
            name: 'schaefers-2',
            component: () => import('src/pages/deskReservation/Schaefers2.vue'),
            children: [
              {
                path: 'desk/:deskNumber',
                name: 'schaefers-2-desk',
              }
            ]
          },
          {
            path: '3',
            name: 'schaefers-3',
            component: () => import('src/pages/deskReservation/Schaefers3.vue'),
            children: [
              {
                path: 'desk/:deskNumber',
                name: 'schaefers-3-desk',
              }
            ]
          }
        ]
      },
      {
        path: 'park-place',
        name: 'park-place',
        component: () => import('src/pages/deskReservation/ParkPlace.vue'),
        children: [
          {
            path: '4',
            name: 'park-place-4',
            component: () => import('src/pages/deskReservation/ParkPlace4.vue'),
          },
          {
            path: '5',
            name: 'park-place-5',
            component: () => import('src/pages/deskReservation/ParkPlace5.vue'),
          }
        ]
      },
      {
        path: 'reports',
        name: 'reports',
        component: () => import('src/pages/deskReservation/Report.vue'),
        beforeEnter: ifCanViewDeskReservationReports
      }
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

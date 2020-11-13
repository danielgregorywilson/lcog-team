import { Route, RouteConfig } from 'vue-router';

import authState from '../store/modules/auth/state'
import userState from '../store/modules/user/state'

// import authStore from '../store/modules/auth'
import userStore from '../store/modules/user'
// import getters from '../store/modules/auth/getters'

type Next = (path?: string) => void

const ifNotAuthenticated = (to: Route, from: Route, next: Next) => {
  if (!authState.token) { // TODO: Use the isAuthenticated getter?
  // if (getters['authModule/isAuthenticated']) {
    next()
    return
  }
  next('/')
}

const ifAuthenticated = (to: Route, from: Route, next: Next) => {
  // /*
  //   Determines where we should send the user.
  // */
  // function proceed () {
  //   /*
  //     If the user has been loaded determine where we should
  //     send the user.
  //   */
  //   if ( authStore.getters.getAuthLoadStatus() == 2 ) {
  //     /*
  //       If the user is not empty, that means there's a user
  //       authenticated we allow them to continue. Otherwise, we
  //       send the user back to the home page.
  //     */
  //     if( authStore.getters.getUser != '' ){
  //       next();
  //     }else{
  //       next('/auth/login');
  //     }
  //   }
  // }
  
  // /*
  // Confirms the user has been loaded
  // */
  // if ( authStore.getters.getAuthLoadStatus != 2 ) {
  //   /*
  //     If not, load the user
  //   */
  //   authStore.dispatch( 'loadUser' );

  //   /*
  //     Watch for the user to be loaded. When it's finished, then
  //     we proceed.
  //   */
  //   authStore.watch( authStore.getters.getUserLoadStatus, function(){
  //     if( authStore.getters.getUserLoadStatus() == 2 ){
  //       proceed();
  //     }
  //   });
  // } else {
  //   /*
  //     User call completed, so we proceed
  //   */
  //   proceed()
  // }

  
  
  
  // CURRENT IMPLEMENTATION
  // console.log(authStore.state.token)
  if (!!authState.token) { // TODO: Use the isAuthenticated getter?
  // if (!getters['authModule/isAuthenticated']) {
    next()
    return
  }
  next('auth/login')
}

// TODO: Implement
// const ifManager = async (to: Route, from: Route, next: Next) => {
//   console.log('CHECK IF MANAGER')
//   console.log('userState', userState)
//   console.log('profile', userState.profile)
//   console.log('isManager', userState.profile.is_manager)
//   // debugger
//   var hasPermission = await userStore.dispatch("auth/hasPermission") //eslint-disable-line
//     if (hasPermission) {
//       next()
//     }
  
//   next()
//   if (userState.profile.employee_pk == -1) {
//     // Profile is not loaded yet, so load it
//     console.log('profile not yet loaded')
//     console.log(authState.status)
//     console.log(authState.token)
//   } else {
//     if (userState.profile.is_manager) {
//       next()
//       return
//     }
//     next('dashboard')
//   }
  
// }

// TODO: Add API guards to notes and PRs
// TODO: Add a reset password view as in Django version
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
        beforeEnter: ifAuthenticated,
      },
      {
        path: '/reviews',
        name: 'reviews',
        component: () => import('pages/PerformanceReviews.vue'),
        // TODO
        // beforeEnter: ifManager,
        beforeEnter: ifAuthenticated,
      },
      {
        path: '/note/new',
        name: 'note-create',
        component: () => import('pages/ReviewNoteCreate.vue'),
        // TODO
        // beforeEnter: ifManager,
        beforeEnter: ifAuthenticated,
      },
      {
        path: '/note/:pk',
        name: 'note-details',
        component: () => import('pages/ReviewNoteDetail.vue'),
        // TODO
        // beforeEnter: ifManager,
        beforeEnter: ifAuthenticated,
      },
      {
        path: '/pr/:pk',
        name: 'pr-details',
        component: () => import('pages/PerformanceReviewDetail.vue'),
        // TODO
        // beforeEnter: ifManager,
        beforeEnter: ifAuthenticated,
      },
      {
        path: '/timeoff',
        name: 'timeoff',
        component: () => import('pages/TimeOffRequests.vue'),
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
        // TODO
        // beforeEnter: ifManager,
        beforeEnter: ifAuthenticated,
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

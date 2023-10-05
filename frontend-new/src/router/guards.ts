import { useCookies } from 'vue3-cookies'
import { RouteLocationNormalized } from 'vue-router'

import http from 'src/http-common'
import { useAuthStore } from 'src/stores/auth'
import { EmployeeRetrieve } from 'src/types'

const { cookies } = useCookies()

export function canViewDeskReservationReports(): Promise<boolean> {
  return http.get('api/v1/current-user/')
    .then((resp: {data: EmployeeRetrieve}) => {
      if (resp.data.can_view_desk_reservation_reports) {
        return true
      } else {
        return false
      }
    })
    .catch(e => {
      console.error('Error getting current user:', e)
      return false
    })
}

export function canViewMealsOnWheelsRoutes() {
  if (cookies.get('can_view_mow_routes') == 'true') {
    return true
  } else {
    console.info('User cannot view Meals on Wheels routes. Redirecting to dashboard.')
    return false
  }
}

export function canViewTimeOffRequest(to: RouteLocationNormalized) {
  const authStore = useAuthStore()
  const toPk = typeof to.params.pk == 'string' ? to.params.pk : to.params.pk[0]
  if (
    authStore.isAuthenticated && cookies.get('time_off_requests_can_view') &&
    cookies.get('time_off_requests_can_view').indexOf(toPk) != -1
  ) {
    return true
  } else {
    return false
  }
}

export function isFiscal() {
  if (cookies.get('is_fiscal_employee') == 'true') {
    return true
  } else {
    console.info('User is not fiscal employee. Redirecting to dashboard.')
    return false
  }
}

export function isAuthenticated() {
  const authStore = useAuthStore()
  if (authStore.isAuthenticated) {
    return true
  } else {
    console.info('User cannot view Meals on Wheels routes. Redirecting to dashboard.')
    return false
  }
}

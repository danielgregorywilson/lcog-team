import { RouteLocationNormalizedLoaded } from 'vue-router'

export function getRoutePk(route: RouteLocationNormalizedLoaded) {
  if (!route || route.params.pk == undefined) {
    return null
  } else {
    return typeof route.params.pk == 'string' ? route.params.pk : route.params.pk[0]
  }
}
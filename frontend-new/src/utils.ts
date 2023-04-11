import { RouteLocationNormalizedLoaded } from 'vue-router'

export function getRouteParam(route: RouteLocationNormalizedLoaded, param = 'pk'): string | null {
  if (!route || route.params[param] == undefined) {
    return null
  } else {
    return typeof route.params[param] == 'string' ? route.params[param] : route.params[param][0]
  }
}

export function getRoutePk(route: RouteLocationNormalizedLoaded) {
  return getRouteParam(route, 'pk')
  // if (!route || route.params.pk == undefined) {
  //   return null
  // } else {
  //   return typeof route.params.pk == 'string' ? route.params.pk : route.params.pk[0]
  // }
}
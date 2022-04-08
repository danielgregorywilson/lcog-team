import http from '../http-common'
import { DeskReservationCreate } from 'src/store/types'


class DeskReservationDataService {
  getAll() {
    return http.get('api/v1/deskreservation')
  }

  create(data: DeskReservationCreate) {
    return http.post('api/v1/deskreservation', data)
  }

  cancelReservation(pk: number) {
    return http.put(`api/v1/deskreservation/${pk}/cancel-reservation`)
  }

  // delete(pk: number) {
  //   return http.delete(`api/v1/deskreservation/${pk}`)
  // }
}

export default new DeskReservationDataService();

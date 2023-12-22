import http from '../http-common';

import { TimeOffRequestUpdate, TimeOffRequestUpdatePartial } from '../store/types'

class TimeOffDataService {
  get(pk: string) {
    return http.get(`api/v1/timeoffrequest/${pk}`);
  }

  update(pk: string, data: TimeOffRequestUpdate) {
    return http.put(`api/v1/timeoffrequest/${pk}`, data);
  }

  updatePartial(pk: string, data: TimeOffRequestUpdatePartial) {
    return http.patch(`api/v1/timeoffrequest/${pk}`, data);
  }

  delete(pk: string) {
    return http.delete(`api/v1/timeoffrequest/${pk}`);
  }
}

export default new TimeOffDataService();

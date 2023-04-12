import http from '../http-common';

class TrustedIPDataService {
  getTrustedIPs() {
    return http.get('api/v1/trustedip');
  }
}

export default new TrustedIPDataService();

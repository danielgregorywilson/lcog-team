export interface SecurityMessageStateInterface {
  viewedSecurityMessages: Array<number>
  viewedLatestSecurityMessage: boolean
}

const state: SecurityMessageStateInterface = {
  viewedSecurityMessages: [],
  viewedLatestSecurityMessage: false
};

export default state;

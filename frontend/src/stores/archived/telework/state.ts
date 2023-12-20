export interface TeleworkApplicationInterface {
  pk?: number
  employee_pk?: number
  employee_name: string
  status: string
}

export interface TeleworkStateInterface {
  teleworkApplication: TeleworkApplicationInterface
  allTeleworkApplicationsSignatureRequired: Array<TeleworkApplicationInterface>
  allTeleworkApplicationsSignatureNotRequired: Array<TeleworkApplicationInterface>
}

const state: TeleworkStateInterface = {
  teleworkApplication: {pk: undefined, employee_pk: undefined, employee_name: '', status: ''},
  allTeleworkApplicationsSignatureRequired: [],
  allTeleworkApplicationsSignatureNotRequired: []
};

export default state;

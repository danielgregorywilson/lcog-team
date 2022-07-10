export interface TimeOffRequestInterface {
  pk: number
  employee_pk: number
  employee_name: string
  manager_pk: number
  date_start: Date
  date_end: Date
  approved: boolean
}

export interface TimeOffRequestStateInterface {
  myTimeOffRequests: Array<TimeOffRequestInterface>
}

const state: TimeOffRequestStateInterface = {
  myTimeOffRequests: [],
};

export default state;

// TODO
interface ReviewNoteInterface {
  employee: unknown
  note: string
}

// TODO: Update to match shape of frontend/src.store/types/PerformanceReviewRetrieve
export interface TeleworkApplicationInterface {
  pk?: number
  employee_pk?: number
  employee_name: string
  performance_period: string
  days_until_review: string
  status: string
  evaluation: string
}

export interface TeleworkStateInterface {
  teleworkApplication: TeleworkApplicationInterface
}

const state: TeleworkStateInterface = {
  teleworkApplication: {pk: undefined, employee_pk: undefined, employee_name: '', performance_period: '', days_until_review: '', status: '', evaluation: ''},
};

export default state;

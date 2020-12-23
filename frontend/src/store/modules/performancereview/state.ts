// TODO
interface ReviewNoteInterface {
  employee: unknown
  note: string
}

// TODO: Update to match shape of frontend/src.store/types/PerformanceReviewRetrieve
export interface PerformanceReviewInterface {
  pk?: number
  employee_pk?: number
  employee_name: string
  performance_period: string
  days_until_review: string
  status: string
  evaluation: string
}

export interface PerformanceReviewStateInterface {
  nextPerformanceReview: PerformanceReviewInterface
  performanceReview: PerformanceReviewInterface
  allPerformanceReviews: Array<PerformanceReviewInterface>
  allPerformanceReviewsActionRequired: Array<PerformanceReviewInterface>
  allPerformanceReviewsActionNotRequired: Array<PerformanceReviewInterface>
  allSignaturePerformanceReviewsActionRequired: Array<PerformanceReviewInterface>
  allSignaturePerformanceReviewsActionNotRequired: Array<PerformanceReviewInterface>
  performanceReviewDetails: { [id: string]: PerformanceReviewInterface } // TODO: Use this instead of performanceReview
  allReviewNotes: Array<ReviewNoteInterface>
}

const state: PerformanceReviewStateInterface = {
  nextPerformanceReview: {pk: undefined, employee_pk: undefined, employee_name: '', performance_period: '', days_until_review: '', status: '', evaluation: ''}, // TODO: This is wrong shape of PR
  performanceReview: {pk: undefined, employee_pk: undefined, employee_name: '', performance_period: '', days_until_review: '', status: '', evaluation: ''}, // TODO: This is wrong shape of PR
  allPerformanceReviews: [],
  allPerformanceReviewsActionRequired: [],
  allPerformanceReviewsActionNotRequired: [],
  allSignaturePerformanceReviewsActionRequired: [],
  allSignaturePerformanceReviewsActionNotRequired: [],
  performanceReviewDetails: {}, // TODO: Use this instead of performanceReview
  allReviewNotes: []
};

export default state;

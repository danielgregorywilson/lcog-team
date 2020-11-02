// TODO
interface ReviewNoteInterface {
  employee: unknown
  note: string
}

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
  allPerformanceReviews: Array<PerformanceReviewInterface>
  allPerformanceReviewsActionRequired: Array<PerformanceReviewInterface>
  allPerformanceReviewsActionNotRequired: Array<PerformanceReviewInterface>
  allUpperManagerPerformanceReviewsActionRequired: Array<PerformanceReviewInterface>
  allUpperManagerPerformanceReviewsActionNotRequired: Array<PerformanceReviewInterface>
  performanceReviewDetails: { [id: string]: PerformanceReviewInterface }
  allReviewNotes: Array<ReviewNoteInterface>
}

const state: PerformanceReviewStateInterface = {
  nextPerformanceReview: {pk: undefined, employee_pk: undefined, employee_name: '', performance_period: '', days_until_review: '', status: '', evaluation: ''},
  allPerformanceReviews: [],
  allPerformanceReviewsActionRequired: [],
  allPerformanceReviewsActionNotRequired: [],
  allUpperManagerPerformanceReviewsActionRequired: [],
  allUpperManagerPerformanceReviewsActionNotRequired: [],
  performanceReviewDetails: {},
  allReviewNotes: []
};

export default state;

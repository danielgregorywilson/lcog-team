// TODO
interface ReviewNoteInterface {
  employee: unknown
  note: string
}

export interface PerformanceReviewInterface {
  pk?: number
  employee_pk?: number
  employee_name: string
  date_of_review: string
  days_until_review: string
  status: string
  date_of_discussion: string
  evaluation: string
  discussion_took_place: boolean
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
  nextPerformanceReview: {pk: undefined, employee_pk: undefined, employee_name: '', date_of_review: '', days_until_review: '', status: '', date_of_discussion: '', evaluation: '', discussion_took_place: false},
  allPerformanceReviews: [],
  allPerformanceReviewsActionRequired: [],
  allPerformanceReviewsActionNotRequired: [],
  allUpperManagerPerformanceReviewsActionRequired: [],
  allUpperManagerPerformanceReviewsActionNotRequired: [],
  performanceReviewDetails: {},
  allReviewNotes: []
};

export default state;

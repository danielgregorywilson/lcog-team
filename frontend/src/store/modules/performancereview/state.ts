// TODO
interface ReviewNoteInterface {
  employee: unknown
  note: string
}

interface PerformanceReviewInterface {
  employee: unknown
  note: string
}

export interface PerformanceReviewStateInterface {
  allReviewNotes: Array<ReviewNoteInterface>
  allPerformanceReviewsActionRequired: Array<PerformanceReviewInterface>
  allPerformanceReviewsActionNotRequired: Array<PerformanceReviewInterface>
}

const state: PerformanceReviewStateInterface = {
  allReviewNotes: [],
  allPerformanceReviewsActionRequired: [],
  allPerformanceReviewsActionNotRequired: []
};

export default state;

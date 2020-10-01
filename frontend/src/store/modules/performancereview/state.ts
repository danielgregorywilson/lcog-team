// TODO
interface ReviewNoteInterface {
  employee: unknown
  note: string
}

export interface PerformanceReviewStateInterface {
  allReviewNotes: Array<ReviewNoteInterface>
}

const state: PerformanceReviewStateInterface = {
  allReviewNotes: []
};

export default state;

export interface ReviewNote {
  pk: number;
  employee_name: string;
  date: Date;
  note: string;
}

export interface PerformanceReview {
  pk: number;
  employee_name: string;
  date_of_review: Date;
  days_until_review: number;
  status: string;
  date_of_discussion: Date;
  discussion_took_place: boolean;
}

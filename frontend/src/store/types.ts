import { Url } from 'url';

///////////////////////////////////////////////////
// Employee Structure from Django Rest Framework //
///////////////////////////////////////////////////

export interface EmployeeRetrieve {
  url: string;
  pk: number;
  employee_name: string;
  user: Url;
  manager: Url;
  hire_date: Date;
  salary: number;
}

export interface AxiosEmployeeRetrieveManyServerResponse {
  data: {
    results: Array<EmployeeRetrieve>
  }
}

////////////////////////////////////////////////////////////
// PerformanceReview Structure from Django Rest Framework //
////////////////////////////////////////////////////////////

export interface PerformanceReviewRetrieve {
  url: Url;
  pk: number;
  employee_name: string;
  date_of_review: Date;
  days_until_review: number;
  status: string;
  date_of_discussion: Date;
  discussion_took_place: boolean;
}

// TODO: Update
export interface PerformanceReviewCreate {
  url: Url;
  pk: number;
  employee_name: string;
  date_of_review: Date;
  days_until_review: number;
  status: string;
  date_of_discussion: Date;
  discussion_took_place: boolean;
}

// TODO: Update
export interface PerformanceReviewUpdate {
  url: Url;
  pk: number;
  employee_name: string;
  date_of_review: Date;
  days_until_review: number;
  status: string;
  date_of_discussion: Date;
  discussion_took_place: boolean;
}

/////////////////////////////////////////////////////
// ReviewNote Structure from Django Rest Framework //
/////////////////////////////////////////////////////

export interface ReviewNoteRetrieve {
  url: Url;
  pk: number;
  employee_pk: number;
  employee_name: string;
  date: Date;
  note: string;
}

export interface AxiosReviewNoteRetrieveOneServerResponse {
  data: ReviewNoteRetrieve
}

export interface ReviewNoteUpdate {
  employee_pk?: number;
  note?: string;
}

export interface AxiosReviewNoteUpdateServerResponse {
  data: ReviewNoteRetrieve
}

export interface ReviewNoteCreate {
  employee_pk: number;
  note: string;
}

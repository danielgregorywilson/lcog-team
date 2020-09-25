import { AxiosResponse } from 'axios';
import { Url } from 'url';

/////////////////////////////////////////////////////
// Auth Users Structure from Django Rest Framework //
/////////////////////////////////////////////////////

export interface AxiosAuthResponse extends AxiosResponse {
  data: {
    token: string;
  }
}

export interface UserRetrieve {
  url: Url;
  username: string;
  email: string;
  name: string;
  // groups: Array<Group>;
  groups: unknown; // TODO: Set
  is_staff: boolean;
}

export interface AxiosUserRetrieveOneServerResponse {
  data: UserRetrieve
}

// TODO: Complete
// export interface Group {}

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
  employee_pk: number;
  employee_name: string;
  date_of_review: Date;
  days_until_review: number;
  status: string;
  date_of_discussion: Date;
  evaluation: string;
  discussion_took_place: boolean;
}

export interface AxiosPerformanceReviewRetrieveOneServerResponse {
  data: PerformanceReviewRetrieve
}

export interface AxiosPerformanceReviewRetrieveManyServerResponse {
  data: {
    results: Array<PerformanceReviewRetrieve>
  }
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

export interface PerformanceReviewUpdate {
  date_of_discussion?: string;
  evaluation?: string;
}

export interface AxiosPerformanceReviewUpdateServerResponse {
  data: PerformanceReviewRetrieve
}

export interface AxiosPerformanceReviewManagerMarkDiscussedServerResponse {
  data: {
    status: string
  }
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

export interface AxiosReviewNoteRetrieveManyServerResponse {
  data: {
    results: Array<ReviewNoteRetrieve>
  }
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

import { AxiosResponse } from 'axios'
import { Url } from 'url'

/////////////////////////////////////////////////////
// Auth Users Structure from Django Rest Framework //
/////////////////////////////////////////////////////

export interface AxiosAuthResponse extends AxiosResponse {
  data: {
    token: string
  }
}

export interface UserRetrieve {
  url: Url
  username: string
  email: string
  name: string
  // groups: Array<Group>
  groups: unknown // TODO: Set
  is_staff: boolean
  is_manager: boolean
  is_upper_manager: boolean
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
  url: string
  pk: number
  employee_name: string
  employee_pk: number
  user: Url
  manager: Url
  hire_date: Date
  salary: number
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
  url: Url
  pk: number
  employee_pk: number
  employee_name: string
  manager_pk: number
  manager_name: string
  period_start_date: Date
  period_end_date: Date
  effective_date: Date
  employee_division: string
  employee_unit_or_program: string
  employee_job_title: string
  evaluation_type: string
  probationary_evaluation_type: string
  step_increase: string
  top_step_bonus: string

  days_until_review: number

  status: string
  factor_job_knowledge: string
  factor_work_quality: string
  factor_work_quantity: string
  factor_work_habits: string
  factor_analysis: string
  factor_initiative: string
  factor_interpersonal: string
  factor_communication: string
  factor_dependability: string
  factor_professionalism: string
  factor_management: string
  factor_supervision: string
  evaluation_successes: string
  evaluation_opportunities: string
  evaluation_goals_manager: string
  evaluation_comments_employee: string
  description_reviewed_employee: boolean

  all_required_signatures: Array<[string, string, string]>
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
  url: Url
  pk: number
  employee_name: string
  days_until_review: number
  status: string
}

export interface PerformanceReviewUpdate {
  pk: number
  evaluation_type: string
  probationary_evaluation_type: string
  step_increase: string
  top_step_bonus: string
  factor_job_knowledge: string
  factor_work_quality: string
  factor_work_quantity: string
  factor_work_habits: string
  factor_analysis: string
  factor_initiative: string
  factor_interpersonal: string
  factor_communication: string
  factor_dependability: string
  factor_professionalism: string
  factor_management: string
  factor_supervision: string
  evaluation_successes: string
  evaluation_opportunities: string
  evaluation_goals_manager: string
  evaluation_comments_employee: string
  description_reviewed_employee: boolean
}

export interface AxiosPerformanceReviewUpdateServerResponse {
  data: PerformanceReviewRetrieve
}

export interface AxiosPerformanceReviewSignServerResponse {
  data: {
    signatures: Array<[string, string, string]>
  }
}


/////////////////////////////////////////////////////
// Signature Structure from Django Rest Framework //
/////////////////////////////////////////////////////

export interface SignatureCreate {
  review_pk: number
  employee_pk: number
}

export interface SignatureRetrieve {
  url: Url
  pk: number
  review: Url
  employee: Url
  date: Date
}

// export interface AxiosReviewNoteRetrieveOneServerResponse {
//   data: ReviewNoteRetrieve
// }

// export interface AxiosManagerReviewNotesForEmployeeServerResponse {
//   data: Array<ReviewNoteRetrieve>
// }

// export interface AxiosReviewNoteRetrieveManyServerResponse {
//   data: {
//     results: Array<ReviewNoteRetrieve>
//   }
// }

// export interface AxiosReviewNoteUpdateServerResponse {
//   data: ReviewNoteRetrieve
// }


/////////////////////////////////////////////////////
// ReviewNote Structure from Django Rest Framework //
/////////////////////////////////////////////////////

export interface ReviewNoteCreate {
  employee_pk: number
  note: string
}

export interface ReviewNoteRetrieve {
  url: Url
  pk: number
  employee_pk: number
  employee_name: string
  date: Date
  note: string
}

export interface ReviewNoteUpdate {
  employee_pk?: number
  note?: string
}

export interface AxiosReviewNoteRetrieveOneServerResponse {
  data: ReviewNoteRetrieve
}

export interface AxiosManagerReviewNotesForEmployeeServerResponse {
  data: Array<ReviewNoteRetrieve>
}

export interface AxiosReviewNoteRetrieveManyServerResponse {
  data: {
    results: Array<ReviewNoteRetrieve>
  }
}

export interface AxiosReviewNoteUpdateServerResponse {
  data: ReviewNoteRetrieve
}



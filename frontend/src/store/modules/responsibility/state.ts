import { SimpleEmployeeRetrieve } from 'src/store/types';

export interface ResponsibilityInterface {
  pk: number
  name: string
  link?: string
  primary_employee_pk?: number
  primary_employee_name?: string
  secondary_employee_pk?: number
  secondary_employee_name?: string
}

export interface EmployeeResponsibilitiesInterface {
  pk: number
  // name: string
  responsibilities: Array<ResponsibilityInterface>
}

export interface ResponsibilityStateInterface {
  allResponsibilities: { results: Array<ResponsibilityInterface> }
  orphanedResponsibilities: Array<ResponsibilityInterface>
  employeePrimaryResponsibilities: Array<EmployeeResponsibilitiesInterface>
  employeeSecondaryResponsibilities: Array<EmployeeResponsibilitiesInterface>
  simpleEmployeeList: Array<SimpleEmployeeRetrieve>
}

const state: ResponsibilityStateInterface = {
  allResponsibilities: { results: []},
  orphanedResponsibilities: [],
  employeePrimaryResponsibilities: [],
  employeeSecondaryResponsibilities: [],
  simpleEmployeeList: []
};

export default state;

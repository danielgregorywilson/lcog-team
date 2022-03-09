import { ResponsibilityStateInterface } from 'src/store/types';

const state: ResponsibilityStateInterface = {
  allResponsibilities: { results: [] },
  orphanedResponsibilities: [],
  employeePrimaryResponsibilities: [],
  employeeSecondaryResponsibilities: [],
  allTags: { results: [] },
  simpleEmployeeList: [],
  simpleEmployeeDetail: { pk: -1, name: '' }
};

export default state;

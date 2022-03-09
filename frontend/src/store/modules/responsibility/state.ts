import { ResponsibilityStateInterface } from 'src/store/types';

const state: ResponsibilityStateInterface = {
  allResponsibilities: { results: [] },
  orphanedResponsibilities: [],
  employeePrimaryResponsibilities: [],
  employeeSecondaryResponsibilities: [],
  tagWithResponsibilities: [],
  allTags: { results: [] },
  simpleEmployeeList: [],
  simpleEmployeeDetail: { pk: -1, name: '' },
  simpleTagList: []
};

export default state;

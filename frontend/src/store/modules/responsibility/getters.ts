import { GetterTree } from 'vuex';
import { StateInterface } from '../../index';
import { ResponsibilityStateInterface } from '../../types';

const getters: GetterTree<ResponsibilityStateInterface, StateInterface> = {
  allResponsibilities: state => state.allResponsibilities,
  orphanedResponsibilities: state => state.orphanedResponsibilities,
  employeePrimaryResponsibilities: state => state.employeePrimaryResponsibilities,
  employeeSecondaryResponsibilities: state => state.employeeSecondaryResponsibilities,
  allTags: state => state.allTags,
  simpleEmployeeList: state => state.simpleEmployeeList,
  simpleEmployeeDetail: state => state.simpleEmployeeDetail,
  simpleTagList: state => state.simpleTagList,
};

export default getters;

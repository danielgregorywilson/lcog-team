import { GetterTree } from 'vuex';
import { StateInterface } from '../../index';
import { ResponsibilityStateInterface } from '../../types';

const getters: GetterTree<ResponsibilityStateInterface, StateInterface> = {
  allResponsibilities: state => state.allResponsibilities,
  orphanedResponsibilities: state => state.orphanedResponsibilities,
  employeePrimaryResponsibilities: state => state.employeePrimaryResponsibilities,
  employeeSecondaryResponsibilities: state => state.employeeSecondaryResponsibilities,
  simpleEmployeeList: state => state.simpleEmployeeList,
  simpleEmployeeDetail: state => state.simpleEmployeeDetail
};

export default getters;

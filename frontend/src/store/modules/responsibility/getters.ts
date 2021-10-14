import { GetterTree } from 'vuex';
import { StateInterface } from '../../index';
import { ResponsibilityStateInterface } from './state';

const getters: GetterTree<ResponsibilityStateInterface, StateInterface> = {
  allResponsibilities: state => state.allResponsibilities,
  orphanedResponsibilities: state => state.orphanedResponsibilities,
  employeePrimaryResponsibilities: state => state.employeePrimaryResponsibilities,
  employeeSecondaryResponsibilities: state => state.employeeSecondaryResponsibilities
};

export default getters;

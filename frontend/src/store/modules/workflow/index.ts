import { Module } from 'vuex';
import { StateInterface } from '../../index';
import state, { WorkflowStateInterface } from './state';
import actions from './actions';
import getters from './getters';
import mutations from './mutations';

const workflowModule: Module<WorkflowStateInterface, StateInterface> = {
  namespaced: true,
  actions,
  getters,
  mutations,
  state
};

export default workflowModule;

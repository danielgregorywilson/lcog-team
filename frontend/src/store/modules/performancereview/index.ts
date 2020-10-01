import { Module } from 'vuex';
import { StateInterface } from '../../index';
import state, { PerformanceReviewStateInterface } from './state';
import actions from './actions';
import getters from './getters';
import mutations from './mutations';

const performanceReviewModule: Module<PerformanceReviewStateInterface, StateInterface> = {
  namespaced: true,
  actions,
  getters,
  mutations,
  state
};

export default performanceReviewModule;

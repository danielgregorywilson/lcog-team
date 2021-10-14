import { Module } from 'vuex';
import { StateInterface } from '../../index';
import state, { ResponsibilityStateInterface } from './state';
import actions from './actions';
import getters from './getters';
import mutations from './mutations';

const teleworkModule: Module<ResponsibilityStateInterface, StateInterface> = {
  namespaced: true,
  actions,
  getters,
  mutations,
  state
};

export default teleworkModule;

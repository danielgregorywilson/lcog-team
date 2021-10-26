import { Module } from 'vuex';
import { StateInterface } from '../../index';
import state from './state';
import { ResponsibilityStateInterface } from '../../types';
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

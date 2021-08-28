import { Module } from 'vuex';
import { StateInterface } from '../../index';
import state, { SecurityMessageStateInterface } from './state';
import actions from './actions';
import getters from './getters';
import mutations from './mutations';

const securityMessageModule: Module<SecurityMessageStateInterface, StateInterface> = {
  namespaced: true,
  actions,
  getters,
  mutations,
  state
};

export default securityMessageModule;

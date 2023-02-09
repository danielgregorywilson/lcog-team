import { Module } from 'vuex';
import { StateInterface } from '../../index';
import state from './state';
import { PeopleStateInterface } from '../../types';
import actions from './actions';
import getters from './getters';
import mutations from './mutations';

const responsibilityModule: Module<PeopleStateInterface, StateInterface> = {
  namespaced: true,
  actions,
  getters,
  mutations,
  state
};

export default responsibilityModule;

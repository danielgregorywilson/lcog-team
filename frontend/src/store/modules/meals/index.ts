import { Module } from 'vuex';
import { StateInterface } from '../../index';
import state, { MealStateInterface } from './state';
import actions from './actions';
import getters from './getters';
import mutations from './mutations';

const mealsModule: Module<MealStateInterface, StateInterface> = {
  namespaced: true,
  actions,
  getters,
  mutations,
  state
};

export default mealsModule;

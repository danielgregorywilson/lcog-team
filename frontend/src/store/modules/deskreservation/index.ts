import { Module } from 'vuex';
import { StateInterface } from '../../index';
import state from './state';
import { DeskReservationStateInterface } from '../../types';
import actions from './actions';
import getters from './getters';
import mutations from './mutations';

const deskReservationModule: Module<DeskReservationStateInterface, StateInterface> = {
  namespaced: true,
  actions,
  getters,
  mutations,
  state
};

export default deskReservationModule;

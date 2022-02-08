import { GetterTree } from 'vuex';
import { StateInterface } from '../../index';
import { DeskReservationStateInterface } from '../../types';

const getters: GetterTree<DeskReservationStateInterface, StateInterface> = {
  allDesks: state => state.allDesks,
  allDeskReservations: state => state.allDeskReservations
};

export default getters;

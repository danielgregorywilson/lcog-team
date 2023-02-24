import { GetterTree } from 'vuex';
import { StateInterface } from '../../index';
import { MealStateInterface } from './state';

const getters: GetterTree<MealStateInterface, StateInterface> = {
  stops: state => state.stops,
};

export default getters;

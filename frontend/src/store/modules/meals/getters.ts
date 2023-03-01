import { GetterTree } from 'vuex';
import { StateInterface } from '../../index';
import { MealStateInterface } from './state';

const getters: GetterTree<MealStateInterface, StateInterface> = {
  stops: state => state.stops,
  gatewayStops: state => state.stops.results.filter(stop => stop.route === 'Gateway'),
  marcolaStops: state => state.stops.results.filter(stop => stop.route === 'Marcola'),
  MCStops: state => state.stops.results.filter(stop => stop.route === 'MC'),
  PUStops: state => state.stops.results.filter(stop => stop.route === 'PU'),
  shortStops: state => state.stops.results.filter(stop => stop.route === 'Short'),
  longStops: state => state.stops.results.filter(stop => stop.route === 'Long'),
  northStops: state => state.stops.results.filter(stop => stop.route === 'North'),
  willStops: state => state.stops.results.filter(stop => stop.route === 'Will')
};

export default getters;

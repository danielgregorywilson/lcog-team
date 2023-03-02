import { GetterTree } from 'vuex';
import { StateInterface } from '../../index';
import { MealStateInterface } from './state';

const getters: GetterTree<MealStateInterface, StateInterface> = {
  stops: state => state.stops,
  gatewayStops: state => state.stops.results.filter(stop => stop.route === 'Gateway'),
  marcolaStops: state => state.stops.results.filter(stop => stop.route === 'Marcola'),
  MCStops: state => state.stops.results.filter(stop => stop.route === 'MC'),
  shortStops: state => state.stops.results.filter(stop => stop.route === 'Short'),
  longStops: state => state.stops.results.filter(stop => stop.route === 'Long'),
  northStops: state => state.stops.results.filter(stop => stop.route === 'North'),
  willStops: state => state.stops.results.filter(stop => stop.route === 'Will'),
  hotPUStops: state => state.stops.results.filter(stop => stop.route === 'PU' && stop.meal_type === 'hot'),
  tu1Stops: state => state.stops.results.filter(stop => stop.route === 'Tu 1'),
  tu2Stops: state => state.stops.results.filter(stop => stop.route === 'Tu 2'),
  tu3Stops: state => state.stops.results.filter(stop => stop.route === 'Tu 3'),
  thur1Stops: state => state.stops.results.filter(stop => stop.route === 'Thur 1'),
  thur2Stops: state => state.stops.results.filter(stop => stop.route === 'Thur 2'),
  thur3Stops: state => state.stops.results.filter(stop => stop.route === 'Thur 3'),
  coldPUStops: state => state.stops.results.filter(stop => stop.route === 'PU' && stop.meal_type === 'cold'),
};

export default getters;

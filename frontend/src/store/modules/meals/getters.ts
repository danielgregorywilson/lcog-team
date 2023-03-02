import { GetterTree } from 'vuex';
import { StateInterface } from '../../index';
import { MealStateInterface } from './state';

const getters: GetterTree<MealStateInterface, StateInterface> = {
  stops: state => state.stops,

  // Current Stops
  gatewayStops: state => state.stops.results.filter(stop => stop.route === 'Gateway' && stop.waitlist === false),
  marcolaStops: state => state.stops.results.filter(stop => stop.route === 'Marcola' && stop.waitlist === false),
  MCStops: state => state.stops.results.filter(stop => stop.route === 'MC' && stop.waitlist === false),
  shortStops: state => state.stops.results.filter(stop => stop.route === 'Short' && stop.waitlist === false),
  longStops: state => state.stops.results.filter(stop => stop.route === 'Long' && stop.waitlist === false),
  northStops: state => state.stops.results.filter(stop => stop.route === 'North' && stop.waitlist === false),
  willStops: state => state.stops.results.filter(stop => stop.route === 'Will' && stop.waitlist === false),
  hotPUStops: state => state.stops.results.filter(stop => stop.route === 'PU' && stop.meal_type === 'hot' && stop.waitlist === false),
  tu1Stops: state => state.stops.results.filter(stop => stop.route === 'Tu 1' && stop.waitlist === false),
  tu2Stops: state => state.stops.results.filter(stop => stop.route === 'Tu 2' && stop.waitlist === false),
  tu3Stops: state => state.stops.results.filter(stop => stop.route === 'Tu 3' && stop.waitlist === false),
  thur1Stops: state => state.stops.results.filter(stop => stop.route === 'Thur 1' && stop.waitlist === false),
  thur2Stops: state => state.stops.results.filter(stop => stop.route === 'Thur 2' && stop.waitlist === false),
  thur3Stops: state => state.stops.results.filter(stop => stop.route === 'Thur 3' && stop.waitlist === false),
  coldPUStops: state => state.stops.results.filter(stop => stop.route === 'PU' && stop.meal_type === 'cold' && stop.waitlist === false),

  // Waitlist Stops
  gatewayWaitlistStops: state => state.stops.results.filter(stop => stop.route === 'Gateway' && stop.waitlist === true),
  marcolaWaitlistStops: state => state.stops.results.filter(stop => stop.route === 'Marcola' && stop.waitlist === true),
  MCWaitlistStops: state => state.stops.results.filter(stop => stop.route === 'MC' && stop.waitlist === true),
  shortWaitlistStops: state => state.stops.results.filter(stop => stop.route === 'Short' && stop.waitlist === true),
  longWaitlistStops: state => state.stops.results.filter(stop => stop.route === 'Long' && stop.waitlist === true),
  northWaitlistStops: state => state.stops.results.filter(stop => stop.route === 'North' && stop.waitlist === true),
  willWaitlistStops: state => state.stops.results.filter(stop => stop.route === 'Will' && stop.waitlist === true),
  hotPUWaitlistStops: state => state.stops.results.filter(stop => stop.route === 'PU' && stop.meal_type === 'hot' && stop.waitlist === true),
  tu1WaitlistStops: state => state.stops.results.filter(stop => stop.route === 'Tu 1' && stop.waitlist === true),
  tu2WaitlistStops: state => state.stops.results.filter(stop => stop.route === 'Tu 2' && stop.waitlist === true),
  tu3WaitlistStops: state => state.stops.results.filter(stop => stop.route === 'Tu 3' && stop.waitlist === true),
  thur1WaitlistStops: state => state.stops.results.filter(stop => stop.route === 'Thur 1' && stop.waitlist === true),
  thur2WaitlistStops: state => state.stops.results.filter(stop => stop.route === 'Thur 2' && stop.waitlist === true),
  thur3WaitlistStops: state => state.stops.results.filter(stop => stop.route === 'Thur 3' && stop.waitlist === true),
  coldPUWaitlistStops: state => state.stops.results.filter(stop => stop.route === 'PU' && stop.meal_type === 'cold' && stop.waitlist === true),
};

export default getters;

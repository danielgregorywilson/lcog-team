import { GetterTree } from 'vuex';
import { StateInterface } from '../../index';
import { TimeOffRequestStateInterface } from './state';

const getters: GetterTree<TimeOffRequestStateInterface, StateInterface> = {
  myTimeOffRequests: state => state.myTimeOffRequests,
  teamTimeOffRequests: state => state.teamTimeOffRequests,
  managedTimeOffRequests: state => state.managedTimeOffRequests
};

export default getters;

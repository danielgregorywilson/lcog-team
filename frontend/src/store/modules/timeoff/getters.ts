import { GetterTree } from 'vuex';
import { StateInterface } from '../../index';
import { TimeOffRequestStateInterface } from './state';

const getters: GetterTree<TimeOffRequestStateInterface, StateInterface> = {
  myTimeOffRequests: state => state.myTimeOffRequests
};

export default getters;

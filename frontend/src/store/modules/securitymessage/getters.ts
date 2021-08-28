import { GetterTree } from 'vuex';
import { StateInterface } from '../../index';
import { SecurityMessageStateInterface } from './state';

const getters: GetterTree<SecurityMessageStateInterface, StateInterface> = {
  viewedSecurityMessages: state => state.viewedSecurityMessages,
  viewedLatestSecurityMessage: state => state.viewedLatestSecurityMessage,
};

export default getters;

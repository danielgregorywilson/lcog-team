import { GetterTree } from 'vuex';
import { StateInterface } from '../../index';
import { TeleworkStateInterface } from './state';

const getters: GetterTree<TeleworkStateInterface, StateInterface> = {
  teleworkApplication: state => state.teleworkApplication,
  allTeleworkApplicationsSignatureRequired: state => state.allTeleworkApplicationsSignatureRequired,
  allTeleworkApplicationsSignatureNotRequired: state => state.allTeleworkApplicationsSignatureNotRequired,
};

export default getters;

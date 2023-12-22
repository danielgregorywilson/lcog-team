import { ActionTree } from 'vuex';
import { StateInterface } from '../../index';
import { TeleworkStateInterface } from './state';
import axios from 'axios';
import {
  AxiosTeleworkApplicationRetrieveOneServerResponse,
  TeleworkSignatureCreate
} from 'src/store/types';

function getApiUrl(): string {
  if (process.env.API_URL) {
    return process.env.API_URL
  } else {
    return ''
  }
}

const actions: ActionTree<TeleworkStateInterface, StateInterface> = {
  getTeleworkApplication: ({ commit }, data: {applicationPk: number}) => {
    return new Promise((resolve, reject) => {
      axios({ url: `${ getApiUrl() }api/v1/teleworkapplication/${ data.applicationPk }` })
        .then(resp => {
          commit('setTeleworkApplication', resp);
          resolve(resp);
        })
        .catch(e => {
          console.error('Error getting telework application:', e)
          reject(e)
        });
    })
  },
  getOrCreateTeleworkApplicationByEmployee: ({ commit }, data: {employeePk: number}): Promise<AxiosTeleworkApplicationRetrieveOneServerResponse> => {
    return new Promise((resolve, reject) => {
      axios({ url: `${ getApiUrl() }api/v1/teleworkapplication/${ data.employeePk }?by_employee=true` })
        .then(resp => {
          commit('setTeleworkApplication', resp);
          resolve(resp);
        })
        .catch(e => {
          console.error('Error getting or creating telework application:', e)
          reject(e)
        });
    })
  },
  createSignature: ({}, signature: TeleworkSignatureCreate) => {
    axios({ url: `${ process.env.API_URL }api/v1/teleworksignature`, data: signature, method: 'POST' }) // eslint-disable-line @typescript-eslint/restrict-template-expressions
      .catch(e => {
        console.error('Error creating a signature:', e)
      });
  },
  getAllTeleworkApplicationsSignatureRequired: ({ commit }) => {
    axios({ url: `${ process.env.API_URL }api/v1/teleworkapplication?signature=True` }) // eslint-disable-line @typescript-eslint/restrict-template-expressions
      .then(resp => {
        commit('setAllTeleworkApplicationsSignatureRequired', resp);
      })
      .catch(e => {
        console.error('Error setting all telework applications signature required:', e)
      });
  },
  getAllTeleworkApplicationsSignatureNotRequired: ({ commit }) => {
    axios({ url: `${ process.env.API_URL }api/v1/teleworkapplication?signature=False` }) // eslint-disable-line @typescript-eslint/restrict-template-expressions
      .then(resp => {
        commit('setAllTeleworkApplicationsSignatureNotRequired', resp);
      })
      .catch(e => {
        console.error('Error setting all telework applications signature not required:', e)
      });
  },
  authLogout: ({commit}) => {
    return new Promise((resolve) => {
      commit('authLogout')
      resolve('Successfully triggered logout')
    })
  }
};

export default actions;

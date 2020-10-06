import { ActionTree } from 'vuex';
import { StateInterface } from '../../index';
import { UserStateInterface } from './state';
import axios from 'axios';

const actions: ActionTree<UserStateInterface, StateInterface> = {
  userRequest: ({ commit, dispatch }) => {
    commit('userRequest');
    axios({ url: `${ process.env.API_URL }api/v1/current-user/` }) // eslint-disable-line @typescript-eslint/restrict-template-expressions
      .then((resp: {data: {pk: number}}) => {
        commit('userSuccess', resp);
        dispatch('performanceReviewModule/getNextPerformanceReview', {pk: resp.data.pk}, { root: true })
            .catch(err => console.log(err))
      })
      .catch(() => {
        commit('userError');
        // if resp is unauthorized, logout, to
        dispatch('authLogout')
          .catch(err => console.log(err))
      });
  }
};

export default actions;

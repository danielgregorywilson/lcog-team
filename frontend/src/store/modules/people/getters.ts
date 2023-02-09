import { GetterTree } from 'vuex';
import { StateInterface } from '../../index';
import { PeopleStateInterface } from '../../types';

const getters: GetterTree<PeopleStateInterface, StateInterface> = {
  simpleEmployeeList: state => state.simpleEmployeeList,
  simpleEmployeeDetail: state => state.simpleEmployeeDetail,
  unitList: state => state.unitList
};

export default getters;

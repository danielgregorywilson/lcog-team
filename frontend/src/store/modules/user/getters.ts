import { GetterTree } from 'vuex';
import { StateInterface } from '../../index';
import { UserStateInterface } from './state';

const getters: GetterTree<UserStateInterface, StateInterface> = {
  getEmployeeProfile: state => state.profile,
  isProfileLoaded: state => !!state.profile.employee_pk,
  isManager: state => state.profile.is_manager,
  hasWorkflowRoles: state => !!state.profile.workflow_roles.length,
  canViewMOWRoutes: state => state.profile.can_view_mow_routes,
  canManageMOWStops: state => state.profile.can_manage_mow_stops
};

export default getters;

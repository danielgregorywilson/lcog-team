import { Stop } from '../../types'

export interface MealStateInterface {
  stops: { results: Array<Stop> }
}

export const blankStop: Stop = {
  first_name: '', last_name: '', address: '', city: '', zip_code: -1,
  latitude: -1, longitude: -1, meal_type: 'hot', waitlist: false, phone: '',
  phone_notes: '', notes: '', route: '', created_at: new Date(),
  updated_at: new Date()
}

const state: MealStateInterface = {
  stops: {results: [] }
};

export default state;

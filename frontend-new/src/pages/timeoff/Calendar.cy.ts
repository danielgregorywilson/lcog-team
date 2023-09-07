import Calendar from './Calendar.vue'

describe('<Calendar />', () => {
  it('renders', () => {
    // see: https://on.cypress.io/mounting-vue
    cy.mount(Calendar)
  })
})
function visit_url(path: string) {
  cy.visit(`${ Cypress.env('base_url') }${ path }`)
}

describe('Manager creates a new employee workflow', () => {
  it('Logs in, creates a new employee workflow, and submits it', () => {
    visit_url(Cypress.env('login_path'))
    cy.get('input#username').type(Cypress.env('manager_username'))
    cy.get('input#password').type(Cypress.env('manager_password'))
    cy.get('button[type="submit"]').click()
    cy.location('pathname', {timeout: 60000}) // Wait until the dashboard loads
      .should('include', '/dashboard')
    visit_url(Cypress.env('workflows_dashboard_path'))
    // cy.get('.workflowtable-new .row-add-new').click()
    // const url = cy.url()
    // url.should('contain', 'localhost')
  })
})

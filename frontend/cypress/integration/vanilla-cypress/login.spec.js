describe('Login Page', () => {
  it('successfully loads', () => {
    cy.visit('/auth/login')
  })
  it('accepts credentials', () => {
    cy.get('#username')
      .type(Cypress.env('users').manager.username)
      .should('have.value', Cypress.env('users').manager.username)
    cy.get('#password')
      .type(Cypress.env('users').manager.pw, {log: false})
      .should('have.value', Cypress.env('users').manager.pw)
  })
  it('logs in successfully', () => {
    cy.contains('Login').click()
    cy.url().should('include', '/dashboard')
  })

  it('can logout', () => {
    cy.get('#menu-button').click()
    cy.contains('Log Out').click()
    cy.url().should('include', '/dashboard')
  })
})
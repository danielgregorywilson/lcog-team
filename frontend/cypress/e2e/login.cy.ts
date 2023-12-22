import { visitUrl } from '../support/helpers'

describe('template spec', () => {
  it('successfully loads', () => {
    visitUrl('/auth/login')
  })
  it('accepts credentials', () => {
    cy.get('#username')
      .type(Cypress.env('users').gsmanager.username)
      .should('have.value', Cypress.env('users').manager.username)
    cy.get('#password')
      .type(Cypress.env('users').gsmanager.pw, {log: false})
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
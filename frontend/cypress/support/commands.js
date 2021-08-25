// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add("login", (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add("drag", { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add("dismiss", { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite("visit", (originalFn, url, options) => { ... })

Cypress.Commands.add('loginEmployeeWithUI', () => {
  cy.visit('/auth/login')
  cy.get('#username')
    .type(Cypress.env('users').employee.username)
  cy.get('#password')
    .type(Cypress.env('users').employee.pw, {log: false})
  cy.contains('Login').click()
});

Cypress.Commands.add('loginManagerWithUI', () => {
  cy.visit('/auth/login')
  cy.get('#username')
    .type(Cypress.env('users').manager.username)
  cy.get('#password')
    .type(Cypress.env('users').manager.pw, {log: false})
  cy.contains('Login').click()
});

Cypress.Commands.add('loginEmployee', () => {
  const username = Cypress.env('users').employee.username
  const password = Cypress.env('users').employee.pw

  cy.request('POST', 'http://localhost:8000/api/api-token-auth-password/', {username, password})
    .its('body.token')
    .should('exist')
    .then(token =>
        localStorage.setItem('user-token', `${token}`)
    );
    // TODO: Also need to set Axios default header for subsequent requests?

    // Verify user token was set
    // expect(localStorage.getItem('user-token')).to.eq('dbbe99f7301bf3134d2259e1919d82148a68676d')
});
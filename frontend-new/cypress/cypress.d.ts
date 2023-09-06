/// <reference types="cypress" />

// Type definitions for Cypress

// Not currently needed because I don't have any custom commands
declare namespace Cypress {
  interface Chainable<Subject = any> {
    loginSuperuser(): Chainable<any>;
  }
}

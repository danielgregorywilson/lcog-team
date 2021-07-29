describe('Login Page', () => {
  it('successfully loads', () => {
    cy.visit('/auth/login')
  })
  it('accepts credentials', () => {
    cy.get('#username')
      .type('dwilson')
      .should('have.value', 'dwilson')
    cy.get('#password')
      .type('fank9crax.SEAP0scuh')
      .should('have.value', 'fank9crax.SEAP0scuh')
  })
  it('logs in successfully', () => {
    cy.contains('Login').click()
    cy.url().should('include', '/dashboard')
  })
})
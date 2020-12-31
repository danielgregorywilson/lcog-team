describe('Employee Basic Workflow', () => {
  beforeEach(() => {
    // TODO: Do not log in using the UI
    cy.visit('/')
    cy.get('#username')
      .type('dwilson')
    cy.get('#password')
      .type('fank9crax.SEAP0scuh')
    cy.contains('Login').click()
  })
  
  // // TODO: Should be able to login and set token without using the UI: https://stackoverflow.com/questions/59008563/cypress-re-use-auth-token-across-multiple-api-tests
  // it('logs in programmatically without using the UI', function () {
  //   const username = "dwilson"
  //   const password = "fank9crax.SEAP0scuh"
    
  //   // programmatically log us in without needing the UI
  //   cy.request('POST', 'http://lcog-hr:8000/api/api-token-auth/', {
  //     username,
  //     password
  //   })

  //   // now that we're logged in, we can visit
  //   // any kind of restricted route!
  //   cy.visit('/')

  //   // Verify user token was set
  //   // expect(localStorage.getItem('user-token')).to.eq('dbbe99f7301bf3134d2259e1919d82148a68676d')

  //   // UI should reflect this user being logged in
  //   cy.get('h1').should('contain', 'jane.lane')
  // })


  it('can navigate around', () => {
    cy.get('#menu-button').click()
    cy.contains('Time off Requests').click()
    cy.url().should('include', '/timeoff')
    cy.get('#menu-button').click()
    cy.contains('Dashboard').click()
    cy.url().should('include', '/dashboard')
  })

  it('can view evaluation and add comments', () => {
    cy.contains('View and Sign Evaluation').click()
    cy.url().should('include', '/pr/')
    const employeeComments = Math.random().toString(36).replace(/[^a-z]+/g, '').substr(0, 10)
    cy.get('.evaluation-comments-employee')
      .clear()  
      .type(employeeComments)
      .should('have.value', employeeComments)
    cy.get('#save-comments-employee').click()

    cy.get('#menu-button').click()
    cy.contains('Dashboard').click()
    cy.contains('View and Sign Evaluation').click()
    cy.get('.evaluation-comments-employee')
      .should('have.value', employeeComments)
  })

  it('can logout', () => {
    cy.get('#menu-button').click()
    cy.contains('Log Out').click()
    cy.url().should('include', '/auth/login')
  })
})
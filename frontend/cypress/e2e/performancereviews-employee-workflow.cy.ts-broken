describe('template spec', () => {
  beforeEach(() => {
    // TODO: Do not log in using the UI
    cy.loginEmployeeWithUI()
  })

  it('can navigate around', () => {
    // cy.eyesOpen({
    //   appName: 'LCOG Team App',
    //   testName: 'Employee navigation',
    // })
    // cy.eyesCheckWindow({
    //   tag: "Dashboard",
    //   target: 'window',
    //   fully: true
    // })
    // cy.eyesClose()
    // cy.get('#menu-button').click()
    // cy.contains('Time off Requests').click()
    // cy.url().should('include', '/timeoff')
    // cy.get('#menu-button').click()
    cy.contains('LCOG Team App').click()
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

    // cy.eyesOpen({
    //   appName: 'LCOG Team App',
    //   testName: 'Employee PR detail',
    // })
    // cy.eyesCheckWindow({
    //   tag: "PR Detail",
    //   target: 'window',
    //   fully: true
    // })
    // cy.eyesClose()

    cy.get('#menu-button').click()
    cy.contains('Dashboard').click()
    cy.contains('View and Sign Evaluation').click()
    cy.get('.evaluation-comments-employee')
      .should('have.value', employeeComments)
  })
})
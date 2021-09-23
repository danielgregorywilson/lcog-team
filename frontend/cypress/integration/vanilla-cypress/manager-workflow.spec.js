describe('Manager Basic Workflow', () => {
  beforeEach(() => {
    // TODO: Do not log in using the UI
    cy.loginManagerWithUI()
  })

  it('can navigate around', () => {
    cy.get('#menu-button').click()
    cy.contains('Performance Reviews').click()
    cy.url().should('include', '/reviews')
    cy.get('#menu-button').click()
    // cy.contains('Time off Requests').click()
    // cy.url().should('include', '/timeoff')
    // cy.get('#menu-button').click()
    cy.contains('Dashboard').click()
    cy.url().should('include', '/dashboard')
  })

  it('can add, edit, and delete a note', () => {
    // Remember how many notes there were to start
    cy.get('.q-table__bottom-item').then($elements => {cy.wrap($elements[2])}).invoke('text').then((text) => {
      const parts = text.split(' ')
      cy.wrap(parts[parts.length - 1]).as('numNotes')
    })
    const note = 'A note'
    const updatedNote = 'An updated note'
    
    // Create
    cy.contains('Add a note').click()
    cy.url().should('include', '/note/new')
    cy.get('#review-note-create-button').should('be.disabled')
    cy.contains('Employee').click()
    cy.contains(Cypress.env('users').employee.name).click()
    cy.get('#review-note-create-button').should('be.disabled')
    cy.get('.review-note')
      .type(note)
      .should('have.value', note)
    cy.get('#review-note-create-button').should('be.enabled')
    cy.get('#review-note-create-button').click()
    cy.url().should('include', '/dashboard')
    // There should now be one extra note
    cy.wait(500)
    cy.get('.q-table__bottom-item').then($elements => {cy.wrap($elements[2])}).invoke('text').then((text) => {
      const parts = text.split(' ')
      cy.get('@numNotes').then(numNotes => {
        expect(parseInt(numNotes, 10)).to.equal(parts[parts.length - 1] - 1)
      })
    })
    
    // Update
    cy.contains('Date').click().click()
    cy.get('.edit-note:first').click()
    cy.get('#review-note-update-button').should('be.disabled')
    cy.get('.review-note').should('have.value', note)
    cy.get('.review-note')
      .clear()  
      .type(updatedNote)  
    cy.get('.review-note')
      .should('have.value', updatedNote)
    cy.get('#review-note-update-button').should('be.enabled')
    cy.get('#review-note-update-button').click()
    
    // Delete
    cy.visit('/')
    // There should still be one extra note
    cy.wait(500)
    cy.get('.q-table__bottom-item').then($elements => {cy.wrap($elements[2])}).invoke('text').then((text) => {
      const parts = text.split(' ')
      cy.get('@numNotes').then(numNotes => {
        expect(parseInt(numNotes, 10)).to.equal(parts[parts.length - 1] - 1)
      })
    })
    cy.contains('Date').click().click()
    cy.get('.delete-note:first').click()
    cy.contains('Yes, delete it').click()
    cy.wait(500)
    // There should now be the original number of notes
    cy.get('.q-table__bottom-item').then($elements => {cy.wrap($elements[2])}).invoke('text').then((text) => {
      const parts = text.split(' ')
      cy.get('@numNotes').then(numNotes => {
        expect(numNotes).to.equal(parts[parts.length - 1])
      })
    })
  })

  it('can view performance review and make a change', () => {
    // Make a change
    cy.contains('Reviews for your Direct Reports').parent().parent()
      .contains(Cypress.env('users').employee.name).parent().parent().parent()
      .find('button.edit-button').click()
    cy.url().should('include', '/pr/')
    const employeeSuccesses = Math.random().toString(36).replace(/[^a-z]+/g, '').substr(0, 30)
    cy.get('.evaluation-successes')
      .clear()  
      .type(employeeSuccesses)
      .should('have.value', employeeSuccesses)
    cy.get('#update-button').click()

    // cy.eyesOpen({
    //   appName: 'LCOG Team App',
    //   testName: 'Manager PR detail',
    // })
    // cy.eyesCheckWindow({
    //   tag: "PR Detail",
    //   target: 'window',
    //   fully: true
    // })
    // cy.eyesClose()

    // Verify changes were saved
    cy.get('#menu-button').click()
    cy.contains('Dashboard').click()
    cy.contains('Reviews for your Direct Reports').parent().parent()
      .contains(Cypress.env('users').employee.name).parent().parent().parent()
      .find('button.edit-button').click()
    cy.get('.evaluation-successes')
      .should('have.value', employeeSuccesses)
  })

})
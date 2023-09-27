import { loginSuperuser, loginUser, visitUrl } from '../support/helpers'

// Cypress clears localstorage between tests, so use this to store data
const LOCAL_STORAGE_MEMORY: { [key: string]: string } = {}

describe('New employee workflow check assignments', () => {

  it('Submitter logs in, creates a new employee workflow, and submits it', () => {
    // Create a new employee workflow
    loginUser(Cypress.env('users').manager).then(() => {
      visitUrl(Cypress.env('workflows_dashboard_path'))
      cy.get('.workflowtable-new .row-add-new').click()
      cy.wait(500) // Wait for the new transition form to load
      cy.url().then((url) => {
        const match = url.match(/wf\/(\d+)\/transition/)
        const pk = match ? match[1] : null
        if (pk) {
          LOCAL_STORAGE_MEMORY['workflowPK'] = pk
        }
        cy.log(`Created workflow pk: ${ pk }`)
        // Enter data into the form
        cy.get('input[name="first-name"]').type('Dustin')
        cy.get('input[name="last-name"]').type('Albrecht')
        // TODO: Try cypress-real-events to focus the email field
        cy.get('input[name="email"]').focus()
        const titleInput = cy.get('select[name="title"]').siblings('input')
        titleInput.type('Case')
        cy.wait(500) // Wait for the title to be selected
        titleInput.type('{downArrow}{enter}')
        const managerInput = cy.get('select[name="manager"]').siblings('input')
        managerInput.type('Hiring M')
        cy.wait(500) // Wait for the title to be selected
        managerInput.type('{downArrow}{enter}')
        // Save the form
        cy.get('button[name="save-button"]').click()
        // Cannot reassign
        cy.get('button[name="reassign-button"]').should('have.attr', 'disabled')
        cy.get('button[name="reassign-button"]').contains('Status: Not submitted')
        // Submit the form
        cy.get('button[name="send-sds-button"]').click()
        cy.get('button[name="send-sds-dialog-button"]').click()
        cy.get('button[name="reassign-button"]').contains('Assigned to: Hiring Lead')
      })
    })
  })

  it ('SDS Hiring Lead sends to fiscal', () => {
    const pk = LOCAL_STORAGE_MEMORY['workflowPK']
    loginUser(Cypress.env('users').sdshiringlead).then(() => {
      visitUrl(`/wf/${pk}/transition`)
      // Can reassign
      const reassignButton = cy.get('button[name="reassign-button"]')
      reassignButton.should('not.have.attr', 'disabled')
      reassignButton.contains('Assigned to: Hiring Lead')
      // Submit the form
      cy.get('button[name="send-fiscal-button"]').click()
      cy.get('button[name="send-fiscal-dialog-button"]').click()
      cy.get('button[name="reassign-button"]').contains('Assigned to: Fiscal')
    })
  })

  it('Fiscal reassigns back to SDS Hiring Lead', () => {
    const pk = LOCAL_STORAGE_MEMORY['workflowPK']
    loginUser(Cypress.env('users').fiscalemployee).then(() => {
      visitUrl(`/wf/${pk}/transition`)
      // Can reassign
      const reassignButton = cy.get('button[name="reassign-button"]')
      reassignButton.should('not.have.attr', 'disabled')
      reassignButton.contains('Assigned to: Fiscal')
      // Reassign to SDS Hiring Lead
      reassignButton.click()
      cy.get('button[name="reassign-dialog-assignee-dropdown"]').click()
      cy.get('.q-menu > .q-list > .q-item').eq(1).click()
      cy.get('textarea[name="reassign-extra-message"]').type('Reassigning to SDS Hiring Lead')
      cy.get('button[name="reassign-dialog-button"]').click()
      // Now cannot reassign
      cy.get('button[name="reassign-button"]').should('have.attr', 'disabled')
      cy.get('button[name="reassign-button"]').contains('Assigned to: Hiring Lead')
    })
  })

  it ('SDS Hiring Lead sends to fiscal a second time', () => {
    const pk = LOCAL_STORAGE_MEMORY['workflowPK']
    loginUser(Cypress.env('users').sdshiringlead).then(() => {
      visitUrl(`/wf/${pk}/transition`)
      // Can reassign
      const reassignButton = cy.get('button[name="reassign-button"]')
      reassignButton.should('not.have.attr', 'disabled')
      reassignButton.contains('Assigned to: Hiring Lead')
      // Submit the form
      cy.get('button[name="send-fiscal-button"]').click()
      cy.get('button[name="send-fiscal-dialog-button"]').click()
      cy.get('button[name="reassign-button"]').contains('Assigned to: Fiscal')
    })
  })

  it('Fiscal sends to HR', () => {
    const pk = LOCAL_STORAGE_MEMORY['workflowPK']
    loginUser(Cypress.env('users').fiscalemployee).then(() => {
      visitUrl(`/wf/${pk}/transition`)
      // Can reassign
      const reassignButton = cy.get('button[name="reassign-button"]')
      reassignButton.should('not.have.attr', 'disabled')
      reassignButton.contains('Assigned to: Fiscal')
      // Submit the form
      cy.get('button[name="send-hr-button"]').click()
      cy.get('button[name="send-hr-dialog-button"]').click()
      cy.get('button[name="reassign-button"]').contains('Assigned to: HR')
    })
  })

  it('HR sends to STN', () => {
    const pk = LOCAL_STORAGE_MEMORY['workflowPK']
    loginUser(Cypress.env('users').hremployee).then(() => {
      visitUrl(`/wf/${pk}/transition`)
      // Can reassign
      const reassignButton = cy.get('button[name="reassign-button"]')
      reassignButton.should('not.have.attr', 'disabled')
      reassignButton.contains('Assigned to: HR')
      // Submit the form
      cy.get('button[name="send-stn-button"]').click()
      cy.get('button[name="send-stn-dialog-button"]').click()
      cy.get('button[name="reassign-button"]').contains('Status: Complete')
    })
  })

  it('Deletes the workflow', () => {
    const pk = LOCAL_STORAGE_MEMORY['workflowPK']
    loginSuperuser().then(() => {
      const token = localStorage.getItem('user-token')
      const url = `${ Cypress.env('api_url') }/api/v1/workflowinstance/${ pk }`
      if (pk) {
        cy.request({
          method: 'DELETE',
          url,
          headers: {
            Authorization: `Token ${ token }`,
          },
        }).then(() => {
          cy.log(`Deleted workflow instance pk: ${ pk }`)
        })
      }
    })
  })
})

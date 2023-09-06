import { loginSuperuser, loginUser, visitUrl } from '../support/helpers'

// Cypress clears localstorage between tests, so use this to store data
const LOCAL_STORAGE_MEMORY: { [key: string]: string } = {}

describe('New employee workflow', () => {

  // it('Manager logs in, creates a new employee workflow, and submits it', () => {
  //   // Create a new employee workflow
  //   loginUser(Cypress.env('users').manager).then(() => {
  //     visitUrl(Cypress.env('workflows_dashboard_path'))
  //     cy.get('.workflowtable-new .row-add-new').click()
  //     cy.wait(1000) // Wait for the new transition form to load
  //     cy.url().then((url) => {
  //       const match = url.match(/wf\/(\d+)\/transition/)
  //       const pk = match ? match[1] : null
  //       if (pk) {
  //         LOCAL_STORAGE_MEMORY['workflowPK'] = pk
  //       }
  //       cy.log(`Created workflow pk: ${ pk }`)

  //       // Enter data into the form
  //       cy.get('input[name="first-name"]').type('Xavier')
  //       cy.get('input[name="last-name"]').type('Xanthopoulos')

  //       // TODO: Try cypress-real-events to focus the email field
  //       cy.get('input[name="email"]').focus()

  //       const titleInput = cy.get('select[name="title"]').siblings('input')
  //       titleInput.type('Case')
  //       cy.wait(1000) // Wait for the title to be selected
  //       titleInput.type('{downArrow}{enter}')

  //       const managerInput = cy.get('select[name="manager"]').siblings('input')
  //       managerInput.type('Daniel Wil')
  //       cy.wait(1000) // Wait for the title to be selected
  //       managerInput.type('{downArrow}{enter}')

  //       // Save the form
  //       cy.get('button[name="save-button"]').click()
  //     })
  //   })
  // })

  it('Another manager can view the workflow but not edit certain fields', () => {
    const pk = LOCAL_STORAGE_MEMORY['workflowPK']
    loginUser(Cypress.env('users').manager2).then(() => {
      visitUrl(`/wf/${pk}/transition`)
      const managerInput = cy.get('select[name="manager"]').siblings('input')
      managerInput.should('be.disabled')
    })
  })

  it('Deletes the workflow', () => {
    const pk = LOCAL_STORAGE_MEMORY['workflowPK']
    loginSuperuser().then(() => {
      const token = localStorage.getItem('user-token')
      if (pk) {
        cy.request({
          method: 'DELETE',
          url: `http://localhost:8000/api/v1/workflowinstance/${ pk }`,
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

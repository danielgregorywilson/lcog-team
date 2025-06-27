import { loginSuperuser, loginUser, visitUrl } from '../support/helpers'

// Cypress clears localstorage between tests, so use this to store data
const LOCAL_STORAGE_MEMORY: { [key: string]: string } = {}

describe('GS employee performance review process', () => {

  it('Creates a review', () => {
    loginSuperuser().then(() => {
      const token = localStorage.getItem('user-token')
      const url = `${ Cypress.env('api_url') }/api/v1/review`
      cy.request({
        method: 'POST',
        url,
        headers: {
          Authorization: `Token ${ token }`,
        },
        body: {
          employee: Cypress.env('users').employee.pk,
          manager: Cypress.env('users').gsmanager.pk,
          period_start_date: '2024-06-30',
          period_end_date: '2025-06-30',
          effective_date: '2024-07-01',
        },
      }).then((resp) => {
        const pk = resp.body.pk
        LOCAL_STORAGE_MEMORY['reviewPK'] = pk
        cy.log(`Created review pk: ${ pk }`)
      })
    })
  })

  it('Manager logs in and copies the link', () => {
    // Create a new employee workflow
    loginUser(Cypress.env('users').gsmanager).then(() => {
      visitUrl(Cypress.env('reviews_dashboard_path'))
      cy.get('.feedback-link').first().click()
      cy.window().then((win) => {
        win.navigator.clipboard.readText().then((text) => {
          const link = `${ Cypress.env('base_url') }/note/new?employee=${Cypress.env('users').employee.pk}`
          expect(text).to.eq(link);
        });
      });
    })
  })

  it('Colleague uses link to submit feedback', () => {
    // loginUser(Cypress.env('users').employee).then(() => {
    //   visitUrl(Cypress.env('reviews_dashboard_path'))
    //   cy.get('.feedback-link').first().click()
    //   cy.window().then((win) => {
    //     win.navigator.clipboard.readText().then((text) => {
    //       const link = `${ Cypress.env('base_url') }/note/new?employee=${Cypress.env('users').employee.pk}`
    //       expect(text).to.eq(link);
    //     });
    //   });
    // })
  })

  it('Employee submits self-evaluation', () => {
  })

  it('Manager submits and signs evaluation', () => {
    // Colleague feedback should be present
  })

  it('Employee reviews and signs evaluation', () => {
  })

  it('All upper managers sign evaluation', () => {
  })

  it('Deletes the review', () => {
    const pk = LOCAL_STORAGE_MEMORY['reviewPK']
    loginSuperuser().then(() => {
      const token = localStorage.getItem('user-token')
      const url = `${ Cypress.env('api_url') }/api/v1/review/${ pk }`
      if (pk) {
        cy.request({
          method: 'DELETE',
          url,
          headers: {
            Authorization: `Token ${ token }`,
          },
        }).then(() => {
          cy.log(`Deleted review pk: ${ pk }`)
        })
      }
    })
  })

  // it('Fiscal reassigns back to submitter', () => {
  //   const pk = LOCAL_STORAGE_MEMORY['workflowPK']
  //   loginUser(Cypress.env('users').fiscalemployee).then(() => {
  //     visitUrl(`/wf/${pk}/transition`)
  //     // Can reassign
  //     const reassignButton = cy.get('button[name="reassign-button"]')
  //     reassignButton.should('not.have.attr', 'disabled')
  //     reassignButton.contains('Assigned to: Fiscal')
  //     // Reassign to SDS Hiring Lead
  //     reassignButton.click()
  //     cy.get('button[name="reassign-dialog-assignee-dropdown"]').click()
  //     cy.get('.q-menu > .q-list > .q-item').first().click()
  //     cy.get('textarea[name="reassign-extra-message"]').type('Reassigning to Submitter')
  //     cy.get('button[name="reassign-dialog-button"]').click()
  //     // Now cannot reassign
  //     cy.get('button[name="reassign-button"]').should('have.attr', 'disabled')
  //     cy.get('button[name="reassign-button"]').contains('Assigned to: GS Manager')
  //   })
  // })

  // it ('Submitter sends to fiscal a second time', () => {
  //   const pk = LOCAL_STORAGE_MEMORY['workflowPK']
  //   loginUser(Cypress.env('users').gsmanager).then(() => {
  //     visitUrl(`/wf/${pk}/transition`)
  //     // Cannot reassign
  //     cy.get('button[name="reassign-button"]').should('have.attr', 'disabled')
  //     cy.get('button[name="reassign-button"]').contains('Assigned to: GS Manager')
  //     // Submit the form
  //     cy.get('button[name="send-fiscal-button"]').click()
  //     cy.get('button[name="send-fiscal-dialog-button"]').click()
  //     cy.get('button[name="reassign-button"]').contains('Assigned to: Fiscal')
  //   })
  // })

  // it('Fiscal sends to HR', () => {
  //   const pk = LOCAL_STORAGE_MEMORY['workflowPK']
  //   loginUser(Cypress.env('users').fiscalemployee).then(() => {
  //     visitUrl(`/wf/${pk}/transition`)
  //     // Can reassign
  //     const reassignButton = cy.get('button[name="reassign-button"]')
  //     reassignButton.should('not.have.attr', 'disabled')
  //     reassignButton.contains('Assigned to: Fiscal')
  //     // Submit the form
  //     cy.get('button[name="send-hr-button"]').click()
  //     cy.get('button[name="send-hr-dialog-button"]').click()
  //     cy.get('button[name="reassign-button"]').contains('Assigned to: HR')
  //   })
  // })

  // it('HR sends to STN', () => {
  //   const pk = LOCAL_STORAGE_MEMORY['workflowPK']
  //   loginUser(Cypress.env('users').hremployee).then(() => {
  //     visitUrl(`/wf/${pk}/transition`)
  //     // Can reassign
  //     const reassignButton = cy.get('button[name="reassign-button"]')
  //     reassignButton.should('not.have.attr', 'disabled')
  //     reassignButton.contains('Assigned to: HR')
  //     // Submit the form
  //     cy.get('button[name="send-stn-button"]').click()
  //     cy.get('button[name="send-stn-dialog-button"]').click()
  //     cy.get('button[name="reassign-button"]').contains('Status: Complete')
  //   })
  // })

  // it('Deletes the workflow', () => {
  //   const pk = LOCAL_STORAGE_MEMORY['workflowPK']
  //   loginSuperuser().then(() => {
  //     const token = localStorage.getItem('user-token')
  //     const url = `${ Cypress.env('api_url') }/api/v1/workflowinstance/${ pk }`
  //     if (pk) {
  //       cy.request({
  //         method: 'DELETE',
  //         url,
  //         headers: {
  //           Authorization: `Token ${ token }`,
  //         },
  //       }).then(() => {
  //         cy.log(`Deleted workflow instance pk: ${ pk }`)
  //       })
  //     }
  //   })
  // })
})

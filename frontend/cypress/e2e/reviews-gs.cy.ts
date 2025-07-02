import {
  loginSuperuser, loginUser, randomString, visitUrl
} from '../support/helpers'

// Cypress clears localstorage between tests, so use this to store data
const LOCAL_STORAGE_MEMORY: { [key: string]: string } = {}

function clearTestData() {
  cy.writeFile('cypress/fixtures/temp-test-data.json', {})
}

function saveValue(key: string, value: string) {
  console.log(`Saving value for key: ${key}, value: ${value}`)
  cy.readFile('cypress/fixtures/temp-test-data.json')
    .then((existingData) => {
      const data = existingData || {}
      data[key] = value
      cy.writeFile('cypress/fixtures/temp-test-data.json', data)
    })
}

function getValue(key: string): Promise<string> {
  console.log(`Getting value for key: ${key}`)
  return new Promise((resolve) => {
    cy.readFile('cypress/fixtures/temp-test-data.json').then((data) => {
      debugger
      resolve(data[key])
    })
  })
}

describe('GS employee performance review process', () => {

  it('Creates a review', () => {
    clearTestData()
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
          form_pk: 1,
          period_start_date: '2024-06-30',
          period_end_date: '2025-06-30',
          effective_date: '2024-07-01',
        },
      }).then((resp) => {
        const pk = resp.body.pk
        saveValue('reviewPK', pk)
        // LOCAL_STORAGE_MEMORY['reviewPK'] = pk
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
          const route = `/note/new?employee=${Cypress.env('users').employee.pk}`
          saveValue('feedbackRoute', route)
          // LOCAL_STORAGE_MEMORY['feedbackRoute'] = route
          expect(text).to.eq(`${Cypress.env('base_url')}${route}`);
        });
      });
    })
  })

  it('Colleague uses link to submit feedback', () => {
    // const route = LOCAL_STORAGE_MEMORY['feedbackRoute']
    getValue('feedbackRoute').then((route) => {
      loginUser(Cypress.env('users').colleague).then(() => {
        console.log("Visiting route: ", route)
        visitUrl(route)
        cy.get('.employee-select input')
          .should('have.value', Cypress.env('users').employee.name)
        const feedback = randomString(20)
        cy.wrap(feedback).as('feedback')
        // LOCAL_STORAGE_MEMORY['feedback'] = feedback
        cy.get('#review-note-editor').type(feedback)
        cy.get("#review-note-create-button").click()
      })
    })
    
  })

  it('Employee submits self-evaluation', () => {
    loginUser(Cypress.env('users').employee).then(() => {
      visitUrl(Cypress.env('reviews_dashboard_path'))
      // TODO: SHOULD NOT CONTAIN FEEDVBACK
      cy.contains('Needs evaluation').siblings().last().find('button').click()
      const selfEvaluation = randomString(20)
      cy.wrap(selfEvaluation).as('selfEvaluation')
      // LOCAL_STORAGE_MEMORY['selfEvaluation'] = selfEvaluation
      cy.get('#employee-self-evaluation').type(selfEvaluation)
      cy.get('#save-comments-employee').click()
    })
  })

  it('Manager submits and signs evaluation', () => {
    loginUser(Cypress.env('users').gsmanager).then(() => {
      visitUrl(Cypress.env('reviews_dashboard_path'))
      cy.contains('Needs evaluation').siblings().last().find('button').first()
        .click()
      cy.get('#step-increase').siblings().first().click()
      cy.get('#top-step-bonus').siblings().first().click()
      // Self-evaluation should be present
      cy.get('@selfEvaluation').then((selfEvaluation) => {
         cy.contains(selfEvaluation)
      })
      // Colleague feedback should be present
      cy.get('@feedback').then((feedback) => {
         cy.contains(feedback)
      })
      cy.get('.factors-radio-box-meets-job-requirements').each(($el) => {
        cy.wrap($el).click()
      })
      const longResponse = randomString(20)
      cy.wrap(longResponse).as('longResponse')
      // LOCAL_STORAGE_MEMORY['longResponse'] = longResponse
      cy.get('.long-response-editor').each(($el) => {
        cy.wrap($el).type(longResponse)
      })
      cy.get('#update-button').click()
      cy.contains('Click to Sign').click()
      cy.contains('Your signature has been recorded')
      cy.contains('Return to Dashboard').click()
      cy.url().should('include', Cypress.env('reviews_dashboard_path'))
    })
  })

  it('Employee reviews and signs evaluation', () => {
  })

  it('All upper managers sign evaluation', () => {
  })

  it('Deletes the review', () => {
    // const pk = LOCAL_STORAGE_MEMORY['reviewPK']
    cy.get('@reviewPK').then((pk) => {
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
        // Delete most recently created review note
      })
    })
  })
})

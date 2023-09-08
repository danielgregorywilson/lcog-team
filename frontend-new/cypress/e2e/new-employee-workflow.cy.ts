import { title } from 'process'
import { loginSuperuser, loginUser, randomString, visitUrl } from '../support/helpers'

// Cypress clears localstorage between tests, so use this to store data
const LOCAL_STORAGE_MEMORY: { [key: string]: string } = {}

function employeeIDViewAndEdit() {
  const employeeIDSelect = cy.get('select[name="employee-id"]')
  const employeeIDInput = employeeIDSelect.siblings('input')
  employeeIDInput.click()
  cy.get('.q-menu > .q-virtual-scroll__content > .q-item > .q-item__section > .q-item__label').first().click()
  employeeIDSelect.get('option').first().should('have.value', 'CLSD')
  const employeeNumber = cy.get('input[name="employee-number"]')
  employeeNumber.type('1234')
  employeeNumber.should('have.value', '1234')
  const email = cy.get('input[name="email"]')
  email.click()
  email.invoke('val').should('not.be.empty')
}

function employeeIDViewNotEdit() {
  const employeeIDSelect = cy.get('select[name="employee-id"]')
  employeeIDSelect.siblings('input').should('not.exist')
  const employeeNumber = cy.get('input[name="employee-number"]').should('exist')
  employeeNumber.should('have.attr', 'readonly')
  const email = cy.get('input[name="email"]')
  email.click()
  email.invoke('val').should('be.empty')
}

function salaryViewAndEdit() {
  const salaryRange = cy.get('input[name="salary-range"]').should('exist')
  salaryRange.should('not.have.attr', 'readonly', 'readonly')
  const salaryStep = cy.get('#salary-step input').should('exist')
  salaryStep.click()
  cy.get('.q-menu > .q-virtual-scroll__content > .q-item > .q-item__section > .q-item__label').first().click()
}

function salaryNotView() {
  cy.get('input[name="salary-range"]').should('not.exist')
  cy.get('#salary-step input').should('not.exist')
}

function managerViewNotEdit() {
  const managerInput = cy.get('select[name="manager"]').siblings('input')
  managerInput.should('have.attr', 'readonly', 'readonly')
}

function fiscalViewAndEdit() {
  const fiscalField = cy.get('textarea[name="fiscal-field"]')
  fiscalField.type('123-456-7890 / 30%{enter}555-555-5555 / 70%')
  fiscalField.invoke('val').should('contain', '123-456-7890 / 30%')
}

function fiscalViewNotEdit() {
  const fiscalField = cy.get('textarea[name="fiscal-field"]')
  fiscalField.should('have.attr', 'readonly', 'readonly')
}

function otherFieldsViewAndEdit() {
  cy.get('#type-return').click()
  cy.get('#type-return').should('have.attr', 'aria-checked', 'true')
  cy.get('#type-change').click()
  cy.get('#type-change').should('have.attr', 'aria-checked', 'true')
  cy.get('#type-exit').click()
  cy.get('#type-exit').should('have.attr', 'aria-checked', 'true')
  const firstName = randomString(10)
  cy.get('input[name="first-name"]').clear().type(firstName)
  cy.get('input[name="first-name"]').should('have.value', firstName)
  const middleInitial = randomString(1)
  cy.get('input[name="middle-initial"]').clear().type(middleInitial)
  cy.get('input[name="middle-initial"]').should('have.value', middleInitial)
  const lastName = randomString(10)
  cy.get('input[name="last-name"]').clear().type(lastName)
  cy.get('input[name="last-name"]').should('have.value', lastName)
  const preferredName = randomString(20)
  cy.get('input[name="preferred-name"]').clear().type(preferredName)
  cy.get('input[name="preferred-name"]').should('have.value', preferredName)
  const titleInput = cy.get('select[name="title"]').siblings('input')
  titleInput.type('Dev')
  cy.wait(500) // Wait for the title to be selected
  titleInput.type('{downArrow}{enter}')
  titleInput.should('have.value', 'Senior Web Developer')
  const fte = 2
  cy.get('input[name="fte"]').clear().type(fte.toString())
  cy.get('input[name="fte"]').should('have.value', fte.toString())
  cy.get('#bilingual').click()
  cy.get('#bilingual').should('have.attr', 'aria-checked', 'true')
  cy.get('#second-language').click()
  cy.get('.q-menu > .q-virtual-scroll__content > .q-item').first().click()
  cy.get('#union-affiliation').click()
  cy.get('.q-menu > .q-virtual-scroll__content > .q-item').first().click()
}

function otherFieldsViewNotEdit() {
  cy.get('#type-return').click()
  cy.get('#type-new').should('have.attr', 'aria-checked', 'true')
  cy.get('#type-change').click()
  cy.get('#type-new').should('have.attr', 'aria-checked', 'true')
  cy.get('#type-exit').click()
  cy.get('#type-new').should('have.attr', 'aria-checked', 'true')
  cy.get('input[name="first-name"]').should('have.attr', 'readonly')
  cy.get('input[name="middle-initial"]').should('have.attr', 'readonly')
  cy.get('input[name="last-name"]').should('have.attr', 'readonly')
  cy.get('input[name="preferred-name"]').should('have.attr', 'readonly')
  cy.get('select[name="title"]').should('not.exist')
  cy.get('input[name="fte"]').should('have.attr', 'readonly')
  cy.get('#bilingual').click()
  cy.get('#bilingual').should('have.attr', 'aria-checked', 'false')
  cy.get('select[name="second-language"]').should('not.exist')
  cy.get('select[name="union-affiliation"]').should('not.exist')
}

describe('New employee workflow', () => {

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
        cy.get('input[name="first-name"]').type('Xavier')
        cy.get('input[name="last-name"]').type('Xanthopoulos')

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

        // Can view but not edit employee ID fields
        employeeIDViewNotEdit()
        // Can view and edit the salary fields
        salaryViewAndEdit
        // Can view but not edit the fiscal field
        fiscalViewNotEdit()
        // Can view and edit all other fields
        otherFieldsViewAndEdit()
      })
    })
  })

  it('Another manager can view the workflow but not edit certain fields', () => {
    const pk = LOCAL_STORAGE_MEMORY['workflowPK']
    loginUser(Cypress.env('users').manager2).then(() => {
      visitUrl(`/wf/${pk}/transition`)

      // Can view but not edit employee ID fields
      employeeIDViewNotEdit()
      // Cannot view the salary fields
      salaryNotView()
      // Can view but not edit the manager field
      managerViewNotEdit()
      // Can view but not edit the fiscal field
      fiscalViewNotEdit()
      // Can view but not edit all other fields
      otherFieldsViewNotEdit()
    })
  })

  it('Hiring Manager can view the workflow and edit certain fields', () => {
    const pk = LOCAL_STORAGE_MEMORY['workflowPK']
    loginUser(Cypress.env('users').hiringmanager).then(() => {
      visitUrl(`/wf/${pk}/transition`)

      // Can view but not edit employee ID fields
      employeeIDViewNotEdit()
      // Can view and edit the salary fields
      salaryViewAndEdit()
      // Can view but not edit the manager field
      managerViewNotEdit()
      // Can view but not edit the fiscal field
      fiscalViewNotEdit()
      // Can view and edit all other fields
      otherFieldsViewAndEdit()
    })
  })

  it('HR can view the workflow and edit certain fields', () => {
    const pk = LOCAL_STORAGE_MEMORY['workflowPK']
    loginUser(Cypress.env('users').hremployee).then(() => {
      visitUrl(`/wf/${pk}/transition`)

      // Can view and edit employee ID fields
      employeeIDViewAndEdit()
      // Can view and edit the salary fields
      salaryViewAndEdit()
      // Can view but not edit the manager field
      managerViewNotEdit()
      // Can view but not edit the fiscal field
      fiscalViewNotEdit()
      // Can view and edit all other fields
      otherFieldsViewAndEdit()
    })
  })

  it('Fiscal can view the workflow and edit certain fields', () => {
    const pk = LOCAL_STORAGE_MEMORY['workflowPK']
    loginUser(Cypress.env('users').fiscalemployee).then(() => {
      visitUrl(`/wf/${pk}/transition`)

      // Can view but not edit employee ID fields
      employeeIDViewNotEdit()
      // Can view and edit the salary fields
      salaryViewAndEdit()
      // Can view but not edit the manager field
      managerViewNotEdit()
      // Can view and edit the fiscal field
      fiscalViewAndEdit()
      // Can view and edit all other fields
      otherFieldsViewAndEdit()
    })
  })

  it ('SDS Hiring Lead can view the workflow and edit certain fields', () => {
    const pk = LOCAL_STORAGE_MEMORY['workflowPK']
    loginUser(Cypress.env('users').sdshiringlead).then(() => {
      visitUrl(`/wf/${pk}/transition`)

      // Can view but not edit employee ID fields
      employeeIDViewNotEdit()
      // Can view and edit the salary fields
      salaryViewAndEdit()
      // Can view but not edit the manager field
      managerViewNotEdit()
      // Can view and edit the fiscal field
      fiscalViewNotEdit()
      // Can view and edit all other fields
      otherFieldsViewAndEdit()
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

function visit_url(path: string) {
  cy.visit(`${ Cypress.env('base_url') }${ path }`)
}

function login_superuser() {
  const username = Cypress.env('users').superuser.username
  const password = Cypress.env('users').superuser.password

  cy.request('POST', 'http://localhost:8000/api/api-token-auth-password/', {username, password})
    .its('body.token')
    .should('exist')
    .then(token =>
        localStorage.setItem('user-token', `${token}`)
    );
}

const LOCAL_STORAGE_MEMORY: { [key: string]: string } = {}

describe('New employee workflow', () => {

  it('Manager logs in, creates a new employee workflow, and submits it', () => {
    // Create a new employee workflow
    visit_url(Cypress.env('login_path'))
    cy.get('input#username').type(Cypress.env('users').manager.username)
    cy.get('input#password').type(Cypress.env('users').manager.password)
    cy.get('button[type="submit"]').click()
    cy.location('pathname', {timeout: 60000}) // Wait until the dashboard loads
      .should('include', '/dashboard')
    cy.wait(1000) // Wait for the dashboard to load and all api calls to be made
    visit_url(Cypress.env('workflows_dashboard_path'))
    cy.get('.workflowtable-new .row-add-new').click()
    cy.wait(1000) // Wait for the new transition form to load
    cy.url().then((url) => {
      const match = url.match(/wf\/(\d+)\/transition/)
      const pk = match ? match[1] : null
      if (pk) {
        LOCAL_STORAGE_MEMORY['workflowPK'] = pk
      }
      cy.log(`Created workflow pk: ${ pk }`)
    })

    // Enter data into the form
    cy.get('input[name="first-name"]').type('Xavier')
    cy.get('input[name="last-name"]').type('Xanthopoulos')

    // TODO: Try cypress-real-events to focus the email field
    cy.get('input[name="email"]').focus()

    const titleInput = cy.get('select[name="title"]').siblings('input')
    titleInput.type('Case')
    cy.wait(1000) // Wait for the title to be selected
    titleInput.type('{downArrow}{enter}')

    const managerInput = cy.get('select[name="manager"]').siblings('input')
    managerInput.type('Daniel Wil')
    cy.wait(1000) // Wait for the title to be selected
    managerInput.type('{downArrow}{enter}')

    // Save the form
    cy.get('button[name="save-button"]').click()

  })

  it('Deletes the workflow', () => {
    const pk = LOCAL_STORAGE_MEMORY['workflowPK']
    // TODO: Log in SU as a command
    const username = Cypress.env('users').superuser.username
    const password = Cypress.env('users').superuser.password

    cy.request({
      method: 'POST',
      url: 'http://localhost:8000/api/api-token-auth-password/',
      body: {username, password}
    })
      .its('body.token')
      .should('exist')
      .then((token) => {
        localStorage.setItem('user-token', `${token}`)
        if (pk) {
          cy.request({
            method: 'DELETE',
            url: `http://localhost:8000/api/v1/workflowinstance/${ pk }`,
            headers: {
              Authorization: `Token ${ token }`,
            },
          })
        }
        cy.log(`Deleted workflow instance pk: ${ pk }`)
      })
  })
})

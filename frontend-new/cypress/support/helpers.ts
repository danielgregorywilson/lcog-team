export function visitUrl(path: string) {
  cy.visit(`${ Cypress.env('base_url') }${ path }`)
}

export function loginSuperuser() {
  return new Promise((resolve, reject) => {
    const username = Cypress.env('users').superuser.username
    const password = Cypress.env('users').superuser.password

    cy.request('POST', 'http://localhost:8000/api/api-token-auth-password/', {username, password})
      .its('body.token')
      .should('exist')
      .then(token => {
        localStorage.setItem('user-token', `${token}`)
        resolve('Successfully logged in superuser')
      });
  })
}

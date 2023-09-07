export function visitUrl(path: string) {
  return new Promise((resolve, reject) => {
    cy.visit(`${ Cypress.env('base_url') }${ path }`).then(() => {
      resolve('Successfully visited url')
    })
  })
}

export function loginUser(user: { username: string, password: string }) {
  return new Promise((resolve, reject) => {
    visitUrl(Cypress.env('login_path')).then(() => {
      cy.get('input#username').type(user.username)
      cy.get('input#password').type(user.password)
      cy.get('button[type="submit"]').click()
      cy.location('pathname', {timeout: 60000}) // Wait until the dashboard loads
        .should('include', '/dashboard')
        .then(() => {
          resolve('Successfully logged in user')
        })
    })
  })
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

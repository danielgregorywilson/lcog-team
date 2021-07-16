# lcog-team

# Run the backend locally
`source ../env/bin/activate && ./manage.py runserver`

# Run the frontend locally
`cd frontend && quasar dev`

# Cypress e2e tests
Open Cypress launcher to run individual tests
`cd frontend`
`npm run cypress:open`
Run Cypress tests in the background and upload results to https://dashboard.cypress.io/
`cd frontend`
`npm run cypress:run`
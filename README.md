# lcog-team

# Run the backend locally
# MacOS
`source ../env/bin/activate && ./manage.py runserver`
# Windows
`.\env_20220114\Scripts\activate && .\manage.py runserver`

# Run the frontend locally
`cd frontend && quasar dev`

# Setting up the backend for the first time
1) Ensure that .env file is in place (in OneDrive). Ensure settings are such that sqlite db is used
2) Run migrations
MacOS `./manage.py migrate`
Windows `.\manage.py migrate`
3) Create a superuser
MacOS `./manage.py createsuperuser --username=dwilsonsu`
Windows `.\manage.py createsuperuser --username=dwilsonsu`
4) Run commands to import employees and reviews from Caselle

# Setting up the frontend for the first time



# Cypress e2e tests
Open Cypress launcher to run individual tests
`cd frontend && npm run cypress:open`
Run Cypress tests in the background and upload results to https://dashboard.cypress.io/
`cd frontend`
`npm run cypress:run`

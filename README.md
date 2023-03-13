# LCOG Team App Backend Readme

Python 3.11.2 

# Run the backend locally
# MacOS
`source ../env/bin/activate && ./manage.py runserver`
# Windows
`..\env_20230309\Scripts\activate; .\manage.py runserver`

# Setting up the backend for the first time
1) Ensure that .env file is in place (in OneDrive). Ensure settings are such that sqlite db is used
2) Create a python virtualenv
MacOS `virtualenv env_20230309`
Windows `python -m venv env_20230309`
3) Activate virtualenv
MacOS `source ./env/bin/activate`
Windows `.\env_20230309\Scripts\activate`
4) Install requirements
MacOS `pip install -r ./code/requirements.txt`
Windows `pip install -r .\code\requirements-windows.txt`
5) Run migrations
MacOS `./manage.py migrate`
Windows `.\manage.py migrate`
6) Create a superuser
MacOS `./manage.py createsuperuser --username=USERNAME`
Windows `.\code\manage.py createsuperuser --username=USERNAME`
7) Run commands to import employees and reviews from Caselle
8) Add settings_local.py file from an existing install
9) Run the backend locally
MacOS `./manage.py runserver`
Windows `.\manage.py runserver`

# Install Elastic Beanstalk CLI
https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install.html
Manually install the CLI using pip. Modify environment variable PATH from instructions.

# Cypress e2e tests
Open Cypress launcher to run individual tests
`cd frontend && npm run cypress:open`
Run Cypress tests in the background and upload results to https://dashboard.cypress.io/
`cd frontend`
`npm run cypress:run`

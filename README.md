# lcog-hr

# Run the backend locally
Activate the virtual environment
`source env/bin/activate` 
Start the server
`./manage.py runserver`

# Run the frontend locally
`cd frontend`
`quasar dev`

# Cypress e2e tests
Open Cypress launcher to run individual tests
`npm run cypress:open`
Run Cypress tests in the background and upload results to https://dashboard.cypress.io/
`npm run cypress:run`

# Deploy backend
In mainsite/middleware/CorsMiddleware, make sure the correct response["Access-Control-Allow-Origin"] is commented out.
`eb deploy --profile lcog`

# Deploy frontend
`cd frontend`
`quasar build`
Navigate to https://s3.console.aws.amazon.com/s3/buckets/lcog-hr-frontend/
Under the 'Objects' tab is the list of files
Drag the contents of frontend/dist/spa to the window to upload the build

# Production Sites
Production Frontend - http://lcog-hr-frontend.s3-website-us-west-2.amazonaws.com
Production API - http://lcog-internal-env.eba-4t9yrmiu.us-west-2.elasticbeanstalk.com/api/
Production Backend - http://lcog-internal-env.eba-4t9yrmiu.us-west-2.elasticbeanstalk.com/admin/
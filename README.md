# lcog-hr


# Run the backend locally
Activate the virtual environment
`source env/bin/activate` 
Start the server
`./manage.py runserver`


# Run the frontend locally
`cd frontend`
`quasar dev`


# Deploy backend
`eb deploy --profile lcog`


# Deploy frontend
`cd frontend`
`quasar build`
Navigate to https://s3.console.aws.amazon.com/s3/buckets/lcog-hr-frontend/
Under the overview tab is the list of files
Drag the contents of frontend/dist/spa to the window to upload the build
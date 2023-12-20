# LCOG Team App Frontend Readme

A Quasar Project

Node 18.15.0
Vue 3
Quasar 2
Pinia 

## Install the dependencies
```bash
yarn
# or
npm install
```

# Run the frontend locally
# MacOS
`cd frontend && quasar dev`
# Windows
`cd frontend; quasar dev`

### Start the app in development mode (hot-code reloading, error reporting, etc.)
```bash
quasar dev
```

# Cypress e2e tests
Open Cypress launcher to run individual tests
`cd frontend-new && npm run cypress:open`
Run Cypress tests in the background and upload results to https://cloud.cypress.io/
`cd frontend-new && npm run cypress:run`

### Lint the files
```bash
yarn lint
# or
npm run lint
```


### Format the files
```bash
yarn format
# or
npm run format
```



### Build the app for production
```bash
quasar build
```

### Customize the configuration
See [Configuring quasar.config.js](https://v2.quasar.dev/quasar-cli-vite/quasar-config-js).

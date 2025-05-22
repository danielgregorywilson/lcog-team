import { defineStore } from 'pinia'
import axios from 'axios'
import { Buffer } from 'buffer'

import { apiURL } from 'src/stores/index'
import { useMealsStore } from 'src/stores/meals'
import { usePeopleStore } from 'src/stores/people'
import { usePurchaseStore } from 'src/stores/purchase'
import { useResponsibilityStore } from 'src/stores/responsibility'
import { useSecurityMessageStore } from 'src/stores/securitymessage'
import { useTimeOffStore } from 'src/stores/timeoff'
import { useUserStore } from 'src/stores/user'
import { useWorkflowsStore } from 'src/stores/workflows'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('user-token') || '',
    status: '',
    goToAuthCode: localStorage.getItem('goToAuthCode') || '',
    goToAccessToken: localStorage.getItem('goToAccessToken') || '',
  }),

  getters: {
    isAuthenticated: state => !!state.token
  },

  actions: {
    // Log in with username and password
    authWithUsername(user: {username: string, password: string}) {
      return this.authenticate(user, `${ apiURL }api/api-token-auth-password/`)
    },
    // Log in with Microsoft Azure SSO
    authWithMicrosoft(user: { username: string, firstName: string, lastName: string }) {
      return this.authenticate(user, `${ apiURL }api/api-token-auth/`)
    },
    authenticate(
      user: { username: string, password: string } | 
        { username: string, firstName: string, lastName: string },
      url: string
    ): Promise<string> {
      return new Promise((resolve, reject) => {
        this.status = 'loading'
        axios({url: url, data: user, method: 'POST'})
          .then((resp) => {
            const token = resp.data.token
            localStorage.setItem('user-token', token)
            axios.defaults.headers.common['Authorization'] = `Token ${token}`
            this.status = 'success'
            this.token = token
            // you have your token, now log in your user :)
            const userStore = useUserStore()
            userStore.userRequest()
              .catch(err => console.log(err))
            resolve(token)
          })
        .catch(err => {
          this.status = 'error'
          // if the request fails, remove any possible user token
          localStorage.removeItem('user-token')
          reject(err)
        })
      })
    },
    authLogout() {
      return new Promise((resolve) => {
        this.$reset()
        localStorage.removeItem('user-token') // clear your user's token from localstorage
        const mealsStore = useMealsStore()
        const peopleStore = usePeopleStore()
        const purchaseStore = usePurchaseStore()
        const responsibilityStore = useResponsibilityStore()
        const securityMessageStore = useSecurityMessageStore()
        const timeOffStore = useTimeOffStore()
        const userStore = useUserStore()
        const workflowsStore = useWorkflowsStore()
        mealsStore.authLogout()
          .catch(err => console.log(err))
        peopleStore.authLogout()
          .catch(err => console.log(err))
        // TODO: Uncomment these when the modules are ready
        // dispatch('performanceReviewModule/authLogout', null, { root: true })
        //   .catch(err => console.log(err))
        purchaseStore.authLogout()
          .catch(err => console.log(err))
        responsibilityStore.authLogout()
          .catch(err => console.log(err))
        securityMessageStore.authLogout()
          .catch(err => console.log(err))
        // dispatch('teleworkModule/authLogout', null, { root: true })
        //   .catch(err => console.log(err))
        timeOffStore.authLogout()
          .catch(err => console.log(err))
        userStore.authLogout()
          .catch(err => console.log(err))
        workflowsStore.authLogout()
          .catch(err => console.log(err))
        
        resolve('Successfully logged user out')
      })
    },

    //////////
    // GoTo //
    //////////

    setGoToAuthCode(authCode: string): Promise<void> {
      return new Promise((resolve) => {
        this.goToAuthCode = authCode
        localStorage.setItem('goToAuthCode', authCode)
        resolve()
      })
    },

    getGoToAccessToken(authCode: string): Promise<void> {
      return new Promise((resolve, reject) => {
        const clientID = import.meta.env.VITE_GOTO_CLIENT_ID
        const clientSecret = import.meta.env.VITE_GOTO_CLIENT_SECRET
        // Import Buffer for base64 encoding
        const authHeader = Buffer.from(`${clientID}:${clientSecret}`).toString('base64')

        axios.post(
          `https://authentication.logmeininc.com/oauth/token`,
          {
            "grant_type": "authorization_code",
            "code": authCode,
            "redirect_uri": "http://localhost:9000/oauth/gta-callback",
          },
          { headers: {
            'Authorization': `Basic ${authHeader}`,
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
          }}
        )
        .then((resp) => {
          this.goToAccessToken = resp.data.access_token
          localStorage.setItem('goToAccessToken', this.goToAccessToken)
          resolve()
        })
        .catch(err => {
          reject(err)
        })
      })
    },

    getMe(accessToken: string): Promise<void> {
      return new Promise((resolve, reject) => {
        axios.get(
          `https://api.getgo.com/identity/v1/Users/me`,
          {
            headers: {
              'Accept': 'application/json',
              'Authorization': `Bearer ${accessToken}`,
            }
          }
        )
        .then((resp) => {
          resolve()
        })
        .catch(err => {
          reject(err)
        })
      })
    },

    getIncidents(accessToken: string): Promise<void> {
      return new Promise((resolve, reject) => {
        axios.get(
          `https://api.getgo.com/G2ASD/rest/v2/incidents?accountKey=${import.meta.env.VITE_GOTO_ACCOUNT_KEY}`,
          {
            headers: {
              'Accept': 'application/json',
              'Authorization': `Bearer ${accessToken}`,
              'Content-Type': 'application/json',
            }
          }
        )
        .then((resp) => {
          debugger
          resolve()
        })
        .catch(err => {
          reject(err)
        })
      })
    },

    getOneIncident(accessToken: string): Promise<void> {
      return new Promise((resolve, reject) => {
        axios.get(
          `https://api.getgo.com/G2ASD/rest/v2/incidents/412?accountKey=${import.meta.env.VITE_GOTO_ACCOUNT_KEY}`,
          {
            headers: {
              'Accept': 'application/json',
              'Authorization': `Bearer ${accessToken}`,
              'Content-Type': 'application/json',
            }
          }
        )
        .then((resp) => {
          debugger
          resolve()
        })
        .catch(err => {
          reject(err)
        })
      })
    },

    createNewIncident(accessToken: string): Promise<void> {
      return new Promise((resolve, reject) => {
        axios.post(
          `https://api.getgo.com/G2ASD/rest/v2/incidents?accountKey=${import.meta.env.VITE_GOTO_ACCOUNT_KEY}`,
          {
            // "title": "Dan Wilson's Test Incident",
            // "description": "This is a test incident created via API through the Team App.",
            // "priority": "medium",
            // "category": "Technical Issue",
            

            "title": "Postman test title",
            "notify_watchlisted": 1,
            "notify_customer": 1,
            "customer": "/customers/1978793872884138217",
            "customer_viewable": 1,
            "watching_external_emails": {
              "add": [
                "dgw@mac.com", "dgw@me.com"
              ]
            },
            "linkages": {"add": ["/incidents/30792"]},
            "type": "Feedback",
            "priority_level": "1",
            "interesting": "true",
            "common": "true",
            "has_agreed_due_date": "true",
            "due_date": "10/10/2025",
            "tasks": {"create": [{"title": "task1", "status": "in_progress"}]},
            "comments": {
              "create": [
                {"note": "This is the new comment",},
                {"note": "This is the second comment"}
              ]
            },
            "symptom": {
              "note": "This is the symptom",
            }
          },  
          { headers: {
            'Accept': 'application/json',
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
          }}
        )
        .then(() => {
          debugger
          resolve()
        })
        .catch(err => {
          debugger
          reject(err)
        })
      })
    }
  }
})

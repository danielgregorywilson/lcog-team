<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title>
          <div v-if="emplayeeName()">
            Hi {{ emplayeeName() }}
          </div>
        </q-toolbar-title>

        <q-btn flat no-caps :to="{ name: 'release-notes'}">{{ appVersionTag() }}</q-btn>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      content-class="bg-grey-1"
      :width="210"
    >
      <q-list>        
        <q-item
          clickable
          :to="{ name: 'dashboard' }"
          v-if="isAuthenticated()"
        >
          <q-item-section avatar>
            <q-img
              id="lcog-logo"
              src="../assets/lcog-logo.png"
              style="width: 30px;"
            />
          </q-item-section>
          <q-item-section>
            <q-item-label>LCOG Team App</q-item-label>
          </q-item-section>
        </q-item>
        <q-item
          clickable
          @click='loginWithMicrosoft'
          v-if="!isAuthenticated()"
        >
          <q-item-section avatar>
            <q-img
              id="ms-logo"
              src="../assets/microsoft-logo.svg"
              style="width: 24px;"
            />
          </q-item-section>
          <q-item-section>
            <q-item-label>Sign in with Microsoft</q-item-label>
          </q-item-section>
        </q-item>
        <div v-if="isAuthenticated()">
          <NavLink
            v-for="link in navLinks"
            :key="link.title"
            v-bind="link"
            :id="link.id"
          />
        </div>
        <q-item
          clickable
          @click='logout'
          v-if="isAuthenticated()"
        >
          <q-item-section avatar>
            <q-icon name='west' />
          </q-item-section>
          <q-item-section>
            <q-item-label>Log Out</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script lang="ts">
import { UserAgentApplication } from 'msal'
import { defineComponent, ref } from 'vue'
import { useAuthStore } from 'src/stores/auth'
import { useUserStore } from 'src/stores/user'
import { Configuration } from 'electron-builder'
import NavLink from 'components/NavLink.vue'

interface LinkData {
  title: string;
  icon: string;
  link: string;
  id?: string;
  managerOnly?: boolean;
  eligibleForTeleworkApplicationOnly?: boolean;
  hasWorkflowRoles?: boolean
  canViewMOWRoutes?: boolean
}

const linksData: Array<LinkData> = [
  {
    title: 'Time Off',
    icon: 'schedule',
    link: '/timeoff'
  },
  {
    title: 'Responsibilities',
    icon: 'hardware',
    link: '/responsibilities'
  },
  {
    title: 'Workflows',
    icon: 'double_arrow',
    link: '/workflows',
    hasWorkflowRoles: true
  },
  // {
  //   title: 'Performance Reviews',
  //   icon: 'assignment_turned_in',
  //   link: '/reviews',
  //   managerOnly: true
  // },
  {
    title: 'Schaefers Desk Reservation',
    icon: 'laptop',
    link: '/desk-reservation/schaefers/1'
  },
  {
    title: 'Meals on Wheels Map',
    icon: 'map',
    link: '/mow-map',
    canViewMOWRoutes: true
  },
  // {
  //   title: 'My Telework Application',
  //   icon: 'home_work',
  //   link: '/telework-application',
  //   eligibleForTeleworkApplicationOnly: true
  // },
  // {
  //   title: 'Telework Policy',
  //   icon: 'computer',
  //   link: '/telework'
  // },
  // {
  //   title: 'Security Message',
  //   icon: 'security',
  //   link: '/security-message'
  // },
  {
    title: 'My Profile',
    icon: 'person',
    link: '/profile',
    id: 'nav-profile'
  },
];

// For msal.js Azure/AD SSO 
const msalConfig: Configuration = {
  auth: {
    clientId: '2c4ec8a0-6be9-4c9c-a6b6-6a40392b8e3e',
    authority: 'https://login.microsoftonline.com/9a80ddb7-1790-4782-a634-ef32f273169c',
    redirectUri: process.env.DASHBOARD_URL,
  },
  cache: {
    cacheLocation: 'sessionStorage', // This configures where your cache will be stored
    storeAuthStateInCookie: false, // Set this to "true" if you are having issues on IE11 or Edge
  }
}

const myMSALObj = new UserAgentApplication(msalConfig)

const loginRequest = {
  scopes: ['openid', 'profile', 'User.Read']
}

export default defineComponent({
  name: 'MainLayout',

  components: {
    NavLink
  },

  methods: {
    toggleLeftDrawer () {
      this.leftDrawerOpen = !this.leftDrawerOpen
    },

    appVersionTag() {
      return process.env.APP_VERSION_TAG
    },

    isAuthenticated(): boolean {
      return this.authStore['isAuthenticated']
    },
    
    emplayeeName(): string {
      return this.userStore['getEmployeeProfile'].name
    },

    getCurrentUser(): void {
      if (this.authStore['isAuthenticated'] && !this.userStore['isProfileLoaded']) {
        this.userStore.userRequest()
          .catch(e => {
            console.error('Error getting user from store', e)
          })
      }
    },

    loginWithMicrosoft(): void {
      myMSALObj.loginPopup(loginRequest)
        .then(() => {
          if (myMSALObj.getAccount()) {
            let account = myMSALObj.getAccount()
            let firstName = account.name.split(' ')[1][0].toUpperCase() + account.name.split(' ')[1].substring(1).toLowerCase()
            let lastName = account.name.split(' ')[0][0].toUpperCase() + account.name.split(' ')[0].substring(1).toLowerCase()
            this.authStore.setAuth({ username: account.userName, firstName, lastName })
              .then(() => this.$router.push('/'))
              .catch((err) => console.log(err))
          }      
        }).catch(function (error) {
            console.log(error);
        });
    },

    loginDev(): void {
      this.$router.push('/auth/login')
        .catch(e => {
          console.error('Error navigating to login page', e)
        })
    },

    logout() {
      if (process.env.DEV) {
        this.logoutDev()
      } else {
        this.logoutWithMicrosoft()
      }
    },

    logoutWithMicrosoft() {
      this.authStore.authLogout()
        .then(() => {
          this.myMSALObj.logout();
        })
        .catch(e => {
          console.error('Error logging out', e);
        })
    },

    // TODO: Old logout
    logoutDev(): void {
      this.authStore.authLogout()
        .then(() => {
          this.$router.push('/auth/login')
            .catch(e => {
              console.error('Error navigating to login page after logout', e)
            })
        })
        .catch(e => {
          console.error('Error logging out', e);
        })
    }
  },

  setup () {
    const authStore = useAuthStore()
    const userStore = useUserStore()

    const leftDrawerOpen = ref(false)

    return {
      navLinks: linksData,
      authStore,
      userStore,
      leftDrawerOpen,
      msalConfig,
      myMSALObj,
      loginRequest
    }
  }
});
</script>

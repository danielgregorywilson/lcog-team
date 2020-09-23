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
          @click="leftDrawerOpen = !leftDrawerOpen"
        />

        <q-toolbar-title>
          Hi {{ name }}
        </q-toolbar-title>

        <div>Quasar v{{ $q.version }}</div>
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
        <q-item-label
          header
          class="text-grey-8"
        >
          LCOG HR App
        </q-item-label>
        <NavLink
          v-for="link in navLinks"
          :key="link.title"
          v-bind="link"
        />
        <q-item
          clickable
          @click='logout'
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
import NavLink from 'components/NavLink.vue'

import { Component, Vue } from 'vue-property-decorator'

import { AxiosUserRetrieveOneServerResponse } from '../store/types'

import CurrentUserDataService from '../services/CurrentUserDataService';

interface LinkData {
  title: string;
  icon: string;
  link: string;
}

const linksData: Array<LinkData> = [
  {
    title: 'Dashboard',
    icon: 'dashboard',
    link: '/dashboard'
  },
  {
    title: 'Performance Reviews',
    icon: 'assignment_turned_in',
    link: '/reviews'
  },
  {
    title: 'Time off Requests',
    icon: 'schedule',
    link: '/timeoff'
  },
];

interface LayoutData {
  name: string
}

@Component({
  components: { NavLink }
})
export default class MainLayout extends Vue{
  private leftDrawerOpen = false;
  private navLinks: Array<LinkData> = linksData;
  private name = ''

  public getCurrentUser(): void {
    CurrentUserDataService.get()
      .then((response: AxiosUserRetrieveOneServerResponse) => {
        this.name = response.data.name;
      })
      .catch(e => {
        console.log(e);
      })
  }
  public logout(): void {
    this.$store.dispatch('authModule/authLogout')
    .then(() => {
      this.$router.push('/auth/login')
        .catch(e => {
          console.log(e)
        })
    })
    .catch(e => {
      console.log(e);
    })
  }
  mounted() {
    this.getCurrentUser();
  }
};
</script>

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
          LCOG HR App - Hi {{ name }}
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
          Essential Links
        </q-item-label>
        <EssentialLink
          v-for="link in essentialLinks"
          :key="link.title"
          v-bind="link"
        />
        <q-item
          clickable
          @click='logout'
        >
          <q-item-section avatar>
            <q-icon name='public' />
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
import EssentialLink from 'components/EssentialLink.vue'

const linksData = [
  {
    title: 'Dashboard',
    caption: '',
    icon: 'school',
    link: '/'
  },
  {
    title: 'Time off Requests',
    caption: '',
    icon: 'code',
    link: '/time-off'
  },
];

import { defineComponent, ref } from '@vue/composition-api';

import CurrentUserDataService from '../services/CurrentUserDataService';

export default defineComponent({
  name: 'MainLayout',
  components: { EssentialLink },
  setup() {
    const leftDrawerOpen = ref(false);
    const essentialLinks = ref(linksData);

    return {leftDrawerOpen, essentialLinks}
  },
  data() {
    return {
      name: null,
    }
  },
  methods: {
    getCurrentUser() {
      CurrentUserDataService.get()
        .then(response => {
          this.name = response.data.name;
          console.log(response.data);
        })
        .catch(e => {
          console.log(e);
        })
    },
    logout: function () {
      this.$store.dispatch('authModule/authLogout')
      .then(() => {
        this.$router.push('/auth/login')
      })
    }
  },
  mounted() {
    this.getCurrentUser();
  }
});
</script>

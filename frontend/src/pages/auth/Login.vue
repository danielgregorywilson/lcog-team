<template>
  <div class="q-pa-md">
    <form class="login" @submit.prevent="login">
      <h4>Sign in</h4>
      <div class="row q-pa-xs">
        <label class="q-pr-sm">User name</label>
        <input required v-model="username" type="text" placeholder="Snoopy"/>
      </div>
      <div class="row q-pa-xs">
        <label class="q-pr-sm">Password</label>
        <input required v-model="password" type="password" placeholder="Password"/>
      </div>
      <hr/>
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent } from '@vue/composition-api';


export default defineComponent({
  name: 'Login',
  components: { },
  data() {
    return {
      username: null,
      password: null,
    }
  },
  computed: {

  },
  methods: {
    login: function () {
      const { username, password } = this
      this.$store.dispatch('authModule/authRequest', { username, password })
        .then(() => this.$router.push('/'))
        .catch((err) => console.log(err))
    }
  },
  mounted() {

  },
  setup() {
  return {  };
  }
});
</script>

<template>
<div>
<form class="login" @submit.prevent="login">
<h1>Sign in</h1>
<label>User name</label>
<input required v-model="username" type="text" placeholder="Snoopy"/>
<label>Password</label>
<input required v-model="password" type="password" placeholder="Password"/>
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
        this.$store.dispatch(AUTH_REQUEST, { username, password }).then(() => {
            this.$router.push('/')
        })
    }},
    mounted() {

    },
    setup() {
    return {  };
    }
});
</script>

<template>
  <form @submit.prevent id="login" class="form-signin" method="post">

    <img class="mb-4" src="/static/spa/assets/images/python.svg" alt="" width="72" height="72">
    <h1 class="h3 mb-3 font-weight-normal">Please login or <router-link to="register"><u>register</u></router-link></h1>

    <label for="email" class="sr-only">Email address</label>
    <input
      v-model='credentials.email'
      type="email"
      id="email"
      name="email"
      class="form-control"
      placeholder="Email address"
      minlength="4"
      maxlength="64"
      required
      autofocus
    >

    <label for="password" class="sr-only">Password</label>
    <input
      v-model='credentials.password'
      type="password"
      id="password"
      name="password"
      class="form-control"
      placeholder="Password"
      minlength="4"
      maxlength="16"
      required
    >

    <button @click="authenticate()" class="btn btn-lg btn-primary btn-block" type="submit">Sign In</button>

    <p v-if="errors.length" class="err">
      <ul>
        <li v-for="error in errors">{{ error }}</li>
      </ul>
    </p>

    <p class="mt-5 mb-3 text-muted">©{{ new Date().getFullYear() }}</p>
  </form>
</template>

<script>
  import axios from 'axios'

  export default {
    name: 'Login',
    data () {
      return {
        credentials: {
          email: '',
          password: ''
        },
        errors: []
      }
    },
    beforeCreate: function() {
      document.body.className = 'auth'
    },
    methods: {
      authenticate () {
        this.checkForm();

        if (this.errors.length) return;

        const payload = this.credentials;
        axios.post(this.$store.state.endpoints.obtainJWT, payload).then((response) => {
          this.$store.commit('updateToken', response.data.token);
          this.$parent.$options.methods.auth(response.data.token);

          this.$router.replace({ name: 'home' });
        }).catch((error) => {
          if (error.response.data.non_field_errors.length) {
            this.errors.push('Unable to log in with provided credentials.')
          }
        })
      },

      /**
       * Validator for Login form
       */
      checkForm () {
        this.errors = [];

        if (!this.credentials.email) {
          this.errors.push("Email didn't set");
        }

        if (!this.credentials.password) {
          this.errors.push("Passwords didn't set");
        }

        if (this.credentials.password.length < 6) {
          this.errors.push("Passwords length too small");
        }
      }
    }
  }
</script>

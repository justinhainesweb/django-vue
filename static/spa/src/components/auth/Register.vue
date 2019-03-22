<template>
  <form @submit.prevent id="register" class="form-signup" method="post">

    <img class="mb-4" src="/static/spa/assets/images/python.svg" alt="" width="72" height="72">
    <h1 class="h3 mb-3 font-weight-normal">Please <router-link to="login"><u>login</u></router-link> or register</h1>

    <label for="email">Enter email (will be used as username)</label>
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

    <label for="password">Create password</label>
    <input
      v-model='credentials.password'
      type="password"
      id="password"
      name="password"
      class="form-control"
      placeholder="Enter password"
      minlength="4"
      maxlength="16"
      required
    >

    <label for="password1">Repeat password</label>
    <input
      v-model='credentials.password1'
      type="password"
      id="password1"
      name="password1"
      class="form-control"
      placeholder="Repeat password"
      minlength="4"
      maxlength="16"
      required
    >

    <br>
    <button @click="signup()" class="btn btn-lg btn-primary btn-block" type="submit">Sign Up</button>

    <p class="err" v-if="errors.length">
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
    name: 'Register',
    data () {
      return {
        credentials: {
          email: '',
          password: '',
          password1: ''
        },
        errors: []
      }
    },
    methods: {

      signup () {
        this.checkForm();

        if (this.errors.length) return;

        const payload = this.credentials;
        const url = this.$store.state.endpoints.signUp;

        axios.post(url, payload, {
          headers: {
            'Content-Type': 'application/json'
          }
        }).then((response) => {
          this.$store.commit('updateToken', response.data.token);
          this.$store.commit('setAuthUser', response.data);
          this.$router.push('home');
        }).catch(error => {
          if (error.response.data.email.length) {
            this.errors.push('User with this email has already exists');
          }
        })
      },

      /**
       * Validator for Register form
       */
      checkForm () {
        this.errors = [];

        if (!this.credentials.email) {
          this.errors.push("Email didn't set");
        }

        if (!this.credentials.password || !this.credentials.password1) {
          this.errors.push("Passwords didn't set");
        }

        if (this.credentials.password !== this.credentials.password1) {
          this.errors.push("Passwords doesn't match");
        }

        if (this.credentials.password.length < 6 || this.credentials.password1.length < 6) {
          this.errors.push("Passwords length too small");
        }
      }
    }
  }
</script>

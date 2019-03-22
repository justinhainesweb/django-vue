<template>
  <router-view />
</template>

<script>
  import axios from 'axios'
  import store from './store/Auth'

  export default {
    name: 'App',
    mounted () {

      const jwtToken = this.$store.state.jwt;
      if (jwtToken) {
        this.auth(jwtToken, true)
      } else {
        // redirect to Login page
        this.$router.replace({ name: 'main' })
      }
    },
    methods: {

      auth(jwtToken, initial = false) {
        // If token exists - will try to get current user
        axios.get('/auth/user/', {
          headers: {
            Authorization: `Bearer ${jwtToken}`,
            'Content-Type': 'application/json'
          }
        }).then(response => {
          store.commit('setAuthUser', response.data);
          if (initial) {
            this.$router.replace({ name: 'home' })
          }
        }).catch(error => {
          // 401 Unathorized - Signature has expired
          // console.log(error)
          if (initial) {
            this.refreshToken(jwtToken)
          }
        })
      },

      refreshToken(jwtToken) {
        axios.post(this.$store.state.endpoints.refreshJWT, {'token': jwtToken}).then((response) => {
          this.$store.commit('updateToken', response.data.token);
          this.$store.commit('setAuthUser', response.data);
          this.$router.replace({ name: 'home' });
        }).catch((error) => {
          this.$router.replace({ name: 'main' });
          console.log(error)
        })
      }
    }
  }
</script>

<style>
  @import '../node_modules/@fortawesome/fontawesome-free/css/all.min.css';
  @import '../node_modules/bootstrap/dist/css/bootstrap.min.css';
  @import '../node_modules/malihu-custom-scrollbar-plugin/jquery.mCustomScrollbar.css';
  @import '../assets/css/main.css';
</style>

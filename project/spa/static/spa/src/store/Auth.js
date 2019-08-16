import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  getters: {
    token: state => state.jwt
  },
  state: {
    authUser: localStorage.getItem('user'),
    jwt: localStorage.getItem('token'),
    endpoints: {
      signUp: process.env.HOST_ADDR + '/auth/users/',
      obtainJWT: process.env.HOST_ADDR + '/auth/jwt/obtain-token/',
      refreshJWT: process.env.HOST_ADDR + '/auth/jwt/refresh-token/'
    }
  },
  mutations: {

    setAuthUser (state, user) {
      localStorage.setItem('user', JSON.stringify(user))
      state.authUser = user
    },

    updateToken (state, newToken) {
      localStorage.setItem('token', newToken)
      state.jwt = newToken
    },

    removeToken (state) {
      localStorage.removeItem('token')
      state.jwt = null
    }
  }
})

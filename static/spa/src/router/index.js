/* eslint-disable */
import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/auth/Login'
import Register from '@/components/auth/Register'
import SPA from '@/components/todo/SPA'

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'main',
      component: Login
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/register',
      name: 'register',
      component: Register
    },
    {
      path: '/home',
      name: 'home',
      component: SPA
    }]
})

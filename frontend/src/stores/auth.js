import { defineStore } from 'pinia'
import { api } from '../lib/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('auth_token') || null,
    user: JSON.parse(localStorage.getItem('auth_user') || 'null'),
  }),
  actions: {
    setAuth(token, user = null) {
      this.token = token
      this.user = user
      localStorage.setItem('auth_token', token)
      localStorage.setItem('auth_user', JSON.stringify(user))
    },
    clearAuth() {
      this.token = null
      this.user = null
      localStorage.removeItem('auth_token')
      localStorage.removeItem('auth_user')
    },
    async fetchMe() {
      if (!this.token) return null
      const { data } = await api.get('/users/me')
      this.user = data
      localStorage.setItem('auth_user', JSON.stringify(data))
      return data
    },
  },
})

import { defineStore } from 'pinia'

import router from '@/router'
import { fetchWrapper } from '@/helpers/fetch-wrapper'
import i18n from '@/i18n'
import type { UserInfo } from '@/types'

const baseUrl = `${import.meta.env.VITE_API_URL}/auth`

export const useAuthStore = defineStore({
  id: 'auth',
  state: () => {
    // initialize state from local storage to enable user to stay logged in
    const userFromLocalStorage = localStorage.getItem('user')
    const user = userFromLocalStorage ? JSON.parse(userFromLocalStorage) : null

    return {
      user: user as UserInfo | null,
      error: null as string | null,
      returnUrl: null as string | null
    }
  },
  actions: {
    async login(username: string, password: string) {
      this.error = null

      const user = await fetchWrapper
        .post(`${baseUrl}/login/`, { username, password })
        .catch((err) => {
          this.error = err
          return null
        })

      if (user) {
        i18n.global.locale.value = user.locale
        this.user = user
        localStorage.setItem('user', JSON.stringify(user))
        router.push(this.returnUrl || '/')
      }
    },
    async logout() {
      await fetchWrapper.post(`${baseUrl}/logout/`).catch((err) => {
        this.error = err
        console.log('Error while logging out.')
        return null
      })
      this.user = null
      localStorage.removeItem('user')
      router.push('/log-in')
    },
    async getUser() {
      const user = await fetchWrapper.get(`${baseUrl}/user/`).catch((err) => {
        return null
      })

      this.user = user
      if (user) {
        i18n.global.locale.value = user.locale
      } else {
        localStorage.removeItem('user')
      }
    },
    async setLocale(locale: string) {
      this.error = null

      const user = await fetchWrapper.post(`${baseUrl}/user/`, { locale }).catch((err) => {
        this.error = err
        return null
      })

      if (user) {
        this.user = user
        i18n.global.locale.value = user.locale
      }
    }
  }
})

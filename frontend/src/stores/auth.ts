import { defineStore } from 'pinia'
import { ref } from 'vue'
import { authApi } from '../api/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const user = ref<any>(null)

  const login = async (username: string, password: string) => {
    const res: any = await authApi.login(username, password)
    token.value = res.access_token
    localStorage.setItem('token', res.access_token)
    await fetchUser()
  }

  const fetchUser = async () => {
    if (!token.value) return
    try {
      user.value = await authApi.getMe()
    } catch {
      logout()
    }
  }

  const logout = () => {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
  }

  if (token.value) {
    fetchUser()
  }

  return { token, user, login, logout, fetchUser }
})

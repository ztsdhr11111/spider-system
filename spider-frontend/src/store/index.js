// src/store/index.js
import { defineStore } from 'pinia'
import { spidersAPI, tasksAPI, authAPI } from '../api'

export const useMainStore = defineStore('main', {
  state: () => ({
    crawlers: [],
    tasks: [],
    token: localStorage.getItem('token') || null,
    user: null
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token
  },
  
  actions: {
    async fetchCrawlers(page = 1, size = 10) {
      try {
        const data = await spidersAPI.getSpiders(page, size)
        this.crawlers = data
        return { success: true, data }
      } catch (error) {
        console.error('Fetch crawlers error:', error)
        return { success: false, message: error.message }
      }
    },
    
    async fetchTasks(page = 1, size = 10) {
      try {
        const data = await tasksAPI.getTasks(page, size)
        this.tasks = data
        return { success: true, data }
      } catch (error) {
        console.error('Fetch tasks error:', error)
        return { success: false, message: error.message }
      }
    },
    
    setToken(token) {
      this.token = token
      localStorage.setItem('token', token)
    },
    
    clearToken() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
    },
    
    async login(username, password) {
      try {
        const response = await authAPI.login(username, password)
        this.setToken(response.access_token)
        this.user = response.user
        return { success: true, data: response }
      } catch (error) {
        return { success: false, message: error.message }
      }
    }
  }
})
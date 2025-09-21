// src/store/index.js
import { defineStore } from 'pinia'

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
    async fetchCrawlers() {
      try {
        const response = await fetch('/api/crawlers', {
          headers: {
            'Authorization': `Bearer ${this.token}`
          }
        })
        
        if (response.ok) {
          const data = await response.json()
          this.crawlers = data
        } else {
          throw new Error('获取爬虫列表失败')
        }
      } catch (error) {
        console.error('Fetch crawlers error:', error)
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
        const response = await fetch('/api/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ username, password })
        })
        
        const data = await response.json()
        
        if (response.ok) {
          this.setToken(data.access_token)
          this.user = data.user
          return { success: true, data }
        } else {
          return { success: false, message: data.message }
        }
      } catch (error) {
        return { success: false, message: '网络错误' }
      }
    }
  }
})
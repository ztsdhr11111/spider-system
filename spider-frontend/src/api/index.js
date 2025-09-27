// src/api/index.js
// API 入口文件
import * as authAPI from './auth'
import * as spidersAPI from './spiders'
import * as tasksAPI from './tasks'

export {
  authAPI,
  spidersAPI,
  tasksAPI
}

// API 基础配置
export const API_BASE_URL = 'http://127.0.0.1:5000/api'

// 通用请求函数
export async function request(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`
  
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers
    },
    ...options
  }
  
  // 如果有 token，自动添加到 Authorization 头部
  const token = localStorage.getItem('token')
  if (token && !config.headers.Authorization) {
    config.headers.Authorization = `Bearer ${token}`
  }
  
  try {
    const response = await fetch(url, config)
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      
      if (response.status === 401) {
        // Token 过期或无效，清除本地存储
        localStorage.removeItem('token')
        window.location.href = '/login'
        throw new Error('认证已过期，请重新登录')
      }
      
      throw new Error(errorData.message || `HTTP error! status: ${response.status}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error(`API request failed: ${error.message}`)
    throw error
  }
}
// src/api/auth.js
// 认证相关 API
import { request } from './index'

// 用户登录
export async function login(username, password) {
  return request('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ username, password })
  })
}

// 用户注册
export async function register(userData) {
  return request('/auth/register', {
    method: 'POST',
    body: JSON.stringify(userData)
  })
}

// 健康检查
export async function healthCheck() {
  return request('/auth/health')
}
// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { useMainStore } from '../store'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import SpiderManagement from '../views/SpiderManagement.vue'
import SystemDesign from '../views/SystemDesign.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/crawlers',
    name: 'SpiderManagement',
    component: SpiderManagement,
    meta: { requiresAuth: true }
  },
  {
    path: '/tasks',
    name: 'Tasks',
    component: SystemDesign, // 临时使用SystemDesign组件
    meta: { requiresAuth: true }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: SystemDesign, // 临时使用SystemDesign组件
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const store = useMainStore()
  
  if (to.meta.requiresAuth && !store.isAuthenticated) {
    next('/login')
  } else if (to.name === 'Login' && store.isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router
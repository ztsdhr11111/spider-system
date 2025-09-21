<!-- src/components/GlobalHeader.vue -->
<template>
  <el-header class="global-header">
    <div class="header-content">
      <div class="logo-section">
        <h2>🕷️ 爬虫管理系统</h2>
      </div>
      <el-menu :default-active="activeMenu" mode="horizontal" class="nav-menu" @select="handleMenuSelect">
        <el-menu-item index="/">首页</el-menu-item>
        <el-menu-item index="/crawlers">爬虫管理</el-menu-item>
        <el-menu-item index="/tasks">任务管理</el-menu-item>
        <el-menu-item index="/settings">系统设置</el-menu-item>
      </el-menu>
      <div class="user-actions">
        <el-dropdown @command="handleUserCommand">
          <span class="el-dropdown-link">
            <el-avatar :size="32" icon="User" />
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile">个人资料</el-dropdown-item>
              <el-dropdown-item command="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>
  </el-header>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router'
import { useMainStore } from '../store'
import { computed } from 'vue'

const router = useRouter()
const route = useRoute()
const store = useMainStore()

// 计算当前激活的菜单项
const activeMenu = computed(() => {
  if (route.path.startsWith('/crawlers')) return '/crawlers'
  if (route.path.startsWith('/tasks')) return '/tasks'
  if (route.path.startsWith('/settings')) return '/settings'
  return route.path
})

const handleMenuSelect = (index) => {
  router.push(index)
}

const handleUserCommand = (command) => {
  if (command === 'logout') {
    store.clearToken()
    router.push('/login')
  } else if (command === 'profile') {
    // 跳转到个人资料页面
    console.log('查看个人资料')
  }
}
</script>

<style scoped>
.global-header {
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 0;
  /* 移除固定高度，让内容自适应 */
}

.header-content {
  display: flex;
  align-items: center;
  /* 设置合适的最大宽度并居中 */
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
  height: 60px;
}

.logo-section {
  padding: 0 20px;
  border-right: 1px solid #ebeef5;
  white-space: nowrap;
}

.logo-section h2 {
  margin: 0;
  color: #409eff;
}

.nav-menu {
  flex: 1;
  border: none;
  /* 调整菜单项间距 */
}

.nav-menu :deep(.el-menu-item) {
  padding: 0 20px;
}

.user-actions {
  padding: 0 20px;
  border-left: 1px solid #ebeef5;
}

/* 响应式设计 */
@media (min-width: 1200px) {
  .header-content {
    max-width: 1600px;
  }
}

@media (min-width: 1600px) {
  .header-content {
    max-width: 1800px;
  }
}
</style>
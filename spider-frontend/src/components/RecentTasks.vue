<!-- src/components/RecentTasks.vue -->
<template>
  <el-card class="recent-tasks">
    <template #header>
      <div class="card-header">
        <span>最近任务</span>
      </div>
    </template>
    <ul v-if="loading" class="task-list">
      <li class="task-item">加载中...</li>
    </ul>
    <ul v-else-if="error" class="task-list">
      <li class="task-item" style="color: #f56c6c;">{{ error }}</li>
    </ul>
    <ul v-else class="task-list">
      <li v-for="task in tasks" :key="task._id" class="task-item">
        <div class="task-info">
          <p class="task-name">{{ task.name || '未命名任务' }}</p>
          <p class="task-time">{{ formatTime(task.start_time) }}</p>
        </div>
        <el-tag :type="getTaskStatusType(task.status)">{{ task.status || '未知' }}</el-tag>
      </li>
    </ul>
  </el-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getTaskRuns } from '../api/tasks'

// 定义响应式数据
const tasks = ref([])
const loading = ref(true)
const error = ref(null)

// 获取最近任务
const fetchRecentTasks = async () => {
  try {
    // 调用API获取任务执行记录，按时间倒序排列，取前5条
    const response = await getTaskRuns({ size: 5 })
    tasks.value = response.data || response || []
  } catch (err) {
    error.value = '获取任务列表失败，请刷新重试'
    console.error('Failed to fetch recent tasks:', err)
  } finally {
    loading.value = false
  }
}

// 格式化时间显示
const formatTime = (timeString) => {
  if (!timeString) return '未知时间'
  return new Date(timeString).toLocaleString('zh-CN')
}

// 根据任务状态返回标签类型
const getTaskStatusType = (status) => {
  switch (status) {
    case 'success':
      return 'success'
    case 'running':
      return 'warning'
    case 'failed':
      return 'danger'
    default:
      return 'info'
  }
}

// 组件挂载后获取数据
onMounted(() => {
  fetchRecentTasks()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.task-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.task-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #ebeef5;
}

.task-item:last-child {
  border-bottom: none;
}

.task-name {
  margin: 0;
  font-weight: 500;
}

.task-time {
  margin: 5px 0 0 0;
  font-size: 0.9rem;
  color: #909399;
}
</style>
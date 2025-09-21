<!-- src/components/RecentTasks.vue -->
<template>
  <el-card class="recent-tasks">
    <template #header>
      <div class="card-header">
        <span>最近任务</span>
      </div>
    </template>
    <ul class="task-list">
      <li v-for="task in 5" :key="task" class="task-item">
        <div class="task-info">
          <p class="task-name">新闻网站爬虫任务 #{{ task }}</p>
          <p class="task-time">2023-06-{{ 10 + task }} 14:{{ 30 + task }}:{{ 15 + task }}</p>
        </div>
        <el-tag type="success">成功</el-tag>
      </li>
    </ul>
  </el-card>
</template>

<script setup>
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
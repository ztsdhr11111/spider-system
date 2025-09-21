<!-- src/components/SystemStatus.vue -->
<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <span>系统状态</span>
      </div>
    </template>
    <div class="system-status">
      <div class="status-item">
        <span>CPU 使用率</span>
        <el-progress :percentage="45" :stroke-width="10" />
      </div>
      <div class="status-item">
        <span>内存使用率</span>
        <el-progress :percentage="68" :stroke-width="10" status="warning" />
      </div>
      <div class="status-item">
        <span>存储空间</span>
        <el-progress :percentage="25" :stroke-width="10" status="success" />
      </div>
    </div>
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

.system-status .status-item {
  margin-bottom: 20px;
}

.system-status .status-item:last-child {
  margin-bottom: 0;
}

.system-status .status-item > span {
  display: block;
  margin-bottom: 8px;
  color: #606266;
}
</style>
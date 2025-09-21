<!-- src/components/SystemStats.vue -->
<script setup>
import { useMainStore } from '../store'

const store = useMainStore()
</script>

<template>
  <el-row :gutter="20" class="stats-row">
    <el-col :span="6">
      <el-card class="stat-card">
        <div class="stat-content">
          <h3>{{ store.crawlers.length }}</h3>
          <p>爬虫总数</p>
        </div>
      </el-card>
    </el-col>
    <el-col :span="6">
      <el-card class="stat-card">
        <div class="stat-content">
          <h3>24</h3>
          <p>运行中任务</p>
        </div>
      </el-card>
    </el-col>
    <el-col :span="6">
      <el-card class="stat-card">
        <div class="stat-content">
          <h3>156</h3>
          <p>今日数据量</p>
        </div>
      </el-card>
    </el-col>
    <el-col :span="6">
      <el-card class="stat-card">
        <div class="stat-content">
          <h3>98%</h3>
          <p>成功率</p>
        </div>
      </el-card>
    </el-col>
  </el-row>
</template>

<style scoped>
.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  text-align: center;
}

.stat-content h3 {
  font-size: 2rem;
  margin: 10px 0;
  color: #409eff;
}

.stat-content p {
  margin: 0;
  color: #909399;
}
</style>
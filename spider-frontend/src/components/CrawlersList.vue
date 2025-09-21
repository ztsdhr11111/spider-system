<!-- src/components/CrawlersList.vue -->
<script setup>
defineProps({
  crawlers: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['createCrawler', 'startCrawler', 'viewDetails'])
</script>

<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <span>爬虫列表</span>
        <el-button type="primary" size="small" @click="emit('createCrawler')">
          创建爬虫
        </el-button>
      </div>
    </template>
    <el-table :data="crawlers" style="width: 100%">
      <el-table-column prop="name" label="爬虫名称" width="180" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="scope">
          <el-tag :type="scope.row.status === '运行中' ? 'success' : 'info'">
            {{ scope.row.status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="type" label="类型" width="120" />
      <el-table-column prop="lastRun" label="最后运行" width="180" />
      <el-table-column prop="dataCount" label="数据量" />
      <el-table-column label="操作" width="150">
        <template #default="scope">
          <el-button 
            size="small" 
            type="primary" 
            @click="emit('startCrawler', scope.row)"
          >
            启动
          </el-button>
          <el-button 
            size="small" 
            @click="emit('viewDetails', scope.row)"
          >
            详情
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
<!-- src/components/CrawlersList.vue -->
<script setup>
import { useRouter } from 'vue-router'

const props = defineProps({
  crawlers: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['createCrawler', 'startCrawler', 'viewDetails'])

const router = useRouter()

// 跳转到爬虫管理页面
const goToSpiderManagement = () => {
  router.push('/crawlers')
}
</script>

<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <span>爬虫列表</span>
        <div>
          <el-button type="primary" size="small" @click="emit('createCrawler')">
            创建爬虫
          </el-button>
          <el-button type="text" size="small" @click="goToSpiderManagement" style="margin-left: 10px;">
            查看全部
          </el-button>
        </div>
      </div>
    </template>
    <el-table :data="crawlers" style="width: 100%">
      <el-table-column prop="name" label="爬虫名称" width="180" />
      <el-table-column prop="category" label="分类" width="120" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="scope">
          <el-tag :type="scope.row.status === '运行中' ? 'success' : 'info'">
            {{ scope.row.status || '未知' }}
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
    
    <div v-if="crawlers.length === 0" class="empty-placeholder">
      <p>暂无爬虫数据</p>
      <el-button type="primary" @click="emit('createCrawler')">创建第一个爬虫</el-button>
    </div>
  </el-card>
</template>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.empty-placeholder {
  text-align: center;
  padding: 40px 0;
  color: #909399;
}

.empty-placeholder p {
  margin-bottom: 20px;
}
</style>
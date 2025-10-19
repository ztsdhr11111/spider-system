<!-- src/views/Dashboard.vue -->
<script setup>
import { useRouter } from 'vue-router'
import GlobalHeader from '../components/GlobalHeader.vue'
import { useMainStore } from '../store'
import CrawlersList from '../components/CrawlersList.vue'
import SystemStats from '../components/SystemStats.vue'
import RecentTasks from '../components/RecentTasks.vue'
import SystemStatus from '../components/SystemStatus.vue'
import { onMounted } from 'vue'

const store = useMainStore()
const router = useRouter()

// 处理爬虫相关事件
const handleCreateCrawler = () => {
  router.push('/crawlers')
}

const handleStartCrawler = (crawler) => {
  console.log('启动爬虫:', crawler)
  // 这里可以实现启动爬虫的逻辑
}

const handleViewDetails = (crawler) => {
  router.push('/crawlers')
}

onMounted(() => {
  store.fetchCrawlers()
})
</script>

<template>
  <div>
    <GlobalHeader />
    
    <el-card class="page-card">
      <div class="dashboard-content">
        <SystemStats />
        
        <el-row :gutter="20" class="content-row">
          <el-col :span="16">
            <CrawlersList 
              :crawlers="store.crawlers" 
              @create-crawler="handleCreateCrawler"
              @start-crawler="handleStartCrawler"
              @view-details="handleViewDetails"
            />
          </el-col>
          
          <el-col :span="8">
            <RecentTasks />
            <SystemStatus style="margin-top: 20px;" />
          </el-col>
        </el-row>
      </div>
    </el-card>
  </div>
</template>

<style scoped>

.page-card {
  margin-bottom: 20px;
}

.dashboard-header {
  text-align: center;
  margin-bottom: 30px;
  padding: 20px 0;
}

.dashboard-header h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
  color: #303133;
}

.dashboard-header p {
  font-size: 1.1rem;
  color: #606266;
}

.content-row {
  margin-top: 20px;
}
</style>
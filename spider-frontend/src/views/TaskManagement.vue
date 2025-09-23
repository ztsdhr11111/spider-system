<!-- src/views/TaskManagement.vue -->
<template>
  <div class="task-management">
    <GlobalHeader />
    
    <el-card class="mb-4">
      <template #header>
        <div class="card-header">
          <span>任务列表</span>
          <div class="header-actions">
            <el-button type="primary" @click="showCreateDialog = true">创建任务</el-button>
            <el-button @click="refreshTasks">刷新</el-button>
          </div>
        </div>
      </template>
      
      <!-- 任务筛选 -->
      <div class="filter-section mb-3">
        <el-form :inline="true" :model="filterForm" class="filter-form">
          <el-form-item label="任务名称">
            <el-input v-model="filterForm.name" placeholder="任务名称" clearable />
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="filterForm.status" placeholder="任务状态" clearable>
              <el-option label="全部" value=""></el-option>
              <el-option label="待执行" value="pending"></el-option>
              <el-option label="执行中" value="running"></el-option>
              <el-option label="已完成" value="completed"></el-option>
              <el-option label="已失败" value="failed"></el-option>
              <el-option label="已取消" value="cancelled"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="爬虫">
            <el-select v-model="filterForm.spider_id" placeholder="选择爬虫" clearable>
              <el-option 
                v-for="spider in allSpiders" 
                :key="spider._id" 
                :label="spider.name" 
                :value="spider._id" 
              />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="fetchTasks">搜索</el-button>
            <el-button @click="resetFilter">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
      
      <!-- 任务表格 -->
      <el-table :data="tasks" style="width: 100%" v-loading="loading" stripe>
        <el-table-column prop="name" label="任务名称" width="180" show-overflow-tooltip />
        <el-table-column prop="spider_name" label="爬虫名称" width="150" show-overflow-tooltip />
        <el-table-column label="执行时间" width="180">
          <template #default="scope">
            <div>
              <div>开始: {{ scope.row.scheduled_time ? formatDate(scope.row.scheduled_time) : '-' }}</div>
              <div v-if="scope.row.start_time">执行: {{ formatDate(scope.row.start_time) }}</div>
              <div v-if="scope.row.end_time">结束: {{ formatDate(scope.row.end_time) }}</div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getTaskStatusType(scope.row.status)">
              {{ getTaskStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="cron_expression" label="调度规则" width="120" show-overflow-tooltip />
        <el-table-column label="创建时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button size="small" type="primary" @click="executeTask(scope.row._id)" 
                       :disabled="scope.row.status === 'running'">
              执行
            </el-button>
            <el-button size="small" @click="editTask(scope.row)">编辑</el-button>
            <el-dropdown @command="(command) => handleTaskAction(command, scope.row)">
              <el-button size="small">
                更多<i class="el-icon-arrow-down el-icon--right"></i>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="viewRuns">执行记录</el-dropdown-item>
                  <el-dropdown-item command="toggle" v-if="scope.row.enabled">
                    禁用
                  </el-dropdown-item>
                  <el-dropdown-item command="toggle" v-else>
                    启用
                  </el-dropdown-item>
                  <el-dropdown-item command="delete" divided style="color: #f56c6c;">
                    删除
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination-container" v-if="total > pageSize">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total">
        </el-pagination>
      </div>
    </el-card>
    
    <!-- 创建/编辑任务对话框 -->
    <el-dialog 
      v-model="showCreateDialog" 
      :title="editingTask ? '编辑任务' : '创建任务'"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form 
        :model="taskForm" 
        :rules="taskRules" 
        ref="taskFormRef"
        label-width="120px"
      >
        <el-form-item label="任务名称" prop="name">
          <el-input v-model="taskForm.name" placeholder="请输入任务名称"></el-input>
        </el-form-item>
        <el-form-item label="关联爬虫" prop="spider_id">
          <el-select v-model="taskForm.spider_id" placeholder="请选择爬虫" style="width: 100%">
            <el-option 
              v-for="spider in allSpiders" 
              :key="spider._id" 
              :label="spider.name" 
              :value="spider._id" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="调度类型" prop="schedule_type">
          <el-radio-group v-model="taskForm.schedule_type">
            <el-radio label="manual">手动执行</el-radio>
            <el-radio label="scheduled">定时调度</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item 
          label="调度规则" 
          prop="cron_expression" 
          v-if="taskForm.schedule_type === 'scheduled'">
          <el-input v-model="taskForm.cron_expression" placeholder="请输入Cron表达式"></el-input>
          <div class="cron-help">
            <el-link type="primary" @click="showCronHelp = true">Cron表达式帮助</el-link>
          </div>
        </el-form-item>
        <el-form-item label="任务参数" prop="parameters">
          <el-input 
            v-model="taskForm.parameters" 
            type="textarea" 
            :rows="3"
            placeholder='请输入JSON格式参数，例如: {"category": "tech", "limit": 100}'
          ></el-input>
        </el-form-item>
        <el-form-item label="启用" prop="enabled">
          <el-switch v-model="taskForm.enabled"></el-switch>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input 
            v-model="taskForm.description" 
            type="textarea" 
            :rows="3"
            placeholder="请输入任务描述"
          ></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showCreateDialog = false">取消</el-button>
          <el-button type="primary" @click="saveTask" :loading="saving">保存</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- Cron表达式帮助对话框 -->
    <el-dialog v-model="showCronHelp" title="Cron表达式帮助" width="600px">
      <div class="cron-help-content">
        <p>Cron表达式由5个字段组成，用空格分隔：</p>
        <el-table :data="cronExamples" border>
          <el-table-column prop="expression" label="表达式" width="150"></el-table-column>
          <el-table-column prop="description" label="说明"></el-table-column>
        </el-table>
        <div class="mt-3">
          <p>字段含义：</p>
          <ul>
            <li>分钟 (0-59)</li>
            <li>小时 (0-23)</li>
            <li>日期 (1-31)</li>
            <li>月份 (1-12)</li>
            <li>星期 (0-7, 0和7都表示星期日)</li>
          </ul>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showCronHelp = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useMainStore } from '../store'
import GlobalHeader from '../components/GlobalHeader.vue'

const store = useMainStore()
const tasks = ref([])
const allSpiders = ref([])
const loading = ref(false)
const saving = ref(false)
const showCreateDialog = ref(false)
const showCronHelp = ref(false)
const editingTask = ref(null)
const taskFormRef = ref()

// 分页相关
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 表单数据
const taskForm = reactive({
  name: '',
  spider_id: '',
  schedule_type: 'manual',
  cron_expression: '',
  parameters: '',
  enabled: true,
  description: ''
})

// 筛选表单
const filterForm = reactive({
  name: '',
  status: '',
  spider_id: ''
})

// 表单验证规则
const taskRules = {
  name: [
    { required: true, message: '请输入任务名称', trigger: 'blur' }
  ],
  spider_id: [
    { required: true, message: '请选择爬虫', trigger: 'change' }
  ],
  cron_expression: [
    { required: true, message: '请输入Cron表达式', trigger: 'blur' }
  ]
}

// Cron表达式示例
const cronExamples = [
  { expression: '0 0 * * *', description: '每天凌晨执行' },
  { expression: '0 12 * * *', description: '每天中午12点执行' },
  { expression: '0 0 * * 0', description: '每周日执行' },
  { expression: '0 0 1 * *', description: '每月1号执行' },
  { expression: '*/30 * * * *', description: '每30分钟执行一次' }
]

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

// 获取任务状态标签类型
const getTaskStatusType = (status) => {
  switch (status) {
    case 'pending': return 'info'
    case 'running': return 'warning'
    case 'completed': return 'success'
    case 'failed': return 'danger'
    case 'cancelled': return 'info'
    default: return 'info'
  }
}

// 获取任务状态文本
const getTaskStatusText = (status) => {
  switch (status) {
    case 'pending': return '待执行'
    case 'running': return '执行中'
    case 'completed': return '已完成'
    case 'failed': return '已失败'
    case 'cancelled': return '已取消'
    default: return status
  }
}

// 获取所有爬虫
const fetchAllSpiders = async () => {
  try {
    const response = await fetch('/api/spiders', {
      headers: {
        'Authorization': `Bearer ${store.token}`
      }
    })
    if (response.ok) {
      const data = await response.json()
      allSpiders.value = data.spiders || data
    }
  } catch (error) {
    ElMessage.error('获取爬虫列表失败: ' + error.message)
  }
}

// 获取任务列表
const fetchTasks = async () => {
  loading.value = true
  try {
    const params = new URLSearchParams({
      page: currentPage.value,
      size: pageSize.value,
      name: filterForm.name,
      status: filterForm.status,
      spider_id: filterForm.spider_id
    })
    
    const response = await fetch(`/api/tasks?${params}`, {
      headers: {
        'Authorization': `Bearer ${store.token}`
      }
    })
    
    if (response.ok) {
      const data = await response.json()
      tasks.value = data.tasks || data
      total.value = data.total || data.length
    } else {
      throw new Error('获取任务列表失败')
    }
  } catch (error) {
    ElMessage.error('获取任务列表失败: ' + error.message)
  } finally {
    loading.value = false
  }
}

// 刷新任务列表
const refreshTasks = () => {
  currentPage.value = 1
  fetchTasks()
}

// 重置筛选条件
const resetFilter = () => {
  filterForm.name = ''
  filterForm.status = ''
  filterForm.spider_id = ''
  refreshTasks()
}

// 编辑任务
const editTask = (task) => {
  editingTask.value = task
  taskForm.name = task.name
  taskForm.spider_id = task.spider_id
  taskForm.schedule_type = task.schedule_type
  taskForm.cron_expression = task.cron_expression || ''
  taskForm.parameters = task.parameters || ''
  taskForm.enabled = task.enabled
  taskForm.description = task.description || ''
  showCreateDialog.value = true
}

// 保存任务
const saveTask = async () => {
  if (!taskFormRef.value) return
  
  await taskFormRef.value.validate(async (valid) => {
    if (valid) {
      saving.value = true
      try {
        const url = editingTask.value 
          ? `/api/tasks/${editingTask.value._id}` 
          : '/api/tasks'
        const method = editingTask.value ? 'PUT' : 'POST'
        
        const response = await fetch(url, {
          method,
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${store.token}`
          },
          body: JSON.stringify(taskForm)
        })
        
        const data = await response.json()
        
        if (response.ok) {
          ElMessage.success(editingTask.value ? '更新成功' : '创建成功')
          showCreateDialog.value = false
          refreshTasks()
        } else {
          ElMessage.error(data.message || '保存失败')
        }
      } catch (error) {
        ElMessage.error('保存失败: ' + error.message)
      } finally {
        saving.value = false
      }
    }
  })
}

// 执行任务
const executeTask = async (taskId) => {
  try {
    const response = await fetch(`/api/tasks/${taskId}/execute`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${store.token}`
      }
    })
    
    if (response.ok) {
      ElMessage.success('任务开始执行')
      refreshTasks()
    } else {
      const data = await response.json()
      ElMessage.error(data.message || '执行任务失败')
    }
  } catch (error) {
    ElMessage.error('执行任务失败: ' + error.message)
  }
}

// 处理任务操作
const handleTaskAction = (command, task) => {
  switch (command) {
    case 'viewRuns':
      // 查看执行记录
      break
    case 'toggle':
      toggleTaskStatus(task)
      break
    case 'delete':
      deleteTask(task._id)
      break
  }
}

// 切换任务状态
const toggleTaskStatus = async (task) => {
  try {
    const response = await fetch(`/api/tasks/${task._id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${store.token}`
      },
      body: JSON.stringify({
        enabled: !task.enabled
      })
    })
    
    if (response.ok) {
      ElMessage.success(`${task.enabled ? '禁用' : '启用'}成功`)
      refreshTasks()
    } else {
      ElMessage.error(`${task.enabled ? '禁用' : '启用'}失败`)
    }
  } catch (error) {
    ElMessage.error(`${task.enabled ? '禁用' : '启用'}失败: ` + error.message)
  }
}

// 删除任务
const deleteTask = async (taskId) => {
  ElMessageBox.confirm('确定要删除这个任务吗？此操作不可恢复', '确认删除', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      const response = await fetch(`/api/tasks/${taskId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${store.token}`
        }
      })
      
      if (response.ok) {
        ElMessage.success('删除成功')
        refreshTasks()
      } else {
        const data = await response.json()
        ElMessage.error(data.message || '删除失败')
      }
    } catch (error) {
      ElMessage.error('删除失败: ' + error.message)
    }
  }).catch(() => {
    // 用户取消删除
  })
}

// 分页处理
const handleSizeChange = (val) => {
  pageSize.value = val
  currentPage.value = 1
  fetchTasks()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchTasks()
}

onMounted(() => {
  fetchAllSpiders()
  fetchTasks()
})
</script>

<style scoped>
.task-management {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 20px;
}

@media (min-width: 1200px) {
  .task-management {
    max-width: 1400px;
    margin: 0 auto;
  }
}

@media (min-width: 1600px) {
  .task-management {
    max-width: 1600px;
  }
}

.mb-4 {
  margin-bottom: 1rem;
}

.mb-3 {
  margin-bottom: 0.75rem;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.filter-section {
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 4px;
  margin-bottom: 20px;
}

.filter-form {
  margin-bottom: 0;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.cron-help {
  margin-top: 5px;
}

.cron-help-content ul {
  padding-left: 20px;
}

.mt-3 {
  margin-top: 1rem;
}
</style>
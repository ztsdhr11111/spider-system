<template>
  <div class="page-container">
    <!-- 添加全局头部 -->
    <GlobalHeader />
    <el-card class="page-card">
    <template #header>
        <div class="card-header">
          <span>爬虫列表</span>
          <div>
            <el-select v-model="selectedCategory" placeholder="请选择分类" @change="fetchSpiders" clearable style="margin-right: 10px;">
              <el-option
                v-for="category in categories"
                :key="category"
                :label="category"
                :value="category">
              </el-option>
            </el-select>
            <el-button type="primary" @click="showCreateSpiderDialog">创建爬虫</el-button>
          </div>
        </div>
      </template>
      
      <el-table :data="spiders" style="width: 100%" v-loading="loading" stripe>
        <el-table-column prop="name" label="名称" width="180">
          <template #default="scope">
            <el-link type="primary" @click="viewSpiderDetails(scope.row)">{{ scope.row.name }}</el-link>
          </template>
        </el-table-column>
        <el-table-column prop="category" label="分类" width="120"></el-table-column>
        <el-table-column prop="description" label="描述" show-overflow-tooltip></el-table-column>
        <el-table-column prop="script_path" label="脚本路径" width="250" show-overflow-tooltip></el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.enabled ? 'success' : 'danger'">
              {{ scope.row.enabled ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="创建时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="250" fixed="right">
          <template #default="scope">
            <el-button size="small" type="primary" @click="runSpider(scope.row._id)" :loading="runningSpiders.has(scope.row._id)">
              {{ runningSpiders.has(scope.row._id) ? '运行中...' : '运行' }}
            </el-button>
            <el-button size="small" @click="editSpider(scope.row)">编辑</el-button>
            <el-dropdown @command="(command) => handleSpiderAction(command, scope.row)">
              <el-button size="small">
                更多<i class="el-icon-arrow-down el-icon--right"></i>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="toggle">
                    {{ scope.row.enabled ? '禁用' : '启用' }}
                  </el-dropdown-item>
                  <el-dropdown-item command="viewRuns">运行记录</el-dropdown-item>
                  <el-dropdown-item command="delete" divided style="color: #f56c6c;">
                    删除
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
        </el-table-column>
      </el-table>
      
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
    
    <!-- 创建/编辑爬虫对话框 -->
    <el-dialog v-model="showCreateDialog" :title="editingSpider ? '编辑爬虫' : '创建爬虫'" width="600px">
      <el-form :model="spiderForm" :rules="spiderRules" ref="spiderFormRef" label-width="100px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="spiderForm.name"></el-input>
        </el-form-item>
        <!-- 创建/编辑爬虫对话框中的分类选择部分 -->
        <el-form-item label="分类" prop="category">
          <el-select 
            v-model="spiderForm.category" 
            placeholder="请选择或输入分类" 
            style="width: 100%;"
            filterable
            allow-create
            default-first-option>
            <el-option
              v-for="category in categories"
              :key="category"
              :label="category"
              :value="category">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="spiderForm.description" type="textarea"></el-input>
        </el-form-item>
        <el-form-item label="脚本路径" prop="script_path">
          <el-input v-model="spiderForm.script_path"></el-input>
        </el-form-item>
        <el-form-item label="主模块" prop="main_module">
          <el-input v-model="spiderForm.main_module"></el-input>
        </el-form-item>
        <el-form-item label="启用" prop="enabled">
          <el-switch v-model="spiderForm.enabled"></el-switch>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showCreateDialog = false">取消</el-button>
          <el-button type="primary" @click="saveSpider" :loading="saving">保存</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 爬虫详情对话框 -->
    <el-dialog 
      v-model="showDetailDialog" 
      :title="detailSpider?.name + ' - 详情'"
      width="600px"
    >
      <el-descriptions :column="1" border>
        <el-descriptions-item label="名称">{{ detailSpider?.name }}</el-descriptions-item>
        <el-descriptions-item label="分类">{{ detailSpider?.category }}</el-descriptions-item>
        <el-descriptions-item label="描述">{{ detailSpider?.description }}</el-descriptions-item>
        <el-descriptions-item label="脚本路径">{{ detailSpider?.script_path }}</el-descriptions-item>
        <el-descriptions-item label="主模块">{{ detailSpider?.main_module }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="detailSpider?.enabled ? 'success' : 'danger'">
            {{ detailSpider?.enabled ? '启用' : '禁用' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="创建时间">
          {{ formatDate(detailSpider?.created_at) }}
        </el-descriptions-item>
        <el-descriptions-item label="更新时间">
          {{ formatDate(detailSpider?.updated_at) }}
        </el-descriptions-item>
      </el-descriptions>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showDetailDialog = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 运行记录对话框 -->
    <el-dialog 
      v-model="showRunsDialog" 
      :title="runsSpider?.name + ' - 运行记录'"
      width="800px"
    >
      <el-table :data="spiderRuns" style="width: 100%" v-loading="runsLoading" max-height="400">
        <el-table-column prop="start_time" label="开始时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.start_time) }}
          </template>
        </el-table-column>
        <el-table-column prop="end_time" label="结束时间" width="180">
          <template #default="scope">
            {{ scope.row.end_time ? formatDate(scope.row.end_time) : '-' }}
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getRunStatusType(scope.row.status)">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100">
          <template #default="scope">
            <el-button size="small" @click="viewRunDetail(scope.row)">详情</el-button>
          </template>
        </el-table-column>
      </el-table>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showRunsDialog = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
    
    
    <el-dialog 
      v-model="showRunDetailDialog" 
      title="运行详情"
      width="700px"
    >
    <!--  
      <el-tabs v-model="activeRunTab">
        <el-tab-pane label="输出日志" name="output">
          <el-input 
            type="textarea" 
            :rows="10" 
            v-model="currentRunDetail?.log_output" 
            readonly
            class="log-textarea"
          ></el-input>
        </el-tab-pane>
        <el-tab-pane label="错误信息" name="error">
          <el-input 
            type="textarea" 
            :rows="10" 
            v-model="currentRunDetail?.error_message" 
            readonly
            class="log-textarea"
          ></el-input>
        </el-tab-pane>
      </el-tabs>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showRunDetailDialog = false">关闭</el-button>
        </span>
      </template>
      -->
    </el-dialog> 
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useMainStore } from '../store'
// 添加 GlobalHeader 组件的导入
import GlobalHeader from '../components/GlobalHeader.vue'
// 导入 spidersAPI
import { spidersAPI } from '../api'

const store = useMainStore()
const spiders = ref([])
const categories = ref([])
const selectedCategory = ref('')
const loading = ref(false)
const saving = ref(false)
const showCreateDialog = ref(false)
const showDetailDialog = ref(false)
const showRunsDialog = ref(false)
const showRunDetailDialog = ref(false)
const editingSpider = ref(null)
const detailSpider = ref(null)
const runsSpider = ref(null)
const spiderRuns = ref([])
const runsLoading = ref(false)
const currentRunDetail = ref(null)
const activeRunTab = ref('output')
const runningSpiders = ref(new Set())

// 分页相关
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const spiderFormRef = ref()

const spiderForm = reactive({
  name: '',
  category: 'default',
  description: '',
  script_path: '',
  main_module: 'main.py',
  enabled: true
})

const spiderRules = {
  name: [
    { required: true, message: '请输入爬虫名称', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择分类', trigger: 'change' }
  ],
  description: [
    { required: true, message: '请输入爬虫描述', trigger: 'blur' }
  ],
  script_path: [
    { required: true, message: '请输入脚本路径', trigger: 'blur' }
  ],
  main_module: [
    { required: true, message: '请输入主模块文件名', trigger: 'blur' }
  ]
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

// 获取运行状态标签类型
const getRunStatusType = (status) => {
  switch (status) {
    case 'success': return 'success'
    case 'failed': return 'danger'
    case 'running': return 'warning'
    default: return 'info'
  }
}

// 获取爬虫列表
const fetchSpiders = async () => {
  loading.value = true
  try {
    const filters = {}
    
    if (selectedCategory.value) {
      filters.category = selectedCategory.value
    }
    
    const response = await spidersAPI.getSpiders(currentPage.value, pageSize.value, filters)
    spiders.value = response.data || response
    // 如果total信息在响应中，更新total值
    if (response.total !== undefined) {
      total.value = response.total
    }
  } catch (error) {
    ElMessage.error('获取爬虫列表失败: ' + error.message)
  } finally {
    loading.value = false
  }
}

// 获取所有分类
const fetchCategories = async () => {
  try {
    const response = await spidersAPI.getSpiderCategories()
    categories.value = response.data?.categories || response.categories || []
  } catch (error) {
    ElMessage.error('获取分类列表失败: ' + error.message)
  }
}

// 显示创建爬虫对话框
const showCreateSpiderDialog = () => {
  editingSpider.value = null  // 重置编辑状态
  // 重置表单数据
  spiderForm.name = ''
  spiderForm.category = 'default'
  spiderForm.description = ''
  spiderForm.script_path = ''
  spiderForm.main_module = 'main.py'
  spiderForm.enabled = true
  showCreateDialog.value = true
}

// 保存爬虫
const saveSpider = async () => {
  spiderFormRef.value.validate(async (valid) => {
    if (!valid) return
  
    try {
      saving.value = true
      let response
      
      if (editingSpider.value) {
        // 更新爬虫
        response = await spidersAPI.updateSpider(editingSpider.value._id, spiderForm)
        ElMessage.success('爬虫更新成功')
      } else {
        // 创建爬虫
        response = await spidersAPI.createSpider(spiderForm)
        ElMessage.success('爬虫创建成功')
      }
      
      showCreateDialog.value = false
      fetchSpiders()
      fetchCategories() // 重新获取分类列表，可能有新分类
    } catch (error) {
      ElMessage.error((editingSpider.value ? '更新' : '创建') + '爬虫失败: ' + error.message)
    } finally {
      saving.value = false
    }
  })
}

// 运行爬虫
const runSpider = async (spiderId) => {
  // 防止重复点击
  if (runningSpiders.value.has(spiderId)) return
  
  try {
    runningSpiders.value.add(spiderId)
    
    const response = await spidersAPI.runSpider(spiderId)
    
    ElMessage.success('爬虫开始运行')
    // 可以轮询获取运行结果
    setTimeout(() => {
      fetchSpiders()
      if (showRunsDialog.value && runsSpider.value?._id === spiderId) {
        fetchSpiderRuns(runsSpider.value._id)
      }
    }, 3000)
  } catch (error) {
    ElMessage.error('运行爬虫失败: ' + error.message)
  } finally {
    runningSpiders.value.delete(spiderId)
  }
}

// 查看爬虫详情
const viewSpiderDetails = (spider) => {
  detailSpider.value = spider
  showDetailDialog.value = true
}

// 编辑爬虫
const editSpider = (spider) => {
  console.log('编辑爬虫:', spider)
  editingSpider.value = spider
  spiderForm.name = spider.name
  spiderForm.category = spider.category || 'default'
  spiderForm.description = spider.description
  spiderForm.script_path = spider.script_path
  spiderForm.main_module = spider.main_module
  spiderForm.enabled = spider.enabled
  showCreateDialog.value = true
}

// 处理爬虫操作
const handleSpiderAction = (command, spider) => {
  switch (command) {
    case 'toggle':
      toggleSpiderStatus(spider)
      break
    case 'viewRuns':
      viewSpiderRuns(spider)
      break
    case 'delete':
      deleteSpider(spider._id)
      break
  }
}

// 切换爬虫状态
const toggleSpiderStatus = async (spider) => {
  try {
    // 先获取当前爬虫的完整信息
    const currentSpider = await spidersAPI.getSpider(spider._id)
    // 更新启用状态
    const updatedData = { ...currentSpider, enabled: !spider.enabled }
    await spidersAPI.updateSpider(spider._id, updatedData)
    
    ElMessage.success(`${spider.enabled ? '禁用' : '启用'}成功`)
    fetchSpiders()
  } catch (error) {
    ElMessage.error(`${spider.enabled ? '禁用' : '启用'}失败: ` + error.message)
  }
}

// 查看运行记录
const viewSpiderRuns = async (spider) => {
  runsSpider.value = spider
  showRunsDialog.value = true
  await fetchSpiderRuns(spider._id)
}

// 获取爬虫运行记录
const fetchSpiderRuns = async (spiderId) => {
  runsLoading.value = true
  try {
    spiderRuns.value = await spidersAPI.getSpiderRuns(spiderId)
  } catch (error) {
    ElMessage.error('获取运行记录失败: ' + error.message)
  } finally {
    runsLoading.value = false
  }
}

// 查看运行详情
const viewRunDetail = (run) => {
  console.log('查看运行详情:', run)
  currentRunDetail.value = run
  showRunDetailDialog.value = true
}

// 删除爬虫
const deleteSpider = async (spiderId) => {
  ElMessageBox.confirm('确认删除该爬虫吗？此操作不可恢复。', '警告', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await spidersAPI.deleteSpider(spiderId)
      ElMessage.success('删除成功')
      fetchSpiders()
    } catch (error) {
      ElMessage.error('删除失败: ' + error.message)
    }
  }).catch(() => {
    // 用户取消删除
  })
}

// 分页相关方法
const handleSizeChange = (val) => {
  pageSize.value = val
  fetchSpiders()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchSpiders()
}

// 初始化
onMounted(() => {
  fetchSpiders()
  fetchCategories()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}

.log-textarea {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
}
</style>
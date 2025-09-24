<template>
  <div class="system-design">
    <GlobalHeader />
    
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>系统设计文档</span>
        </div>
      </template>
      
      <el-tabs v-model="activeTab" type="border-card">
        <el-tab-pane label="API接口文档" name="api">
          <div class="api-docs">
            <h3>后端API接口文档</h3>
            <p>本系统基于Flask框架开发，使用JWT进行用户认证，MongoDB作为数据库。</p>
            
            <el-divider>认证相关接口</el-divider>
            
            <el-card class="api-card" shadow="hover">
              <div class="api-endpoint">
                <el-tag type="success">POST</el-tag>
                <strong>/api/register</strong> - 用户注册
              </div>
              <div class="api-description">
                <p>注册新用户</p>
                <div class="api-params">
                  <h4>请求参数:</h4>
                  <ul>
                    <li><code>username</code> (string, 必填) - 用户名</li>
                    <li><code>email</code> (string, 必填) - 邮箱</li>
                    <li><code>password</code> (string, 必填) - 密码</li>
                  </ul>
                </div>
              </div>
            </el-card>
            
            <el-card class="api-card" shadow="hover">
              <div class="api-endpoint">
                <el-tag type="success">POST</el-tag>
                <strong>/api/login</strong> - 用户登录
              </div>
              <div class="api-description">
                <p>用户登录，获取访问令牌</p>
                <div class="api-params">
                  <h4>请求参数:</h4>
                  <ul>
                    <li><code>username</code> (string, 必填) - 用户名</li>
                    <li><code>password</code> (string, 必填) - 密码</li>
                  </ul>
                  <h4>响应:</h4>
                  <ul>
                    <li><code>access_token</code> (string) - JWT访问令牌</li>
                    <li><code>user</code> (object) - 用户信息</li>
                  </ul>
                </div>
              </div>
            </el-card>
            
            <el-divider>用户管理接口</el-divider>
            
            <el-card class="api-card" shadow="hover">
              <div class="api-endpoint">
                <el-tag type="primary">GET</el-tag>
                <strong>/api/users</strong> - 获取用户列表
              </div>
              <div class="api-description">
                <p>获取所有用户信息（需要认证）</p>
              </div>
            </el-card>
            
            <el-card class="api-card" shadow="hover">
              <div class="api-endpoint">
                <el-tag type="primary">GET</el-tag>
                <strong>/api/users/&lt;user_id&gt;</strong> - 获取指定用户
              </div>
              <div class="api-description">
                <p>根据用户ID获取用户详细信息（需要认证）</p>
              </div>
            </el-card>
            
            <el-divider>爬虫管理接口</el-divider>
            
            <el-card class="api-card" shadow="hover">
              <div class="api-endpoint">
                <el-tag type="primary">GET</el-tag>
                <strong>/api/spiders</strong> - 获取爬虫列表
              </div>
              <div class="api-description">
                <p>获取所有爬虫信息（需要认证）</p>
              </div>
            </el-card>
            
            <el-card class="api-card" shadow="hover">
              <div class="api-endpoint">
                <el-tag type="success">POST</el-tag>
                <strong>/api/spiders</strong> - 创建爬虫
              </div>
              <div class="api-description">
                <p>创建新的爬虫（需要认证）</p>
                <div class="api-params">
                  <h4>请求参数:</h4>
                  <ul>
                    <li><code>name</code> (string, 必填) - 爬虫名称</li>
                    <li><code>description</code> (string, 必填) - 爬虫描述</li>
                    <li><code>script_path</code> (string, 必填) - 脚本路径</li>
                    <li><code>main_module</code> (string, 必填) - 主模块文件名</li>
                    <li><code>enabled</code> (boolean, 可选) - 是否启用，默认为true</li>
                  </ul>
                </div>
              </div>
            </el-card>
            
            <el-card class="api-card" shadow="hover">
              <div class="api-endpoint">
                <el-tag type="primary">GET</el-tag>
                <strong>/api/spiders/&lt;spider_id&gt;</strong> - 获取爬虫详情
              </div>
              <div class="api-description">
                <p>根据爬虫ID获取爬虫详细信息（需要认证）</p>
              </div>
            </el-card>
            
            <el-card class="api-card" shadow="hover">
              <div class="api-endpoint">
                <el-tag type="warning">PUT</el-tag>
                <strong>/api/spiders/&lt;spider_id&gt;</strong> - 更新爬虫
              </div>
              <div class="api-description">
                <p>更新指定爬虫信息（需要认证）</p>
              </div>
            </el-card>
            
            <el-card class="api-card" shadow="hover">
              <div class="api-endpoint">
                <el-tag type="danger">DELETE</el-tag>
                <strong>/api/spiders/&lt;spider_id&gt;</strong> - 删除爬虫
              </div>
              <div class="api-description">
                <p>删除指定爬虫（需要认证）</p>
              </div>
            </el-card>
            
            <el-card class="api-card" shadow="hover">
              <div class="api-endpoint">
                <el-tag type="success">POST</el-tag>
                <strong>/api/spiders/&lt;spider_id&gt;/run</strong> - 运行爬虫
              </div>
              <div class="api-description">
                <p>手动运行指定爬虫（需要认证）</p>
              </div>
            </el-card>
            
            <el-card class="api-card" shadow="hover">
              <div class="api-endpoint">
                <el-tag type="primary">GET</el-tag>
                <strong>/api/spiders/runs</strong> - 获取爬虫运行记录
              </div>
              <div class="api-description">
                <p>获取爬虫运行记录（需要认证）</p>
                <div class="api-params">
                  <h4>查询参数:</h4>
                  <ul>
                    <li><code>spider_id</code> (string, 可选) - 爬虫ID</li>
                  </ul>
                </div>
              </div>
            </el-card>
            
            <el-divider>任务管理接口</el-divider>
            
            <el-card class="api-card" shadow="hover">
              <div class="api-endpoint">
                <el-tag type="primary">GET</el-tag>
                <strong>/api/tasks</strong> - 获取任务列表
              </div>
              <div class="api-description">
                <p>获取所有任务信息（需要认证）</p>
                <div class="api-params">
                  <h4>查询参数:</h4>
                  <ul>
                    <li><code>page</code> (int, 可选) - 页码，默认为1</li>
                    <li><code>size</code> (int, 可选) - 每页数量，默认为10</li>
                    <li><code>name</code> (string, 可选) - 任务名称筛选</li>
                    <li><code>status</code> (string, 可选) - 任务状态筛选</li>
                    <li><code>spider_id</code> (string, 可选) - 爬虫ID筛选</li>
                  </ul>
                </div>
              </div>
            </el-card>
            
            <el-card class="api-card" shadow="hover">
              <div class="api-endpoint">
                <el-tag type="success">POST</el-tag>
                <strong>/api/tasks</strong> - 创建任务
              </div>
              <div class="api-description">
                <p>创建新的任务（需要认证）</p>
                <div class="api-params">
                  <h4>请求参数:</h4>
                  <ul>
                    <li><code>name</code> (string, 必填) - 任务名称</li>
                    <li><code>spider_id</code> (string, 必填) - 关联的爬虫ID</li>
                    <li><code>schedule_type</code> (string, 可选) - 调度类型 (manual/scheduled)，默认为manual</li>
                    <li><code>cron_expression</code> (string, 条件必填) - Cron表达式（当schedule_type为scheduled时必填）</li>
                    <li><code>parameters</code> (string, 可选) - 任务参数（JSON格式）</li>
                    <li><code>enabled</code> (boolean, 可选) - 是否启用，默认为true</li>
                    <li><code>description</code> (string, 可选) - 任务描述</li>
                  </ul>
                </div>
              </div>
            </el-card>
            
            <el-card class="api-card" shadow="hover">
              <div class="api-endpoint">
                <el-tag type="primary">GET</el-tag>
                <strong>/api/tasks/&lt;task_id&gt;</strong> - 获取任务详情
              </div>
              <div class="api-description">
                <p>根据任务ID获取任务详细信息（需要认证）</p>
              </div>
            </el-card>
            
            <el-card class="api-card" shadow="hover">
              <div class="api-endpoint">
                <el-tag type="warning">PUT</el-tag>
                <strong>/api/tasks/&lt;task_id&gt;</strong> - 更新任务
              </div>
              <div class="api-description">
                <p>更新指定任务信息（需要认证）</p>
              </div>
            </el-card>
            
            <el-card class="api-card" shadow="hover">
              <div class="api-endpoint">
                <el-tag type="danger">DELETE</el-tag>
                <strong>/api/tasks/&lt;task_id&gt;</strong> - 删除任务
              </div>
              <div class="api-description">
                <p>删除指定任务（需要认证）</p>
              </div>
            </el-card>
            
            <el-card class="api-card" shadow="hover">
              <div class="api-endpoint">
                <el-tag type="success">POST</el-tag>
                <strong>/api/tasks/&lt;task_id&gt;/execute</strong> - 执行任务
              </div>
              <div class="api-description">
                <p>手动执行指定任务（需要认证）</p>
              </div>
            </el-card>
            
            <el-card class="api-card" shadow="hover">
              <div class="api-endpoint">
                <el-tag type="primary">GET</el-tag>
                <strong>/api/tasks/runs</strong> - 获取任务运行记录
              </div>
              <div class="api-description">
                <p>获取任务运行记录（需要认证）</p>
                <div class="api-params">
                  <h4>查询参数:</h4>
                  <ul>
                    <li><code>task_id</code> (string, 可选) - 任务ID</li>
                  </ul>
                </div>
              </div>
            </el-card>
          </div>
        </el-tab-pane>
        
        <el-tab-pane label="系统架构" name="architecture">
          <div class="architecture">
            <h3>系统架构设计</h3>
            <p>本系统采用前后端分离的架构设计，后端基于Flask框架，前端基于Vue 3和Element Plus组件库。</p>
            
            <el-card class="arch-card">
              <div slot="header">
                <span>后端架构</span>
              </div>
              <div class="arch-content">
                <h4>分层架构</h4>
                <ul>
                  <li><strong>Routes层</strong>: 处理HTTP请求和响应</li>
                  <li><strong>Services层</strong>: 实现业务逻辑</li>
                  <li><strong>Repositories层</strong>: 处理数据访问</li>
                  <li><strong>Models层</strong>: 定义数据模型</li>
                </ul>
                
                <h4>技术栈</h4>
                <ul>
                  <li>Web框架: Flask</li>
                  <li>数据库: MongoDB</li>
                  <li>认证机制: JWT (JSON Web Tokens)</li>
                  <li>Python版本: 3.8+</li>
                </ul>
              </div>
            </el-card>
            
            <el-card class="arch-card">
              <div slot="header">
                <span>前端架构</span>
              </div>
              <div class="arch-content">
                <h4>技术栈</h4>
                <ul>
                  <li>框架: Vue 3 (Composition API)</li>
                  <li>状态管理: Pinia</li>
                  <li>UI组件库: Element Plus</li>
                  <li>构建工具: Vite</li>
                  <li>路由: Vue Router</li>
                </ul>
                
                <h4>目录结构</h4>
                <ul>
                  <li><code>components/</code>: 可复用的UI组件</li>
                  <li><code>views/</code>: 页面级组件</li>
                  <li><code>router/</code>: 路由配置</li>
                  <li><code>store/</code>: 状态管理</li>
                </ul>
              </div>
            </el-card>
            
            <el-card class="arch-card">
              <div slot="header">
                <span>认证机制</span>
              </div>
              <div class="arch-content">
                <p>系统使用JWT进行用户认证：</p>
                <ol>
                  <li>用户通过<code>/api/login</code>接口登录</li>
                  <li>服务器验证用户凭据，生成JWT令牌并返回给客户端</li>
                  <li>客户端在后续请求的Authorization头中携带令牌</li>
                  <li>服务器验证令牌有效性，处理请求</li>
                </ol>
                <p>令牌默认有效期为7天</p>
              </div>
            </el-card>
          </div>
        </el-tab-pane>
        
        <el-tab-pane label="数据模型" name="models">
          <div class="data-models">
            <h3>数据模型设计</h3>
            <p>系统使用MongoDB作为数据库，主要包含以下数据模型：</p>
            
            <el-card class="model-card">
              <div slot="header">
                <span>User (用户)</span>
              </div>
              <div class="model-content">
                <ul>
                  <li><code>_id</code> (ObjectId) - 用户ID</li>
                  <li><code>username</code> (string) - 用户名</li>
                  <li><code>email</code> (string) - 邮箱</li>
                  <li><code>password_hash</code> (string) - 密码哈希值</li>
                  <li><code>created_at</code> (datetime) - 创建时间</li>
                </ul>
              </div>
            </el-card>
            
            <el-card class="model-card">
              <div slot="header">
                <span>Spider (爬虫)</span>
              </div>
              <div class="model-content">
                <ul>
                  <li><code>_id</code> (ObjectId) - 爬虫ID</li>
                  <li><code>name</code> (string) - 爬虫名称</li>
                  <li><code>description</code> (string) - 描述</li>
                  <li><code>script_path</code> (string) - 脚本路径</li>
                  <li><code>main_module</code> (string) - 主模块文件名</li>
                  <li><code>enabled</code> (boolean) - 是否启用</li>
                  <li><code>created_at</code> (datetime) - 创建时间</li>
                  <li><code>updated_at</code> (datetime) - 更新时间</li>
                </ul>
              </div>
            </el-card>
            
            <el-card class="model-card">
              <div slot="header">
                <span>Task (任务)</span>
              </div>
              <div class="model-content">
                <ul>
                  <li><code>_id</code> (ObjectId) - 任务ID</li>
                  <li><code>name</code> (string) - 任务名称</li>
                  <li><code>spider_id</code> (ObjectId) - 关联的爬虫ID</li>
                  <li><code>schedule_type</code> (string) - 调度类型 (manual/scheduled)</li>
                  <li><code>cron_expression</code> (string) - Cron表达式</li>
                  <li><code>parameters</code> (string) - 参数（JSON格式）</li>
                  <li><code>enabled</code> (boolean) - 是否启用</li>
                  <li><code>status</code> (string) - 任务状态</li>
                  <li><code>scheduled_time</code> (datetime) - 计划执行时间</li>
                  <li><code>start_time</code> (datetime) - 开始执行时间</li>
                  <li><code>end_time</code> (datetime) - 结束执行时间</li>
                  <li><code>created_at</code> (datetime) - 创建时间</li>
                  <li><code>updated_at</code> (datetime) - 更新时间</li>
                </ul>
              </div>
            </el-card>
            
            <el-card class="model-card">
              <div slot="header">
                <span>TaskRun (任务执行记录)</span>
              </div>
              <div class="model-content">
                <ul>
                  <li><code>_id</code> (ObjectId) - 执行记录ID</li>
                  <li><code>task_id</code> (ObjectId) - 关联的任务ID</li>
                  <li><code>spider_id</code> (ObjectId) - 关联的爬虫ID</li>
                  <li><code>status</code> (string) - 执行状态</li>
                  <li><code>parameters</code> (string) - 执行时的参数</li>
                  <li><code>log_output</code> (string) - 日志输出</li>
                  <li><code>error_message</code> (string) - 错误信息</li>
                  <li><code>start_time</code> (datetime) - 开始执行时间</li>
                  <li><code>end_time</code> (datetime) - 结束执行时间</li>
                </ul>
              </div>
            </el-card>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import GlobalHeader from '../components/GlobalHeader.vue'

const activeTab = ref('api')
</script>

<style scoped>
.system-design {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 20px;
}

@media (min-width: 1200px) {
  .system-design {
    max-width: 1400px;
    margin: 0 auto;
  }
}

@media (min-width: 1600px) {
  .system-design {
    max-width: 1600px;
  }
}

.page-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.api-docs h3, .architecture h3, .data-models h3 {
  margin-bottom: 20px;
  color: #303133;
}

.api-card, .arch-card, .model-card {
  margin-bottom: 20px;
}

.api-endpoint {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.api-endpoint .el-tag {
  width: 60px;
  text-align: center;
}

.api-description p {
  color: #606266;
  margin: 10px 0;
}

.api-params h4 {
  margin: 10px 0 5px;
}

.api-params ul {
  padding-left: 20px;
}

.api-params li {
  margin-bottom: 5px;
}

.arch-content h4, .model-content h4 {
  margin: 15px 0 10px;
}

.arch-content ul, .model-content ul {
  padding-left: 20px;
}

.arch-content li, .model-content li {
  margin-bottom: 5px;
}

.el-divider {
  margin: 30px 0;
}
</style>
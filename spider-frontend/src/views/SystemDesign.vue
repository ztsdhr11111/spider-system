<template>
  <div>
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
            <p class="note">API文档通过Swagger UI自动生成，与后端代码保持同步。</p>
            
            <div class="iframe-container">
              <iframe 
                src="http://127.0.0.1:5000/docs/" 
                frameborder="0" 
                class="swagger-frame"
                title="API Documentation">
              </iframe>
            </div>
          </div>
        </el-tab-pane>
        
        <el-tab-pane label="系统架构" name="architecture">
          <div class="architecture">
            <h3>系统架构设计</h3>
            <p>本系统采用前后端分离的架构设计，后端基于Flask框架，前端基于Vue 3和Element Plus组件库。</p>
            
            <div class="arch-section">
              <h4>后端架构</h4>
              <div class="arch-content">
                <h5>分层架构</h5>
                <ul>
                  <li><strong>Routes层</strong>: 处理HTTP请求和响应</li>
                  <li><strong>Services层</strong>: 实现业务逻辑</li>
                  <li><strong>Repositories层</strong>: 处理数据访问</li>
                  <li><strong>Models层</strong>: 定义数据模型</li>
                </ul>
                
                <h5>技术栈</h5>
                <ul>
                  <li>Web框架: Flask</li>
                  <li>数据库: MongoDB</li>
                  <li>认证机制: JWT (JSON Web Tokens)</li>
                  <li>Python版本: 3.8+</li>
                </ul>
              </div>
            </div>
            
            <div class="arch-section">
              <h4>前端架构</h4>
              <div class="arch-content">
                <h5>技术栈</h5>
                <ul>
                  <li>框架: Vue 3 (Composition API)</li>
                  <li>状态管理: Pinia</li>
                  <li>UI组件库: Element Plus</li>
                  <li>构建工具: Vite</li>
                  <li>路由: Vue Router</li>
                </ul>
                
                <h5>目录结构</h5>
                <ul>
                  <li><code>components/</code>: 可复用的UI组件</li>
                  <li><code>views/</code>: 页面级组件</li>
                  <li><code>router/</code>: 路由配置</li>
                  <li><code>store/</code>: 状态管理</li>
                </ul>
              </div>
            </div>
            
            <div class="arch-section">
              <h4>认证机制</h4>
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
            </div>
          </div>
        </el-tab-pane>
        
        <el-tab-pane label="数据模型" name="models">
          <div class="data-models">
            <h3>数据模型设计</h3>
            <p>系统使用MongoDB作为数据库，主要包含以下数据模型：</p>
            
            <div class="model-section">
              <h4>User (用户)</h4>
              <div class="model-content">
                <table>
                  <thead>
                    <tr>
                      <th>字段名</th>
                      <th>类型</th>
                      <th>说明</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><code>_id</code></td>
                      <td>ObjectId</td>
                      <td>用户ID</td>
                    </tr>
                    <tr>
                      <td><code>username</code></td>
                      <td>string</td>
                      <td>用户名</td>
                    </tr>
                    <tr>
                      <td><code>email</code></td>
                      <td>string</td>
                      <td>邮箱</td>
                    </tr>
                    <tr>
                      <td><code>password_hash</code></td>
                      <td>string</td>
                      <td>密码哈希值</td>
                    </tr>
                    <tr>
                      <td><code>created_at</code></td>
                      <td>datetime</td>
                      <td>创建时间</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            
            <div class="model-section">
              <h4>Spider (爬虫)</h4>
              <div class="model-content">
                <table>
                  <thead>
                    <tr>
                      <th>字段名</th>
                      <th>类型</th>
                      <th>说明</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><code>_id</code></td>
                      <td>ObjectId</td>
                      <td>爬虫ID</td>
                    </tr>
                    <tr>
                      <td><code>name</code></td>
                      <td>string</td>
                      <td>爬虫名称</td>
                    </tr>
                    <tr>
                      <td><code>description</code></td>
                      <td>string</td>
                      <td>描述</td>
                    </tr>
                    <tr>
                      <td><code>script_path</code></td>
                      <td>string</td>
                      <td>脚本路径</td>
                    </tr>
                    <tr>
                      <td><code>main_module</code></td>
                      <td>string</td>
                      <td>主模块文件名</td>
                    </tr>
                    <tr>
                      <td><code>enabled</code></td>
                      <td>boolean</td>
                      <td>是否启用</td>
                    </tr>
                    <tr>
                      <td><code>created_at</code></td>
                      <td>datetime</td>
                      <td>创建时间</td>
                    </tr>
                    <tr>
                      <td><code>updated_at</code></td>
                      <td>datetime</td>
                      <td>更新时间</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            
            <div class="model-section">
              <h4>Task (任务)</h4>
              <div class="model-content">
                <table>
                  <thead>
                    <tr>
                      <th>字段名</th>
                      <th>类型</th>
                      <th>说明</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><code>_id</code></td>
                      <td>ObjectId</td>
                      <td>任务ID</td>
                    </tr>
                    <tr>
                      <td><code>name</code></td>
                      <td>string</td>
                      <td>任务名称</td>
                    </tr>
                    <tr>
                      <td><code>spider_id</code></td>
                      <td>ObjectId</td>
                      <td>关联的爬虫ID</td>
                    </tr>
                    <tr>
                      <td><code>schedule_type</code></td>
                      <td>string</td>
                      <td>调度类型 (manual/scheduled)</td>
                    </tr>
                    <tr>
                      <td><code>cron_expression</code></td>
                      <td>string</td>
                      <td>Cron表达式</td>
                    </tr>
                    <tr>
                      <td><code>parameters</code></td>
                      <td>string</td>
                      <td>参数（JSON格式）</td>
                    </tr>
                    <tr>
                      <td><code>enabled</code></td>
                      <td>boolean</td>
                      <td>是否启用</td>
                    </tr>
                    <tr>
                      <td><code>status</code></td>
                      <td>string</td>
                      <td>任务状态</td>
                    </tr>
                    <tr>
                      <td><code>scheduled_time</code></td>
                      <td>datetime</td>
                      <td>计划执行时间</td>
                    </tr>
                    <tr>
                      <td><code>start_time</code></td>
                      <td>datetime</td>
                      <td>开始执行时间</td>
                    </tr>
                    <tr>
                      <td><code>end_time</code></td>
                      <td>datetime</td>
                      <td>结束执行时间</td>
                    </tr>
                    <tr>
                      <td><code>created_at</code></td>
                      <td>datetime</td>
                      <td>创建时间</td>
                    </tr>
                    <tr>
                      <td><code>updated_at</code></td>
                      <td>datetime</td>
                      <td>更新时间</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            
            <div class="model-section">
              <h4>TaskRun (任务执行记录)</h4>
              <div class="model-content">
                <table>
                  <thead>
                    <tr>
                      <th>字段名</th>
                      <th>类型</th>
                      <th>说明</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><code>_id</code></td>
                      <td>ObjectId</td>
                      <td>执行记录ID</td>
                    </tr>
                    <tr>
                      <td><code>task_id</code></td>
                      <td>ObjectId</td>
                      <td>关联的任务ID</td>
                    </tr>
                    <tr>
                      <td><code>spider_id</code></td>
                      <td>ObjectId</td>
                      <td>关联的爬虫ID</td>
                    </tr>
                    <tr>
                      <td><code>status</code></td>
                      <td>string</td>
                      <td>执行状态</td>
                    </tr>
                    <tr>
                      <td><code>parameters</code></td>
                      <td>string</td>
                      <td>执行时的参数</td>
                    </tr>
                    <tr>
                      <td><code>log_output</code></td>
                      <td>string</td>
                      <td>日志输出</td>
                    </tr>
                    <tr>
                      <td><code>error_message</code></td>
                      <td>string</td>
                      <td>错误信息</td>
                    </tr>
                    <tr>
                      <td><code>start_time</code></td>
                      <td>datetime</td>
                      <td>开始执行时间</td>
                    </tr>
                    <tr>
                      <td><code>end_time</code></td>
                      <td>datetime</td>
                      <td>结束执行时间</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
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
.page-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.note {
  background-color: #fffbe6;
  border: 1px solid #ffe58f;
  border-radius: 4px;
  padding: 10px;
  margin: 10px 0;
  color: #d46b08;
}

.iframe-container {
  width: 100%;
  height: 800px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  overflow: hidden;
  margin-top: 20px;
}

.swagger-frame {
  width: 100%;
  height: 100%;
}

.arch-section,
.model-section {
  margin-bottom: 30px;
}

.arch-section h4,
.model-section h4 {
  margin: 20px 0 10px;
  color: #303133;
  border-left: 4px solid #409eff;
  padding-left: 10px;
}

.arch-content h5,
.model-content h5 {
  margin: 15px 0 10px;
}

.arch-content ul,
.model-content ul {
  padding-left: 20px;
  margin-bottom: 15px;
}

.arch-content li,
.model-content li {
  margin-bottom: 5px;
}

.arch-content ol {
  padding-left: 20px;
  margin-bottom: 15px;
}

.arch-content ol li {
  margin-bottom: 5px;
}

.model-content table {
  width: 100%;
  border-collapse: collapse;
  margin: 15px 0;
}

.model-content table th,
.model-content table td {
  border: 1px solid #ebeef5;
  padding: 8px 12px;
  text-align: left;
}

.model-content table th {
  background-color: #f5f7fa;
  font-weight: bold;
}

.auto-doc h3,
.architecture h3,
.data-models h3,
.api-docs h3 {
  margin-bottom: 20px;
  color: #303133;
  border-left: 4px solid #409eff;
  padding-left: 10px;
}

.auto-doc h4,
.architecture h4,
.data-models h4,
.api-docs h4 {
  margin: 20px 0 10px;
  color: #303133;
}

.auto-doc p,
.architecture p,
.data-models p,
.api-docs p {
  line-height: 1.6;
  color: #606266;
}
</style>
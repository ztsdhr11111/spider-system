<template>
  <div class="system-design">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>系统设计模块</span>
        </div>
      </template>
      <el-form :model="form" label-width="120px">
        <el-form-item label="爬虫名称">
          <el-input v-model="form.crawlerName" />
        </el-form-item>
        <el-form-item label="爬虫类型">
          <el-select v-model="form.crawlerType">
            <el-option label="网页爬虫" value="web" />
            <el-option label="API爬虫" value="api" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm">保存</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

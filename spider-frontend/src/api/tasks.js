// src/api/tasks.js
// 任务相关 API
import { request } from './index'

// 获取任务列表
export async function getTasks(page = 1, size = 10, filters = {}) {
  const params = new URLSearchParams({
    page,
    size,
    ...filters
  })
  
  return request(`/tasks?${params}`)
}

// 创建任务
export async function createTask(taskData) {
  return request('/tasks', {
    method: 'POST',
    body: JSON.stringify(taskData)
  })
}

// 获取任务详情
export async function getTask(taskId) {
  return request(`/tasks/${taskId}`)
}

// 更新任务
export async function updateTask(taskId, taskData) {
  return request(`/tasks/${taskId}`, {
    method: 'PUT',
    body: JSON.stringify(taskData)
  })
}

// 删除任务
export async function deleteTask(taskId) {
  return request(`/tasks/${taskId}`, {
    method: 'DELETE'
  })
}

// 运行任务
export async function runTask(taskId) {
  return request(`/tasks/${taskId}/execute`, {
    method: 'POST'
  })
}

// 获取任务执行记录
export async function getTaskRuns(filters = {}) {
  const params = new URLSearchParams(filters)
  return request(`/tasks/runs?${params}`)
}
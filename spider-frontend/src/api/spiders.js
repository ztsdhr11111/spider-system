// src/api/spiders.js
// 爬虫相关 API
import { request } from './index'

// 获取爬虫列表
export async function getSpiders(page = 1, size = 10, filters = {}) {
  const params = new URLSearchParams({
    page,
    size,
    ...filters
  })
  
  return request(`/spiders/?${params}`)
}

// 创建爬虫
export async function createSpider(spiderData) {
  return request('/spiders/', {
    method: 'POST',
    body: JSON.stringify(spiderData)
  })
}

// 获取爬虫详情
export async function getSpider(spiderId) {
  return request(`/spiders/${spiderId}`)
}

// 更新爬虫
export async function updateSpider(spiderId, spiderData) {
  return request(`/spiders/${spiderId}`, {
    method: 'PUT',
    body: JSON.stringify(spiderData)
  })
}

// 删除爬虫
export async function deleteSpider(spiderId) {
  return request(`/spiders/${spiderId}`, {
    method: 'DELETE'
  })
}

// 运行爬虫
export async function runSpider(spiderId) {
  return request(`/spiders/${spiderId}/run`, {
    method: 'POST'
  })
}

// 获取爬虫运行记录
export async function getSpiderRuns(spiderId) {
  const params = new URLSearchParams({ spider_id: spiderId })
  return request(`/spiders/runs?${params}`)
}
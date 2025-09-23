# app/repositories/task_repository.py
from app import mongo
from app.models.task import Task
from app.models.task_run import TaskRun
from bson import ObjectId
from typing import Optional, List
from datetime import datetime

class TaskRepository:
    def __init__(self):
        self.tasks_collection = mongo.tasks
        self.task_runs_collection = mongo.task_runs
    
    def find_all_tasks(self, page: int = 1, size: int = 10, filters: dict = None) -> List[Task]:
        """获取所有任务"""
        print('task repository find all tasks')
        query = {}
        if filters:
            if filters.get('name'):
                query['name'] = {'$regex': filters['name'], '$options': 'i'}
            if filters.get('status'):
                query['status'] = filters['status']
            if filters.get('spider_id'):
                query['spider_id'] = filters['spider_id']
        
        skip = (page - 1) * size
        tasks_data = list(self.tasks_collection.find(query).skip(skip).limit(size).sort('created_at', -1))
        return [Task.from_dict(task_data) for task_data in tasks_data]
    
    def count_tasks(self, filters: dict = None) -> int:
        """统计任务数量"""
        query = {}
        if filters:
            if filters.get('name'):
                query['name'] = {'$regex': filters['name'], '$options': 'i'}
            if filters.get('status'):
                query['status'] = filters['status']
            if filters.get('spider_id'):
                query['spider_id'] = filters['spider_id']
        
        return self.tasks_collection.count_documents(query)
    
    def find_task_by_id(self, task_id: str) -> Optional[Task]:
        """根据ID查找任务"""
        try:
            task_data = self.tasks_collection.find_one({'_id': ObjectId(task_id)})
            return Task.from_dict(task_data) if task_data else None
        except Exception:
            return None
    
    def save_task(self, task: Task) -> str:
        """保存任务"""
        task_data = task.to_dict()
        task_id = task_data.get('_id')
        
        if task_id and str(task_id).strip():
            # 更新操作
            del task_data['_id']
            task_data['updated_at'] = datetime.utcnow()
            self.tasks_collection.update_one(
                {'_id': ObjectId(task_id)}, 
                {'$set': task_data}
            )
        else:
            # 插入操作
            if '_id' in task_data:
                del task_data['_id']
            result = self.tasks_collection.insert_one(task_data)
            task_id = str(result.inserted_id)
        
        return task_id
    
    def delete_task(self, task_id: str) -> bool:
        """删除任务"""
        result = self.tasks_collection.delete_one({'_id': ObjectId(task_id)})
        return result.deleted_count > 0
    
    def save_task_run(self, run: TaskRun) -> str:
        """保存任务执行记录"""
        run_data = run.to_dict()
        run_id = run_data.get('_id')
        
        if run_id and str(run_id).strip():
            # 更新操作
            del run_data['_id']
            self.task_runs_collection.update_one(
                {'_id': ObjectId(run_id)}, 
                {'$set': run_data}
            )
        else:
            # 插入操作
            if '_id' in run_data:
                del run_data['_id']
            result = self.task_runs_collection.insert_one(run_data)
            run_id = str(result.inserted_id)
        
        return run_id
    
    def find_task_runs(self, task_id: str = None, limit: int = 50) -> List[TaskRun]:
        """获取任务执行记录"""
        query = {}
        if task_id:
            query['task_id'] = task_id
        
        runs_data = list(self.task_runs_collection.find(query).sort('start_time', -1).limit(limit))
        return [TaskRun.from_dict(run_data) for run_data in runs_data]
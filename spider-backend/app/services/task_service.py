# app/services/task_service.py
import json
from datetime import datetime
from app.repositories.task_repository import TaskRepository
from app.repositories.spider_repository import SpiderRepository
from app.models.task import Task
from app.models.task_run import TaskRun
from app.services.spider_service import SpiderService
from app.utils.exceptions import BusinessError
import croniter

class TaskService:
    def __init__(self):
        self.task_repository = TaskRepository()
        self.spider_repository = SpiderRepository()
        self.spider_service = SpiderService()
    
    def get_all_tasks(self, page: int = 1, size: int = 10, filters: dict = None):
        """获取所有任务"""
        print('task service get all tasks')
        tasks = self.task_repository.find_all_tasks(page, size, filters)
        total = self.task_repository.count_tasks(filters)
        
        # 补充爬虫名称信息
        spider_ids = list(set(task.spider_id for task in tasks))
        spiders = {}
        for spider_id in spider_ids:
            spider = self.spider_repository.find_spider_by_id(spider_id)
            if spider:
                spiders[spider_id] = spider
        
        tasks_data = []
        for task in tasks:
            task_data = task.to_dict()
            spider = spiders.get(task.spider_id)
            if spider:
                task_data['spider_name'] = spider.name
            tasks_data.append(task_data)
        
        return {
            'tasks': tasks_data,
            'total': total,
            'page': page,
            'size': size
        }
    
    def get_task_by_id(self, task_id):
        """根据ID获取任务"""
        task = self.task_repository.find_task_by_id(task_id)
        if not task:
            raise BusinessError('Task not found')
        
        # 补充爬虫名称信息
        spider = self.spider_repository.find_spider_by_id(task.spider_id)
        task_data = task.to_dict()
        if spider:
            task_data['spider_name'] = spider.name
        
        return task_data
    
    def create_task(self, task_data):
        """创建任务"""
        # 验证爬虫是否存在
        spider = self.spider_repository.find_spider_by_id(task_data['spider_id'])
        if not spider:
            raise BusinessError('Spider not found')
        
        # 验证调度类型
        if task_data.get('schedule_type') == 'scheduled':
            if not task_data.get('cron_expression'):
                raise BusinessError('Cron expression is required for scheduled tasks')
            
            # 验证Cron表达式
            try:
                croniter.croniter(task_data['cron_expression'])
            except Exception:
                raise BusinessError('Invalid cron expression')
        
        # 验证参数格式（如果提供）
        if task_data.get('parameters'):
            try:
                json.loads(task_data['parameters'])
            except json.JSONDecodeError:
                raise BusinessError('Parameters must be valid JSON')
        
        task = Task(
            name=task_data['name'],
            spider_id=task_data['spider_id'],
            schedule_type=task_data.get('schedule_type', 'manual'),
            cron_expression=task_data.get('cron_expression'),
            parameters=task_data.get('parameters'),
            enabled=task_data.get('enabled', True),
            description=task_data.get('description')
        )
        
        # 计算下次执行时间
        if task.schedule_type == 'scheduled' and task.enabled:
            try:
                cron = croniter.croniter(task.cron_expression, datetime.utcnow())
                task.scheduled_time = cron.get_next(datetime)
            except Exception:
                pass  # 如果计算失败，scheduled_time保持为None
        
        task_id = self.task_repository.save_task(task)
        task._id = task_id
        return task.to_dict()
    
    def update_task(self, task_id, task_data):
        """更新任务"""
        task = self.task_repository.find_task_by_id(task_id)
        if not task:
            raise BusinessError('Task not found')
        
        # 更新字段
        updatable_fields = ['name', 'schedule_type', 'cron_expression', 'parameters', 'enabled', 'description']
        for field in updatable_fields:
            if field in task_data:
                setattr(task, field, task_data[field])
        
        # 如果是调度任务且启用，计算下次执行时间
        if task.schedule_type == 'scheduled' and task.enabled:
            if task.cron_expression:
                try:
                    cron = croniter.croniter(task.cron_expression, datetime.utcnow())
                    task.scheduled_time = cron.get_next(datetime)
                except Exception:
                    task.scheduled_time = None
        else:
            task.scheduled_time = None
        
        task.updated_at = datetime.utcnow()
        self.task_repository.save_task(task)
        return task.to_dict()
    
    def delete_task(self, task_id):
        """删除任务"""
        return self.task_repository.delete_task(task_id)
    
    def execute_task(self, task_id):
        """执行任务"""
        task = self.task_repository.find_task_by_id(task_id)
        if not task:
            raise BusinessError('Task not found')
        
        if not task.enabled:
            raise BusinessError('Task is disabled')
        
        # 更新任务状态
        task.status = 'running'
        task.start_time = datetime.utcnow()
        task.end_time = None
        self.task_repository.save_task(task)
        
        # 创建执行记录
        run = TaskRun(
            task_id=task_id,
            spider_id=task.spider_id,
            status='running',
            parameters=task.parameters
        )
        run_id = self.task_repository.save_task_run(run)
        
        try:
            # 执行关联的爬虫
            result = self.spider_service.run_spider(task.spider_id)
            
            # 更新执行记录
            run.end_time = datetime.utcnow()
            run.status = 'success' if result['status'] == 'success' else 'failed'
            run.log_output = result.get('output', '')
            run.error_message = result.get('error', None)
            self.task_repository.save_task_run(run)
            
            # 更新任务状态
            task.status = 'completed' if result['status'] == 'success' else 'failed'
            task.end_time = datetime.utcnow()
            self.task_repository.save_task(task)
            
            return {
                'run_id': run_id,
                'status': run.status,
                'output': result.get('output', ''),
                'error': result.get('error', None)
            }
            
        except Exception as e:
            # 更新执行记录
            run.end_time = datetime.utcnow()
            run.status = 'failed'
            run.error_message = str(e)
            self.task_repository.save_task_run(run)
            
            # 更新任务状态
            task.status = 'failed'
            task.end_time = datetime.utcnow()
            self.task_repository.save_task(task)
            
            raise BusinessError(f'Failed to execute task: {str(e)}')
    
    def get_task_runs(self, task_id=None, page=1, size=10):
        """获取任务执行记录"""
        runs = self.task_repository.find_task_runs(task_id, page, size)
        return [run.to_dict() for run in runs]
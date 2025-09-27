# app/routes/task_routes.py
from flask import Blueprint, request, jsonify
from app.services.task_service import TaskService
from flask_jwt_extended import jwt_required
from app.utils.exceptions import BusinessError
# 导入 flask-restx 相关模块
from app import api
from flask_restx import Resource, fields

task_bp = Blueprint('tasks', __name__)
task_service = TaskService()

# 定义 API 模型
task_model = api.model('Task', {
    'name': fields.String(required=True, description='任务名称'),
    'spider_id': fields.String(required=True, description='爬虫ID'),
    'schedule_type': fields.String(default='manual', description='调度类型 (manual/scheduled)'),
    'cron_expression': fields.String(description='Cron表达式'),
    'parameters': fields.String(description='参数（JSON格式）'),
    'enabled': fields.Boolean(default=True, description='是否启用'),
    'description': fields.String(description='任务描述')
})

task_response_model = api.model('TaskResponse', {
    '_id': fields.String(description='任务ID'),
    'name': fields.String(description='任务名称'),
    'spider_id': fields.String(description='爬虫ID'),
    'schedule_type': fields.String(description='调度类型'),
    'cron_expression': fields.String(description='Cron表达式'),
    'parameters': fields.String(description='参数'),
    'enabled': fields.Boolean(description='是否启用'),
    'description': fields.String(description='任务描述'),
    'created_at': fields.String(description='创建时间'),
    'updated_at': fields.String(description='更新时间'),
    'scheduled_time': fields.String(description='计划执行时间'),
    'start_time': fields.String(description='开始执行时间'),
    'end_time': fields.String(description='结束执行时间'),
    'status': fields.String(description='任务状态')
})

task_run_model = api.model('TaskRun', {
    '_id': fields.String(description='执行记录ID'),
    'task_id': fields.String(description='任务ID'),
    'spider_id': fields.String(description='爬虫ID'),
    'status': fields.String(description='执行状态'),
    'parameters': fields.String(description='执行时的参数'),
    'start_time': fields.String(description='开始执行时间'),
    'end_time': fields.String(description='结束执行时间'),
    'log_output': fields.String(description='日志输出'),
    'error_message': fields.String(description='错误信息')
})

# 定义命名空间
task_ns = api.namespace('tasks', description='任务相关操作')

@task_ns.route('')
class Tasks(Resource):
    @api.doc('get_tasks')
    @api.param('page', '页码', default=1)
    @api.param('size', '每页数量', default=10)
    @api.param('name', '任务名称')
    @api.param('status', '任务状态')
    @api.param('spider_id', '爬虫ID')
    @jwt_required()
    def get(self):
        """获取任务列表"""
        try:
            page = int(request.args.get('page', 1))
            size = int(request.args.get('size', 10))
            
            filters = {}
            if request.args.get('name'):
                filters['name'] = request.args.get('name')
            if request.args.get('status'):
                filters['status'] = request.args.get('status')
            if request.args.get('spider_id'):
                filters['spider_id'] = request.args.get('spider_id')
            
            result = task_service.get_all_tasks(page, size, filters)
            return result
        except Exception as e:
            return {'message': str(e)}, 500
    
    @api.doc('create_task')
    @api.expect(task_model)
    @api.marshal_with(task_response_model, code=201)
    @jwt_required()
    def post(self):
        """创建任务"""
        try:
            task_data = request.get_json()
            task = task_service.create_task(task_data)
            return task, 201
        except BusinessError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': str(e)}, 500

@task_ns.route('/<task_id>')
@task_ns.param('task_id', '任务ID')
class Task(Resource):
    @api.doc('get_task')
    @jwt_required()
    def get(self, task_id):
        """获取任务详情"""
        try:
            task = task_service.get_task_by_id(task_id)
            return task
        except BusinessError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': str(e)}, 500
    
    @api.doc('update_task')
    @api.expect(task_model)
    @api.marshal_with(task_response_model)
    @jwt_required()
    def put(self, task_id):
        """更新任务"""
        try:
            task_data = request.get_json()
            task = task_service.update_task(task_id, task_data)
            return task
        except BusinessError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': str(e)}, 500
    
    @api.doc('delete_task')
    @jwt_required()
    def delete(self, task_id):
        """删除任务"""
        try:
            result = task_service.delete_task(task_id)
            if result:
                return '', 204
            else:
                return {'message': 'Task not found'}, 404
        except Exception as e:
            return {'message': str(e)}, 500

@task_ns.route('/<task_id>/execute')
@task_ns.param('task_id', '任务ID')
class ExecuteTask(Resource):
    @api.doc('execute_task')
    @jwt_required()
    def post(self, task_id):
        """执行任务"""
        try:
            result = task_service.execute_task(task_id)
            return result
        except BusinessError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': str(e)}, 500

@task_ns.route('/runs')
class TaskRuns(Resource):
    @api.doc('get_task_runs')
    @api.param('task_id', '任务ID')
    @jwt_required()
    def get(self):
        """获取任务执行记录"""
        try:
            task_id = request.args.get('task_id')
            runs = task_service.get_task_runs(task_id)
            return runs
        except Exception as e:
            return {'message': str(e)}, 500
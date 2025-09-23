# app/routes/task_routes.py
from flask import Blueprint, request, jsonify
from app.services.task_service import TaskService
from flask_jwt_extended import jwt_required
from app.utils.exceptions import BusinessError

task_bp = Blueprint('tasks', __name__)
task_service = TaskService()

@task_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
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
        return jsonify(result)
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@task_bp.route('/tasks/<task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    """获取任务详情"""
    try:
        task = task_service.get_task_by_id(task_id)
        return jsonify(task)
    except BusinessError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@task_bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    """创建任务"""
    try:
        task_data = request.get_json()
        task = task_service.create_task(task_data)
        return jsonify(task), 201
    except BusinessError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@task_bp.route('/tasks/<task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    """更新任务"""
    try:
        task_data = request.get_json()
        task = task_service.update_task(task_id, task_data)
        return jsonify(task)
    except BusinessError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@task_bp.route('/tasks/<task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    """删除任务"""
    try:
        result = task_service.delete_task(task_id)
        if result:
            return '', 204
        else:
            return jsonify({'message': 'Task not found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@task_bp.route('/tasks/<task_id>/execute', methods=['POST'])
@jwt_required()
def execute_task(task_id):
    """执行任务"""
    try:
        result = task_service.execute_task(task_id)
        return jsonify(result)
    except BusinessError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@task_bp.route('/tasks/runs', methods=['GET'])
@jwt_required()
def get_task_runs():
    """获取任务执行记录"""
    try:
        task_id = request.args.get('task_id')
        runs = task_service.get_task_runs(task_id)
        return jsonify(runs)
    except Exception as e:
        return jsonify({'message': str(e)}), 500
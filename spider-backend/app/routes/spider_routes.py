# app/routes/spider_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.spider_service import SpiderService
from app.utils.exceptions import BusinessError
# 导入 flask-restx 相关模块
from app import api
from flask_restx import Resource, fields

bp = Blueprint('spiders', __name__)
spider_service = SpiderService()

# 定义 API 模型
spider_model = api.model('Spider', {
    'name': fields.String(required=True, description='爬虫名称'),
    'description': fields.String(required=True, description='爬虫描述'),
    'script_path': fields.String(required=True, description='脚本路径'),
    'main_module': fields.String(required=True, description='主模块文件名'),
    'enabled': fields.Boolean(default=True, description='是否启用')
})

spider_response_model = api.model('SpiderResponse', {
    '_id': fields.String(description='爬虫ID'),
    'name': fields.String(description='爬虫名称'),
    'description': fields.String(description='爬虫描述'),
    'script_path': fields.String(description='脚本路径'),
    'main_module': fields.String(description='主模块文件名'),
    'created_at': fields.String(description='创建时间'),
    'updated_at': fields.String(description='更新时间'),
    'enabled': fields.Boolean(description='是否启用')
})

spider_run_model = api.model('SpiderRun', {
    '_id': fields.String(description='运行记录ID'),
    'spider_id': fields.String(description='爬虫ID'),
    'status': fields.String(description='运行状态'),
    'start_time': fields.String(description='开始时间'),
    'end_time': fields.String(description='结束时间'),
    'result_data': fields.Raw(description='结果数据'),
    'log_output': fields.String(description='日志输出'),
    'error_message': fields.String(description='错误信息')
})

# 定义命名空间
spider_ns = api.namespace('spiders', description='爬虫相关操作')

@spider_ns.route('/')
class Spiders(Resource):
    @api.doc('list_spiders')
    @jwt_required()
    def get(self):
        """获取爬虫列表"""
        try:
            spiders = spider_service.get_all_spiders()
            return spiders, 200
        except Exception as e:
            return {'message': 'Internal server error'}, 500
    
    @api.doc('create_spider')
    @api.expect(spider_model)
    @api.marshal_with(spider_response_model, code=201)
    @jwt_required()
    def post(self):
        """创建爬虫"""
        try:
            data = request.get_json()
            required_fields = ['name', 'description', 'script_path', 'main_module']
            for field in required_fields:
                if field not in data or not data[field]:
                    return {'message': f'Missing required field: {field}'}, 400
            
            spider = spider_service.create_spider(data)
            return spider, 201
        except BusinessError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': 'Internal server error'}, 500

@spider_ns.route('/<spider_id>')
@spider_ns.param('spider_id', '爬虫ID')
class Spider(Resource):
    @api.doc('get_spider')
    @jwt_required()
    def get(self, spider_id):
        """获取爬虫详情"""
        try:
            spider = spider_service.get_spider_by_id(spider_id)
            if spider:
                return spider, 200
            return {'message': 'Spider not found'}, 404
        except Exception as e:
            return {'message': 'Internal server error'}, 500
    
    @api.doc('update_spider')
    @api.expect(spider_model)
    @api.marshal_with(spider_response_model)
    @jwt_required()
    def put(self, spider_id):
        """更新爬虫"""
        try:
            data = request.get_json()
            spider = spider_service.update_spider(spider_id, data)
            return spider, 200
        except BusinessError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': 'Internal server error'}, 500
    
    @api.doc('delete_spider')
    @jwt_required()
    def delete(self, spider_id):
        """删除爬虫"""
        try:
            result = spider_service.delete_spider(spider_id)
            if result:
                return {'message': 'Spider deleted successfully'}, 200
            return {'message': 'Spider not found'}, 404
        except Exception as e:
            return {'message': 'Internal server error'}, 500

@spider_ns.route('/<spider_id>/run')
@spider_ns.param('spider_id', '爬虫ID')
class RunSpider(Resource):
    @api.doc('run_spider')
    @jwt_required()
    def post(self, spider_id):
        """手动运行爬虫"""
        try:
            result = spider_service.run_spider(spider_id)
            return result, 200
        except BusinessError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': 'Internal server error'}, 500

@spider_ns.route('/runs')
class SpiderRuns(Resource):
    @api.doc('list_spider_runs')
    @api.param('spider_id', '爬虫ID')
    @jwt_required()
    def get(self):
        """获取爬虫运行记录"""
        try:
            spider_id = request.args.get('spider_id')
            runs = spider_service.get_spider_runs(spider_id)
            return runs, 200
        except Exception as e:
            return {'message': 'Internal server error'}, 500
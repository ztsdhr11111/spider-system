# app/routes/spider_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.spider_service import SpiderService
from app.utils.exceptions import BusinessError

bp = Blueprint('spiders', __name__)
spider_service = SpiderService()

@bp.route('/spiders', methods=['GET'])
@jwt_required()
def list_spiders():
    """获取爬虫列表"""
    try:
        spiders = spider_service.get_all_spiders()
        return jsonify(spiders), 200
    except Exception as e:
        return jsonify({'message': 'Internal server error'}), 500

@bp.route('/spiders', methods=['POST'])
@jwt_required()
def create_spider():
    """创建爬虫"""
    try:
        data = request.get_json()
        required_fields = ['name', 'description', 'script_path', 'main_module']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'message': f'Missing required field: {field}'}), 400
        
        spider = spider_service.create_spider(data)
        return jsonify(spider), 201
    except BusinessError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': 'Internal server error'}), 500

@bp.route('/spiders/<spider_id>', methods=['GET'])
@jwt_required()
def get_spider(spider_id):
    """获取爬虫详情"""
    try:
        spider = spider_service.get_spider_by_id(spider_id)
        if spider:
            return jsonify(spider), 200
        return jsonify({'message': 'Spider not found'}), 404
    except Exception as e:
        return jsonify({'message': 'Internal server error'}), 500

@bp.route('/spiders/<spider_id>', methods=['PUT'])
@jwt_required()
def update_spider(spider_id):
    """更新爬虫"""
    try:
        data = request.get_json()
        spider = spider_service.update_spider(spider_id, data)
        return jsonify(spider), 200
    except BusinessError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': 'Internal server error'}), 500

@bp.route('/spiders/<spider_id>', methods=['DELETE'])
@jwt_required()
def delete_spider(spider_id):
    """删除爬虫"""
    try:
        result = spider_service.delete_spider(spider_id)
        if result:
            return jsonify({'message': 'Spider deleted successfully'}), 200
        return jsonify({'message': 'Spider not found'}), 404
    except Exception as e:
        return jsonify({'message': 'Internal server error'}), 500

@bp.route('/spiders/<spider_id>/run', methods=['POST'])
@jwt_required()
def run_spider(spider_id):
    """手动运行爬虫"""
    try:
        result = spider_service.run_spider(spider_id)
        return jsonify(result), 200
    except BusinessError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': 'Internal server error'}), 500

@bp.route('/spiders/runs', methods=['GET'])
@jwt_required()
def list_spider_runs():
    """获取爬虫运行记录"""
    try:
        spider_id = request.args.get('spider_id')
        runs = spider_service.get_spider_runs(spider_id)
        return jsonify(runs), 200
    except Exception as e:
        return jsonify({'message': 'Internal server error'}), 500
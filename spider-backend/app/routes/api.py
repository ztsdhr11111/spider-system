# routes/api.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from app.services.user_service import UserService
from app.utils.exceptions import BusinessError
from datetime import timedelta

bp = Blueprint('api', __name__)
user_service = UserService()

@bp.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({'status': 'ok', 'message': 'Backend is running with MongoDB'})

@bp.route('/register', methods=['POST'])
def register():
    """用户注册接口"""
    try:
        data = request.get_json()
        
        # 验证必要字段
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'message': f'Missing required field: {field}'}), 400
        
        # 调用业务逻辑层
        user_data = user_service.register_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        
        return jsonify({
            'message': 'User created successfully', 
            'user': user_data
        }), 201
        
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': 'Internal server error'}), 500
    
@bp.route('/login', methods=['POST'])
def login():
    """用户登录接口"""
    try:
        data = request.get_json()
        
        # 验证必要字段
        if not data.get('username') or not data.get('password'):
            return jsonify({'message': 'Username and password are required'}), 400
        
        # 调用业务逻辑层进行认证
        user = user_service.authenticate_user(data['username'], data['password'])
        
        if user:
            # 设置token有效期为一周
            access_token = create_access_token(
                identity=user['_id'],
                expires_delta=timedelta(days=7)
            )
            return jsonify({
                'access_token': access_token,
                'user': user
            }), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
            
    except Exception as e:
        return jsonify({'message': 'Internal server error'}), 500

@bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    """获取所有用户接口"""
    try:
        users = user_service.get_all_users()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({'message': 'Internal server error'}), 500

@bp.route('/users/<user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """获取指定用户接口"""
    try:
        user = user_service.get_user_by_id(user_id)
        
        if user:
            return jsonify(user), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'message': 'Internal server error'}), 500
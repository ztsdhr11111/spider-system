# routes/api.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from app.services.user_service import UserService
from app.utils.exceptions import BusinessError
from datetime import timedelta
# 导入 flask-restx 相关模块
from app import api
from flask_restx import Resource, fields

bp = Blueprint('api', __name__)
user_service = UserService()

# 定义 API 模型
health_model = api.model('Health', {
    'status': fields.String(description='状态'),
    'message': fields.String(description='消息')
})

register_model = api.model('Register', {
    'username': fields.String(required=True, description='用户名'),
    'email': fields.String(required=True, description='邮箱'),
    'password': fields.String(required=True, description='密码')
})

register_response_model = api.model('RegisterResponse', {
    'message': fields.String(description='消息'),
    'user': fields.Raw(description='用户信息')
})

login_model = api.model('Login', {
    'username': fields.String(required=True, description='用户名'),
    'password': fields.String(required=True, description='密码')
})

login_response_model = api.model('LoginResponse', {
    'access_token': fields.String(description='访问令牌'),
    'user': fields.Raw(description='用户信息')
})

# 定义命名空间
ns = api.namespace('auth', description='认证相关操作')

@ns.route('/health')
class HealthCheck(Resource):
    @api.doc('health_check')
    @api.marshal_with(health_model)
    def get(self):
        """健康检查接口"""
        return {'status': 'ok', 'message': 'Backend is running with MongoDB'}

@ns.route('/register')
class Register(Resource):
    @api.doc('register_user')
    @api.expect(register_model)
    @api.marshal_with(register_response_model, code=201)
    def post(self):
        """用户注册接口"""
        try:
            data = request.get_json()
            
            # 验证必要字段
            required_fields = ['username', 'email', 'password']
            for field in required_fields:
                if field not in data or not data[field]:
                    return {'message': f'Missing required field: {field}'}, 400
            
            # 调用业务逻辑层
            user_data = user_service.register_user(
                username=data['username'],
                email=data['email'],
                password=data['password']
            )
            
            return {
                'message': 'User created successfully', 
                'user': user_data
            }, 201
            
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': 'Internal server error'}, 500

@ns.route('/login')
class Login(Resource):
    @api.doc('login_user')
    @api.expect(login_model)
    @api.marshal_with(login_response_model)
    def post(self):
        """用户登录接口"""
        try:
            data = request.get_json()
            
            # 验证必要字段
            if not data.get('username') or not data.get('password'):
                return {'message': 'Username and password are required'}, 400
            
            # 调用业务逻辑层进行认证
            user = user_service.authenticate_user(data['username'], data['password'])
            
            if user:
                # 设置token有效期为一周
                access_token = create_access_token(
                    identity=user['_id'],
                    expires_delta=timedelta(days=7)
                )
                return {
                    'access_token': access_token,
                    'user': user
                }, 200
            else:
                return {'message': 'Invalid credentials'}, 401
                
        except Exception as e:
            return {'message': 'Internal server error'}, 500

# 用户相关路由的命名空间
user_ns = api.namespace('users', description='用户相关操作')

@user_ns.route('/')
class Users(Resource):
    @api.doc('get_users')
    @jwt_required()
    def get(self):
        """获取所有用户接口"""
        try:
            users = user_service.get_all_users()
            return users, 200
        except Exception as e:
            return {'message': 'Internal server error'}, 500

@user_ns.route('/<user_id>')
@user_ns.param('user_id', '用户ID')
class User(Resource):
    @api.doc('get_user')
    @jwt_required()
    def get(self, user_id):
        """获取指定用户接口"""
        try:
            user = user_service.get_user_by_id(user_id)
            
            if user:
                return user, 200
            else:
                return {'message': 'User not found'}, 404
        except Exception as e:
            return {'message': 'Internal server error'}, 500